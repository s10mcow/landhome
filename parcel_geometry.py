#!/usr/bin/env python3
"""Measure saved ArcGIS parcel polygons; never infer frontage or a legal boundary.

Lengths and areas use U.S. survey feet. Preserve source coordinates, attributes,
all polygon rings, native CRS, and the conversion used. Require ArcGIS ring
winding (clockwise shells, counterclockwise holes). Accept only unquantized
coordinates with consistent, vetted projected CRS identifiers; reject custom
WKT and coordinate transforms. Reject intersections and touching rings rather
than report an ambiguous area. Merge runs only after checking every vertex and
segment against the complete run chord. Network retrieval and parcel identity
confirmation belong to the calling workflow.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import sys
from pathlib import Path

US_FOOT_METRES = 1200 / 3937
METRES_PER_UNIT = {"us-survey-foot": US_FOOT_METRES, "foot": 0.3048, "metre": 1.0}
CRS_DEFINITIONS = {i: (i, "us-survey-foot") for i in (2236, 2237, 2238)}
CRS_DEFINITIONS.update({102658: (2236, "us-survey-foot"), 102659: (2237, "us-survey-foot"), 102660: (2238, "us-survey-foot")})
CRS_DEFINITIONS.update({i: (i, "metre") for i in (26958, 26959, 26960)})
CRS_DEFINITIONS.update({i: (i, "metre") for i in range(26901, 26924)})
CRS_DEFINITIONS.update({i: (i, "metre") for i in range(32601, 32661)})
CRS_DEFINITIONS.update({i: (i, "metre") for i in range(32701, 32761)})
FORBIDDEN_CRS = {4326, 4269, 4258, 4230, 3857, 3395, 102100, 102113}
MAX_SEGMENTS = 5000
CLOSURE_TOLERANCE_NATIVE = 0.001
STRAIGHT_ANGLE_DEGREES = 0.1
STRAIGHT_DISTANCE_US_FEET = 0.05


class GeometryError(ValueError):
    pass


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def resolve_units(spatial_reference, declared_units=None, geometry_properties=None):
    """Require every provided horizontal ID to resolve to one vetted CRS."""
    if not isinstance(spatial_reference, dict):
        raise GeometryError("A source spatial reference is required; do not guess units.")
    if any(str(k).lower().startswith("wkt") for k in spatial_reference):
        raise GeometryError("Custom/WKT CRS definitions are unsupported; request unquantized coordinates in a vetted projected WKID.")
    if declared_units is not None and declared_units not in METRES_PER_UNIT:
        raise GeometryError("Unsupported declared units.")
    ids = []
    for name in ("wkid", "latestWkid"):
        value = spatial_reference.get(name)
        if isinstance(value, bool):
            raise GeometryError("Invalid spatial reference identifier.")
        if value is not None:
            if not isinstance(value, int) and not (isinstance(value, str) and value.isdecimal()):
                raise GeometryError("Spatial reference identifiers must be integer WKIDs.")
            ids.append(int(value))
    if any(i in FORBIDDEN_CRS or 4000 <= i <= 4999 for i in ids):
        raise GeometryError("Geographic or global Mercator coordinates must be reprojected to a suitable local projected CRS.")
    if not ids or any(i not in CRS_DEFINITIONS for i in ids):
        hint = (geometry_properties or {}).get("units")
        raise GeometryError("Every source WKID must be vetted; request unquantized coordinates in a supported local projected CRS. Source unit hint: " + repr(hint))
    definitions = {CRS_DEFINITIONS[i] for i in ids}
    if len(definitions) != 1:
        raise GeometryError("Source wkid/latestWkid disagree; verify the CRS instead of selecting one identifier.")
    canonical_wkid, unit = definitions.pop()
    if declared_units and declared_units != unit:
        raise GeometryError("Declared units conflict with the recognized CRS; verify the source instead of overriding it.")
    return {
        "canonical_wkid": canonical_wkid,
        "native_unit": unit,
        "native_metres_per_unit": METRES_PER_UNIT[unit],
        "output_length_unit": "us-survey-foot",
        "output_area_unit": "square-us-survey-foot",
        "native_to_us_survey_feet": METRES_PER_UNIT[unit] / US_FOOT_METRES,
        "provenance": "all source horizontal identifiers match one vetted projected CRS",
    }


def _reject_quantization(container, label):
    if any(str(k).lower() in {"transform", "quantizationparameters"} for k in container):
        raise GeometryError(f"{label} contains a coordinate transform/quantization declaration; request unquantized rings without transform or quantizationParameters.")


def _cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _on_segment(a, b, p):
    eps = 1e-8
    return abs(_cross(a, b, p)) <= eps and min(a[0], b[0]) - eps <= p[0] <= max(a[0], b[0]) + eps and min(a[1], b[1]) - eps <= p[1] <= max(a[1], b[1]) + eps


def _intersects(a, b, c, d):
    p, q, r, s = _cross(a, b, c), _cross(a, b, d), _cross(c, d, a), _cross(c, d, b)
    eps = 1e-8
    if ((p > eps and q < -eps) or (p < -eps and q > eps)) and ((r > eps and s < -eps) or (r < -eps and s > eps)):
        return True
    return any((_on_segment(a, b, c), _on_segment(a, b, d), _on_segment(c, d, a), _on_segment(c, d, b)))


def _inside(point, ring):
    x, y = point
    inside = False
    for a, b in zip(ring, ring[1:]):
        if (a[1] > y) != (b[1] > y):
            cross_x = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x < cross_x:
                inside = not inside
    return inside


def _signed_area(ring):
    x0, y0 = ring[0]
    return math.fsum((a[0] - x0) * (b[1] - y0) - (b[0] - x0) * (a[1] - y0) for a, b in zip(ring, ring[1:])) / 2


def _prepare_rings(raw_rings):
    if not isinstance(raw_rings, list) or not raw_rings:
        raise GeometryError("A nonempty ArcGIS rings array is required.")
    rings, notes = [], []
    for index, raw in enumerate(raw_rings):
        if not isinstance(raw, list) or len(raw) < 4:
            raise GeometryError(f"Ring {index} needs at least three vertices plus closure.")
        ring = []
        for vertex in raw:
            if not isinstance(vertex, (list, tuple)) or len(vertex) < 2 or not all(_is_number(v) for v in vertex[:2]):
                raise GeometryError(f"Ring {index} contains invalid/nonfinite XY coordinates.")
            ring.append((float(vertex[0]), float(vertex[1])))
        gap = math.dist(ring[0], ring[-1])
        if gap > CLOSURE_TOLERANCE_NATIVE:
            raise GeometryError(f"Ring {index} is open; do not fabricate its closing boundary.")
        if gap:
            notes.append(f"Ring {index} closing coordinate snapped to first for calculation within {CLOSURE_TOLERANCE_NATIVE} native units; original retained.")
            ring[-1] = ring[0]
        if any(math.dist(a, b) <= 1e-10 for a, b in zip(ring, ring[1:])):
            raise GeometryError(f"Ring {index} has a zero-length edge.")
        if abs(_signed_area(ring)) <= 1e-10:
            raise GeometryError(f"Ring {index} is degenerate.")
        rings.append(ring)
    segment_count = sum(len(r) - 1 for r in rings)
    if segment_count > MAX_SEGMENTS:
        raise GeometryError(f"More than {MAX_SEGMENTS} segments: use a GIS geometry validator before measuring.")
    # Translate every ring by a common origin for stable orientation comparisons.
    origin = rings[0][0]
    local = [[(x - origin[0], y - origin[1]) for x, y in r] for r in rings]
    for ri, ring in enumerate(local):
        count = len(ring) - 1
        for i in range(count):
            for j in range(i + 1, count):
                if j == i + 1 or (i == 0 and j == count - 1):
                    continue
                if _intersects(ring[i], ring[i + 1], ring[j], ring[j + 1]):
                    raise GeometryError(f"Ring {ri} self-intersects or touches itself.")
        for rj in range(ri):
            other = local[rj]
            if any(_intersects(a, b, c, d) for a, b in zip(ring, ring[1:]) for c, d in zip(other, other[1:])):
                raise GeometryError(f"Rings {rj} and {ri} intersect/touch; topology requires GIS review.")
    depths = [sum(_inside(r[0], other) for j, other in enumerate(local) if j != i) for i, r in enumerate(local)]
    for i, (ring, depth) in enumerate(zip(local, depths)):
        if (_signed_area(ring) < 0) != (depth % 2 == 0):
            raise GeometryError(f"Ring {i} winding conflicts with ArcGIS clockwise-shell/counterclockwise-hole convention.")
    return rings, depths, notes


def _runs(ring, factor):
    """Merge only if the whole candidate is straight within both tolerances."""
    count = len(ring) - 1

    def straight(i):
        a, b, c = ring[(i - 1) % count], ring[i], ring[(i + 1) % count]
        u, v = (b[0] - a[0], b[1] - a[1]), (c[0] - b[0], c[1] - b[1])
        dot = u[0] * v[0] + u[1] * v[1]
        if dot <= 0:
            return False
        angle = math.degrees(math.atan2(abs(u[0] * v[1] - u[1] * v[0]), dot))
        distance = abs(_cross(a, c, b)) / math.dist(a, c) * factor
        return angle <= STRAIGHT_ANGLE_DEGREES and distance <= STRAIGHT_DISTANCE_US_FEET

    corners = [i for i in range(count) if not straight(i)]
    if len(corners) < 3:
        raise GeometryError("Boundary runs do not define a usable polygon.")
    def measure(start, end, indexes, rejection=None):
        a, b = ring[start], ring[end]
        chord_native = math.dist(a, b)
        path = math.fsum(math.dist(ring[i], ring[i + 1]) for i in indexes) * factor
        offsets = [abs(_cross(a, b, ring[(i + 1) % count])) / chord_native * factor for i in indexes] if chord_native else [math.inf]
        vector = (b[0] - a[0], b[1] - a[1])
        angles = []
        for i in indexes:
            u = (ring[i + 1][0] - ring[i][0], ring[i + 1][1] - ring[i][1])
            dot = u[0] * vector[0] + u[1] * vector[1]
            angles.append(math.degrees(math.atan2(abs(u[0] * vector[1] - u[1] * vector[0]), dot)))
        offset, angle = max(offsets), max(angles)
        value = {"start_vertex_index": start, "end_vertex_index": end, "source_segment_indices": indexes, "path_length_ft": path, "chord_length_ft": chord_native * factor, "display_length_ft": f"{path:.1f}", "merged": len(indexes) > 1, "maximum_vertex_offset_ft": offset, "maximum_segment_angle_degrees": angle}
        if rejection:
            value["merge_rejection_reason"] = rejection
        return value

    result = []
    for n, start in enumerate(corners):
        end = corners[(n + 1) % len(corners)]
        indexes = []
        current = start
        while current != end:
            indexes.append(current)
            current = (current + 1) % count
        candidate = measure(start, end, indexes)
        if candidate["maximum_vertex_offset_ft"] <= STRAIGHT_DISTANCE_US_FEET and candidate["maximum_segment_angle_degrees"] <= STRAIGHT_ANGLE_DEGREES:
            result.append(candidate)
        else:
            # Preserve source segments when a gently curving chain passes local
            # tests but bows away from the complete endpoint chord.
            for i in indexes:
                result.append(measure(i, (i + 1) % count, [i], "candidate exceeds whole-run straightness tolerance"))
    return result


def analyze_feature(feature, spatial_reference, units=None, geometry_properties=None):
    if not isinstance(feature, dict):
        raise GeometryError("Invalid feature object.")
    geometry = feature.get("geometry")
    if not isinstance(geometry, dict) or "rings" not in geometry or "curveRings" in geometry:
        raise GeometryError("Only linear polygon rings are supported; true curves require GIS review.")
    _reject_quantization(feature, "Feature")
    _reject_quantization(geometry, "Geometry")
    sr = geometry.get("spatialReference", spatial_reference)
    conversion = resolve_units(sr, units, geometry_properties)
    if "spatialReference" in geometry and spatial_reference is not None:
        layer_conversion = resolve_units(spatial_reference, units, geometry_properties)
        if layer_conversion["canonical_wkid"] != conversion["canonical_wkid"]:
            raise GeometryError("Query and geometry spatial references disagree; request consistent source coordinates.")
    factor = conversion["native_to_us_survey_feet"]
    rings, depths, notes = _prepare_rings(geometry["rings"])
    signed = [_signed_area(r) for r in rings]
    native_area = abs(math.fsum(signed))
    area = native_area * factor**2
    acres = area / 43560
    if not math.isfinite(area) or area <= 0:
        raise GeometryError("Invalid computed area.")
    attributes = copy.deepcopy(feature.get("attributes", {}))
    if not isinstance(attributes, dict):
        raise GeometryError("Invalid attributes object.")
    by_lower = {str(k).lower(): v for k, v in attributes.items()}
    legal = by_lower.get("legal_acreage")
    if legal is not None and (not _is_number(legal) or legal < 0):
        raise GeometryError("Invalid appraiser legal_acreage value.")
    threshold = max(0.01, acres * 0.01)
    discrepancy = None if legal is None else abs(acres - legal) > threshold
    measured_rings = []
    for index, (ring, depth, signed_area) in enumerate(zip(rings, depths, signed)):
        edges = []
        for i, (a, b) in enumerate(zip(ring, ring[1:])):
            length = math.dist(a, b) * factor
            edges.append({"segment_index": i, "start_vertex_index": i, "end_vertex_index": i + 1, "length_ft": length, "display_length_ft": f"{length:.1f}"})
        measured_rings.append({"ring_index": index, "nesting_depth": depth, "role": "shell" if depth % 2 == 0 else "hole", "winding": "clockwise" if signed_area < 0 else "counterclockwise", "signed_native_area": signed_area, "segments": edges, "straight_boundary_runs": _runs(ring, factor)})
    return {
        "attributes": attributes,
        "source_spatial_reference": copy.deepcopy(sr),
        "unit_conversion": conversion,
        "computed_area_sq_ft": area,
        "computed_area_acres": acres,
        "computed_area_display_acres": f"{acres:.3f}",
        "appraiser_legal_acreage": legal,
        "source_gis_area_attribute": by_lower.get("gis_area"),
        "acreage_discrepancy": discrepancy,
        "acreage_discrepancy_threshold_acres": threshold,
        "acreage_difference_acres": None if legal is None else acres - legal,
        "source_geometry": copy.deepcopy(geometry),
        "rings": measured_rings,
        "notes": notes,
        "limits": ["GIS estimates for preliminary layout; legal boundaries require survey/record verification.", "Parcel identity must be confirmed independently against address and parcel identifier.", "Frontage, depth, page orientation, north, setbacks and buildability are not inferred.", "Area uses summed signed ArcGIS rings after closure, intersection and winding checks; this is not a complete cadastral/topology validation.", "Reported acreage uses 43,560 square U.S. survey feet per acre; source acreage fields remain independent."],
    }


def analyze_query(data, units=None, source_url=None):
    if not isinstance(data, dict):
        raise GeometryError("Expected an ArcGIS query JSON object.")
    _reject_quantization(data, "Query")
    if "error" in data:
        raise GeometryError("ArcGIS returned an error; retrieval failure is not evidence that the parcel does not exist: " + str(data["error"]))
    if data.get("exceededTransferLimit"):
        raise GeometryError("Query response is incomplete; retrieve all intended features before analysis.")
    if data.get("geometryType") not in (None, "esriGeometryPolygon"):
        raise GeometryError("Query does not contain parcel polygons.")
    features = data.get("features")
    if not isinstance(features, list) or not features:
        raise GeometryError("No features returned. Verify query/parcel identity; do not infer that the address does not exist.")
    return {"schema_version": 1, "source_url": source_url, "measurement_status": "preliminary_gis", "feature_count": len(features), "features": [analyze_feature(f, data.get("spatialReference"), units, data.get("geometryProperties")) for f in features], "straight_run_tolerances": {"maximum_turn_degrees": STRAIGHT_ANGLE_DEGREES, "maximum_intermediate_vertex_offset_ft": STRAIGHT_DISTANCE_US_FEET}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Saved ArcGIS feature query JSON")
    parser.add_argument("--units", choices=METRES_PER_UNIT, help="Confirm vetted CRS units; cannot override CRS units or accept custom WKT")
    parser.add_argument("--source-url", help="Official query URL retained as provenance")
    parser.add_argument("--output", type=Path, help="Write JSON here instead of stdout")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        result = analyze_query(data, args.units, args.source_url)
        rendered = json.dumps(result, indent=2, allow_nan=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
    except (OSError, ValueError, TypeError) as exc:
        print("parcel_geometry: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

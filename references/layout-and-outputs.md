# Layout and output rules

## Input and evidence record

Record the following for each parcel. Leave unknown values null with an open-item note; do not use zero for unknown offsets or elevations.

- Address, APN, county and governing jurisdiction; source URLs and retrieval dates.
- Boundary source type: current survey, recorded plat, GIS, or user dimensions; source CRS/units and full geometry.
- Measured boundary runs, frontage evidence, computed square feet/acres, appraiser acreage and discrepancies.
- Road/ROW edge and width when known, easement geometry, tree/protection areas, drainage/flood constraints and relevant neighboring features.
- CutSheetRX screen when run: page URL, check date, flight date and quality label if shown, which outline was drawn, and the readings in [CutSheetRX](cutsheet-rx.md). Leave the block null when the screen was not run or the zoomed parcel had no lidar. Do not store zero elevation or zero cut to mean "not checked." Keep drawn acres off the legal and GIS acreage lines. Note the result on the sheet as an approximate constraint. Do not draw the lidar contours as surveyed contours.
- Home model/footprint/bedrooms and basis; layout revision; each improvement's coordinates and verified versus assumed status.
- Known versus assumed design criteria, site evaluation status, and required professional/agency review.

## Geometry and placement

Use a local feet-based drawing frame only after locating its origin, axes, frontage, and rotation relative to the source geometry. Record that transform. Preserve the actual polygon and holes instead of replacing it with a convenient rectangle. Translate large GIS coordinates before shoelace calculations to reduce numerical cancellation.

Trace each proposed footprint against the actual parcel and known constraints. Check the full septic reservation and well point, not just the label or center. Measure offsets perpendicular to the specified line where that is the intended offset; do not confuse them with distance to a vertex or distance along a side. Keep side lengths, frontage length and perpendicular lot depth distinct on irregular parcels.

Do not fabricate a rectangular buildable envelope when setbacks/easements or an irregular boundary are unresolved. Show missing criteria in the open-items panel and make only conceptual placement claims. Place optional steps, deck, HVAC and pump components only from known selections or explicit assumptions.

Keep future well service and septic installation access in view. Home delivery, well drilling, septic construction and final driveway work can require different corridors. Do not claim access is verified from imagery; note transporter/installer field confirmation where pending.

## Sheet composition

Use a readable sheet and scale selected for the actual lot. Default to 11 x 17 inches when it improves legibility; preserve print scale at 100 percent. State the actual chosen scale (for example 1 inch = 40 feet only when the drawn geometry truly matches). Include a scale bar and physical page size. Mark context aerials/insets not to scale unless scaled independently and correctly.

Keep main boundary and dimension lines clear, use distinct vector line styles for proposed and known features, and separate notes from labels. Show the revision/date and source basis in a title block. Place uncertain features in dashed outlines with local `ASSUMED` or `PROPOSED RESERVATION` labels. Show north only when its relationship to the drawing is established.

On acreage conflicts, print both values and the unresolved status. Do not suppress them to make the title block cleaner. On unknown survey/septic inputs, keep the draft visibly preliminary rather than silently promoting it to a permit-ready sheet.

## Review and delivery

Perform a geometry check and a rendered-page check. In the geometry review, verify parcel identity, boundary runs, area, coordinate transform, offsets, feature containment, known constraints, and no intended overlap of well, field, home and truck corridor. Limit findings to the checks actually possible from the evidence.

In the visual review, inspect the PDF and editable SVG for consistent geometry, scale, north, labels, margins, notes and readable dimension text. Save one explicit drawing identity/version for the user to share; do not send to trades or others without instruction. Keep generated sheets unsealed. Retain an authentic professional seal/signature only on a separate, unchanged source attachment; never edit a sealed source into a different design or reuse its seal.

Save final user-facing PDFs, SVGs and source/input JSON using the current Library workflow. Treat a published/accepted packet number, upload timestamp or filename as metadata, not evidence of permit approval. Ask for a new survey or qualified design only where the actual pending decision requires it; continue useful conceptual work meanwhile.

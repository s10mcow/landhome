---
name: lot-to-proposed-site-plan
description: Retrieve and measure official parcel boundaries from an address or parcel ID, reconcile lot dimensions and acreage, and create a scaled proposed manufactured-home site plan with home, well, septic area, driveway, and delivery access. Use for land-home property intake, lot measurements, GIS or aerial checks, adapting the Laurel layout, preliminary site plans, and drafting jurisdiction-specific permit packets for Rising Tide and Requity, especially in Flagler County, Florida. Look up lot dimensions automatically before asking the user to provide them.
---

# Lot to Proposed Site Plan

Turn an address, parcel ID, survey, or referenced lot into sourced measurements and a parcel-specific proposed plan. Treat automatic dimension retrieval as the first deliverable, even when the user requests only a layout. Use the Laurel arrangement as an editable preference, never as evidence about a new parcel.

For a new property added through this workflow, run [Draft permit packets](references/permit-packet.md) alongside the preliminary site plan. Reuse the same property data. Return both drafts and their open items. A standalone measurement or layout request stays scoped to that deliverable unless the user asks for the packet.

## 1. Resolve the property and collect measurements

1. Resolve the address to the county's official property-appraiser or GIS record. If the user supplied an APN, match it exactly and cross-check the situs address and legal lot/block. For a vacant lot with no situs, cross-check the legal description, plat/lot/block, and mapped road location instead; do not invent an address. Record which identity fields were actually checked. Do not silently substitute a nearby parcel. Preserve the official APN format; formatting/order can differ among systems.
2. Use the county's parcel-boundary service and its native coordinate system. For Flagler, read [Flagler sources](references/flagler-and-laurel.md). For another county, discover its official layer and inspect its fields, CRS, and units before querying. Prefer an existing authoritative survey or recorded plat for boundary evidence, and use GIS to obtain working measurements and compare sources.
3. Query attributes AND complete polygon geometry. Check for service errors, empty results, candidate ambiguity and transfer/pagination limits; require complete geometry and one resolved match per intended parcel. Retain source URL, retrieval date, parcel identity, CRS, units, every ring, appraiser acreage, and GIS acreage. Retrieve aerial imagery with parcel overlay when it helps the task at a reasonable cost; record the image date when known. Never measure legal boundaries from clearing, fences, tree lines, or aerial pixels alone.
4. Use available public HTTP or browsing tools first. If a tool cannot read the query, try an available connected fetch/extract service, following its discovery and pricing instructions. A local networking failure is not proof that the property is absent. Do not ask the user to measure a lot merely because one retrieval route failed.
5. Save the actual query response as JSON, then use `parcel_geometry.py` to calculate boundary segments/runs and area in a suitable local projected CRS. Obtain full, unquantized rings; reject transformed/quantized responses and requery without coordinate quantization. Reject geographic degrees and Web Mercator as a basis for foot measurements. The helper supports vetted CRS identifiers/aliases only; reproject or request a suitable local UTM CRS when another source CRS is unsupported. Do not override mismatching or unknown CRS metadata with guessed units. Do not treat an extent or bounding box as the parcel, or collapse a curved/densified boundary into a straight side.
6. Match the returned feature to the intended parcel before using any calculation. Preserve nonrectangular boundaries, holes, multipart parcels, and intervening rights-of-way; do not stretch or square the shape to match a template. If geometry is unsupported or suspect, report that limitation and obtain a plat/survey or competent geometry processing.
7. Identify the road frontage using official road/ROW or plat evidence, corroborated by the map. Label frontage/depth only once that edge is known. Preserve true or grid north separately from page-up; rotate all features and the north arrow consistently. If frontage or north is unresolved, label it unresolved and produce measurements without inventing a road or orientation.

For missing address/county, attempt resolution from the current property reference and available files. Ask only for the minimum identifier needed to choose the correct parcel when ambiguity remains.

## 2. Reconcile the evidence before placing improvements

Produce a short measurement table: frontage where known, other boundary runs, measured area, appraiser acreage, supplied-plan dimensions, and evidence status. Label GIS-derived numbers approximate; retain precision in the JSON without implying survey accuracy in labels.

Keep computed geometry area, GIS acreage fields, appraiser/legal acreage, and quoted listing dimensions separate. Do not average conflicting values or invent a right-of-way deduction to explain a discrepancy. Flag material differences in both the plan and source JSON. Use conceptual geometry while keeping its uncertainty visible; obtain survey/plat clarification before relying on disputed acreage or boundaries for permitting/design.

Never claim that a source was checked unless it was actually retrieved. Do not copy historical values from the reference as if they were fresh results. If official measurements cannot be obtained, return what is verified and clearly identify any user-supplied dimensions used for an explicitly conceptual drawing.

## 3. Build the parcel-specific proposed layout

Read [Layout and output rules](references/layout-and-outputs.md). Keep the preferred home model, front-corner well access, driveway beside the home, and rear septic reservation where the actual parcel supports them. Use a mirrored option when site constraints favor the other side.

Keep all assumptions explicit. Define offsets by reference and direction: front boundary to nearest home edge, side boundary to well point, or driveway edge versus centerline. Confirm model dimensions, bedrooms, doors, steps/decks, HVAC, installation clearances, and transporter access before calling placement settled.

Verify current local setbacks, easements, ROW, tree, flood/drainage and septic/well requirements from primary sources when using them to assess compliance. Carry unknown values as unknown. Do not label a buildable envelope or a compliant separation without the necessary evidence.

Reserve a conceptual septic area until the evaluator/installer determines the actual system and footprint. Do not infer soils, seasonal water table, elevation, neighboring system positions, or treatment requirements from imagery. Coordinate home/pad, septic, well, drainage, utilities, road entrance, delivery and later excavation access together. Review adjacent project lots together where relevant.

## 4. Create, check, and deliver the proposed plan

1. Use available PDF tooling for PDF deliverables. In ChatGPT Work, use the Library workflow for current source files and saving generated plans. In Hermes, use the authorized private project workspace. Use deterministic vector drawing or CAD tools, not image generation, for measurements and diagrams.
2. Default to one scaled vector PDF and an editable SVG, with the parcel-specific input/source JSON. If the user asks only for dimensions, return the sourced measurements without generating unnecessary files. If evidence is insufficient for a responsible layout, deliver the measurements and unresolved layout inputs first.
3. Title drawings `PROPOSED SITE PLAN - PRELIMINARY`; add `Not a boundary survey. Subject to survey, site evaluation, professional design and agency approval.` Label reservations and assumed features at the feature itself, not only in a remote footnote. Keep every generated sheet unsealed; never transfer a professional seal/signature or approval stamp onto it. Retain an authentic seal only on a separate, unchanged source attachment. Do not invent a license number or approval.
4. Show property identity, actual boundary shape/run dimensions, source basis/date, units, frontage/road evidence, north when known, drawing scale/scale bar, proposed home and offsets, well, septic reservation, driveway/entry, delivery corridor, known constraints, and a concise assumptions/open-items panel. Include conflicting acreage prominently.
5. Compute scale from actual page units. Preserve aspect ratio and geometry. Use a larger sheet or another stated scale when the lot will not fit; never stretch it while retaining an old scale label. State print-at-100-percent and distinguish a scaled plan from a not-to-scale context inset.
6. Check feature containment, measured offsets, intended non-overlaps, usable delivery and later trade access, and known constraints. Report what was checked. Treat any automated geometric check as a drawing check, not regulatory or engineering approval. Where required criteria are unknown, say they remain unverified.
7. Render and visually inspect every final page at readable resolution. Verify labels/dimensions, scale, north, legend, page margins and footer, and absence of clipped or overlapping content. Save generated deliverables and link the saved result. Preserve existing file identity when editing a plan; keep one explicit revision for all trades.

End with the measured lot dimensions, the chosen arrangement, and the few unresolved items that affect submission or fieldwork. Progress on the concept without asking approval for routine reversible layout choices. Keep permit filing, spending commitments and construction outside this skill unless separately authorized.

## Geometry helper

Resolve `parcel_geometry.py` relative to this skill's directory. Run `python3 parcel_geometry.py parcel-query.json --source-url ACTUAL_OFFICIAL_QUERY_URL --output measured-parcel.json`, replacing the placeholder with the quoted retrieved URL. Preserve the retrieval date in the input/source record. Use `--units` only to confirm verified units of a supported CRS; it does not add support for an unknown CRS or WKT. Request unquantized coordinates and a suitable vetted local projected CRS when required. Read the helper's warnings and preserve them in the drawing assumptions. For a multi-feature response, choose the exact matching parcel before drafting; do not use the first result by position.

## Supporting resources

- [Flagler sources and Laurel examples](references/flagler-and-laurel.md): official retrieval route, cross-check fields, known example conflicts and layout preferences.
- [Layout and output rules](references/layout-and-outputs.md): geometry, assumption handling, feature placement and output checklist.
- [Draft permit packets](references/permit-packet.md): jurisdiction routing, verified intake, official form prefills, and filing checklist.
- `fixtures/laurel-county-parcels.json`: dated public-data regression fixture; use only for helper checks, never as a fresh live lookup.

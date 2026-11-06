# Flagler sources and Laurel examples

## Source registry (checked 2026-11-04; verify current links and requirements)

| Purpose | Primary source |
| --- | --- |
| County parcel layer published by Palm Coast | https://gis.palmcoast.gov/hosting/rest/services/External/FlaglerCountyParcels/MapServer/1 |
| Property-appraiser GIS entry point | https://flaglerpa.com/gis/ |
| County GIS map portal | https://www.flaglercounty.gov/County-Services/Geographic-Information-Systems |
| Current county permitting packets | https://www.flaglercounty.gov/Growth-Building/Central-Permitting |
| Mobile-home packet | https://www.flaglercounty.gov/files/assets/county/v/1/growth-management/documents/central-permitting-doc-center/requirements-for-contractors-applying-online/onlinemobilehomecontractor_packet.pdf |
| ROW / culvert / driveway packet | https://www.flaglercounty.gov/files/assets/county/v/1/growth-management/documents/central-permitting-doc-center/printable-permit-forms/right-of-way-culvert-dri.pdf |
| Current separately published tree form | https://www.flaglercounty.gov/files/assets/county/v/1/growth-management/documents/tree-protection-form.pdf |
| Septic application / site plan / evaluation | https://floridadep.gov/sites/default/files/DEP%204015_0.pdf |
| Flagler well program | https://flagler.floridahealth.gov/programs-and-services/environmental-public-health/water-well-construction/ |

The county mobile-home packet has included older embedded tree forms. Obtain current standalone forms through the official page rather than reusing embedded calculations. Distinguish unincorporated Flagler from Bunnell, Palm Coast, and other incorporated jurisdictions; a Bunnell mailing address alone does not resolve the permitting authority.

## Retrieve dimensions automatically

Inspect layer metadata before relying on its schema. The checked layer uses `PARCELNO` (hyphenated), `situs_num`, `situs_street`, `legal_acreage`, `GIS_AREA`, and polygon rings in WKID 102658 / EPSG 2236, Florida East US survey feet.

Build an HTTPS GET to `<layer-url>/query` with URL-encoded parameters:

```json
{
  "where": "PARCELNO = '13-12-28-1800-00470-0180'",
  "outFields": "OBJECTID,PARCELNO,situs_num,situs_street,Legal,block,lot,legal_acreage,GIS_AREA",
  "returnGeometry": "true",
  "f": "pjson"
}
```

Use the actual parcel ID after resolving its address. Escape SQL string literals correctly; never concatenate unvalidated arbitrary input. Confirm that the response has no service error or transfer-limit flag and exactly one resolved match for a single-parcel query. If using address discovery, query the actual schema for number/street, then verify every candidate's legal identity. If a service omits legal/lot/block fields, cross-check a property-appraiser or plat record and record that separate source. Handle absent situs on vacant parcels using legal/plat identity. Never infer county service APNs by blindly reversing digit groups. Do not reuse object IDs as stable parcel identifiers.

Save the returned JSON and query URL, then run the geometry helper. `GIS_AREA` in this checked layer is an acreage field, not square feet; use the geometry to calculate square footage. Recheck this interpretation against each other service. Retrieve the entire, unquantized geometry: a straight boundary can include additional collinear vertices, while a densely segmented curved boundary must retain its actual shape.

If local HTTP or web retrieval fails, use an available connected web-fetch service. A working session route was a live fetch of the fully encoded official query through Treg; discover current endpoint parameters/pricing instead of assuming that tool is installed. Do not require the user to supply measurements when another public-source route remains available.

## Historical regression cases; do not treat as current lookups

| Address / APN | GIS measurements checked 2026-11-04 | Separate acreage attribute |
| --- | --- | --- |
| 1573 Laurel Ave / 13-12-28-1800-00250-0050 | About 165.00 x 300.00 ft; 1.13613 mapped acres | `legal_acreage` 1.036; cause of discrepancy unverified |
| 2285 Laurel Ave / 13-12-28-1800-00470-0180 | About 165.00 x 319.98 ft; 1.21200 mapped acres | `legal_acreage` 1.212 |

The supplied 1573 concept states 165 x 300 ft / 49,500 sf. The supplied 2285 concept states 165 x 319 ft / 52,635 sf. The mapped 2285 polygon is closer to 320 ft deep and about 52,795 sf. Do not present either PDF as a survey or proof of approval. The fixture preserves both official query records to test measurements and discrepancy handling.

## User's preferred starting arrangement

- Use a 68 x 28 ft home as the reference model only; replace with actual manufacturer dimensions or label assumed.
- Reference home placement is 60 ft from the front line to the front home edge and 62 ft from the left boundary to the home edge in a street-at-bottom local drawing frame. These are preferences, not verified universal setbacks.
- Prefer an accessible front-corner well, starting on the left and mirroring where constraints favor the right. Reference offsets are 15 ft from the side and 10 ft from the front boundary. Verify all well siting constraints, neighboring systems and future rig access.
- The supplied concepts show a 20-ft-wide driveway alongside the home and describe it as flush with the home side. Record side, width and gap separately: left side in the street-at-bottom drawing frame, width 20 ft, conceptual gap zero. These are reference assumptions, not construction clearances. The source calls that side west, but re-establish the real compass direction from current GIS/plat evidence. Verify entrance location, edge versus centerline and turning requirements. Do not assume the transporter's full swept path equals the driveway width.
- Reserve a rear septic area; reference rectangles are 60 x 35 ft or rotated 35 x 60 ft. Label the area a conceptual reservation until the evaluator identifies whether it is active field, overall system/mound footprint or another area. Do not infer a pump is needed from the reference drawing.
- Reference house-rear-to-septic annotation is 75 ft. It is not a statutory separation, not well-to-septic clearance, and not a reason to lengthen the sewer run on a deeper lot.
- Show a proposed road entry and culvert only as applicable. Flagler's checked ROW packet specifies 40-ft culvert length where required, with diameter varying by location; confirm current permit specifications and road authority before treating that as the project design. Never transfer it automatically to another jurisdiction.
- Remove the old address, owner, APN, north arrow, lot dimensions, trees and easements before adapting the concept; add them back only from the current parcel evidence. Preserve page orientation independently of geographical north.

## Desktop terrain screen

CutSheetRX is not a Flagler permit source. Before calling a vacant lot buildable, or before freezing the pad, well, septic, and driveway, follow [CutSheetRX](cutsheet-rx.md). County flood, ROW, septic, and well requirements stay on the official sources above. Lidar from that page does not set a culvert size or a finished floor.

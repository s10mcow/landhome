# Landhome

Dedicated skills for Rising Tide and Requity land-home packages. The root site-plan skill can retrieve official lot dimensions, reconcile mapped and recorded acreage, and prepare a parcel-specific proposed manufactured-home site plan.

Start with [SKILL.md](SKILL.md). Give the agent an address or parcel ID and the selected home information. The workflow looks up parcel measurements first.

Before a vacant lot is called buildable, or before the pad, well, septic, and driveway are frozen, the site-plan skill runs a [CutSheetRX](references/cutsheet-rx.md) screen. That public page reads USGS 3DEP bare-earth lidar and Esri imagery for elevation, a profile slope, standing water, and rough cut/fill. The numbers are approximate lidar estimates, not a survey, septic design, or sealed grading plan. No account or API key is required.

## Contents

- `SKILL.md`: parcel lookup, evidence reconciliation, layout and drawing workflow.
- `parcel_geometry.py`: standard-library Python helper for a retrieved ArcGIS parcel response.
- `references/`: Flagler sources, editable Laurel layout preferences, and output rules.
- `references/cutsheet-rx.md`: public USGS 3DEP screen for lot drainage and rough pad cut/fill. Run it before calling a vacant lot buildable.
- `fixtures/laurel-county-parcels.json`: historical public GIS response for measurement checks, not a current lookup.
- `agents/openai.yaml`: skill display metadata.

The helper measures a saved response. Live parcel retrieval is performed by the agent using available official-source web or HTTP tools. Generated plans are preliminary and unsealed. The instructions and geometry helper have been reviewed and the measurement cases tested; a complete PDF/SVG drawing run has not yet been exercised.

Keep private project records, generated plans, credentials and runtime outputs outside this source repository.

## Scheduling

Use [Landhome Scheduling](skills/schedule-landhome-projects/SKILL.md) to turn a contract or project record into parallel preconstruction work, readiness checks, a two-week trade plan, and separate GC-completion and occupancy forecasts. It includes a high-level flowchart, phase dependencies, Flagler source links, and portal behavior/acceptance requirements.

Example: “Use $schedule-landhome-projects to review this lot, show what can start now and what is blocked, and explain our GC completion and CO forecasts.”

The scheduling skill plans and reviews using available records; it does not install a scheduling engine in the portal or create background monitoring. Live changes and outside commitments require the corresponding user authorization and tools.

# Landhome

Standalone skill for Rising Tide and Requity land-home packages: retrieve official lot dimensions, reconcile mapped and recorded acreage, and prepare a parcel-specific proposed manufactured-home site plan.

Start with [SKILL.md](SKILL.md). Give the agent an address or parcel ID and the selected home information. The workflow looks up parcel measurements first.

## Contents

- `SKILL.md`: parcel lookup, evidence reconciliation, layout and drawing workflow.
- `parcel_geometry.py`: standard-library Python helper for a retrieved ArcGIS parcel response.
- `references/`: Flagler sources, editable Laurel layout preferences and output rules.
- `fixtures/laurel-county-parcels.json`: historical public GIS response for measurement checks, not a current lookup.
- `agents/openai.yaml`: skill display metadata.

The helper measures a saved response. Live parcel retrieval is performed by the agent using available official-source web or HTTP tools. Generated plans are preliminary and unsealed. The instructions and geometry helper have been reviewed and the measurement cases tested; a complete PDF/SVG drawing run has not yet been exercised.

Keep private project records, generated plans, credentials and runtime outputs outside this source repository.

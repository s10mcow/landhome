# Manufactured-home sub-cost estimates

Requity land-and-home sub-cost context for Flagler, St. Johns, Clay, Duval, Volusia, and Putnam. This skill repo has no pricing model. These files are the structured data.

**Every dollar figure is an estimate.** None of it is a bid, a contract, or a quote for a specific parcel. Confirm current fees and contractor prices before using them. A blank amount was not found; it is not zero.

| File | What it is |
| --- | --- |
| [flagler-baseline-quotes.md](flagler-baseline-quotes.md) | Flagler call list: GC, site work, fees, homes, and the $190,000-$210,000 land-and-home package range. |
| [county_sub_costs.md](county_sub_costs.md) | Per-county sheets with sources. |
| [county_sub_costs.csv](county_sub_costs.csv) | Same county rows, one record per line. |
| [county_sub_costs.json](county_sub_costs.json) | Same county rows plus the Flagler baseline, for anything that needs structured data. `figure_status` is `estimate` on every record. |
| [county_sub_costs.xlsx](county_sub_costs.xlsx) | County sheets and a Summary tab. The Summary rollup is not the land-and-home package range. |
| [build.py](build.py) | Regenerates the five files above. |

Regenerate with `python3 references/sub-costs/build.py` from the repo root. That requires `openpyxl`. Do not hand-edit the generated files; change `build.py` and run it again.

These estimates do not change parcel measurement, setbacks, or site-plan rules.

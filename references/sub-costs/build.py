#!/usr/bin/env python3
"""Write Requity manufactured-home sub-cost estimates next to this script.

Every dollar figure is an estimate, not a bid or a parcel-specific quote.
Outputs:

- county_sub_costs.xlsx
- county_sub_costs.csv
- county_sub_costs.md
- county_sub_costs.json
- flagler-baseline-quotes.md

Adapted from the attached county-sheet generator. County rows are the
researched sheets. The Flagler baseline is the separate call list.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

OUT = Path(__file__).resolve().parent
FIGURE_STATUS = "estimate"
DISCLAIMER = (
    "All dollar figures are estimates. They are not bids, contracts, or quotes "
    "for a specific parcel. Fee schedules, dealer prices, and contractor quotes "
    "change; confirm the current amount before relying on it. A blank low or high "
    "means that figure was not found, not that the cost is zero."
)
CALLS = "User's own Flagler calls (baseline)"
NF = "not found"
T_WELL = "Treg: perplexity.web.search.fast"
S_SEP_FL = "https://septicandwell.com/articles/septic-installation-cost-florida (via Treg: perplexity.web.search.fast)"
S_SETUP = "https://www.localmovers.com/moving-resources/what-it-costs-to-set-up-a-manufactured-home (via Treg: perplexity.web.search.fast)"
S_OCALA = "https://ocalalevelpros.com/blog/mobile-home-setup-florida/ (via Treg: perplexity.web.search.fast)"
S_REQ = "https://requitygroup.com/insights/land-home-package-cost/ (via Treg: perplexity.web.search.fast)"
S_RMH = "https://realmobilehomes.com/guides/manufactured-home-installation-setup (via Treg: perplexity.web.search.fast)"
S_EFL = "https://estimateflorida.com/manufactured-home-cost-estimator/ (via Treg: perplexity.web.search.fast)"
HEADERS = ["Line item", "Low", "High", "Unit", "Source", "Notes", "Figure status"]


def common():
    """Statewide or generic items repeated on every county sheet."""
    return [
        ("Install: block/tie/level/marry (DW)", 7000, 20000, "job", S_SETUP, "All-in set/block/level/anchor range, not county-specific. Baseline $12-14K incl ~$2K plumbing"),
        ("Tie-down/anchor package (component)", 1500, 3000, "job", S_OCALA, "Ocala installer price list"),
        ("Delivery & setup (DW, dealer)", 4000, 10000, "job", S_REQ, "Often included in dealer price - confirm"),
        ("Electric service / pole hookup", 1000, 3000, "job", S_RMH, "Generic connection to pole/underground; baseline $4,500"),
        ("FPL / JEA / co-op line extension", None, None, "job", NF, "No published residential drop fee found; baseline says FPL pole drop free recently"),
        ("HVAC (central A/C)", 4000, 9000, "job", S_REQ, "Baseline ~$6K"),
        ("Skirting (vinyl)", 1200, 3500, "job", S_OCALA, "Baseline ~$1,800; localmovers lists vinyl $630-1,550"),
        ("Steps (all entrances, + small porch)", 500, 2000, "job", S_RMH, "Baseline ~$800 each/$2,400; FHA needs steps at every door"),
        ("Siding", None, None, "job", NF, "Baseline $1,500-2,000"),
        ("Interior trim-out", None, None, "job", NF, "Baseline ~$3K; Champion trim $3K"),
        ("Final cleaning", None, None, "job", NF, "Baseline ~$200"),
        ("Site prep / clearing (wooded)", 1000, 10000, "job", S_EFL + " / " + S_RMH, "Baseline ~$8K hauled"),
        ("Boundary survey", None, None, "job", NF, "Baseline ~$1K (+tree survey in Flagler; SWA trip $200)"),
        ("Driveway & access", 3000, 8000, "job", S_EFL, "Baseline millings ~$2,400"),
        ("Culvert", None, None, "each", NF, "Baseline ~$3K"),
        ("Dirt work / fill", None, None, "job", NF, "Baseline $1,800-2,500; sand $200/load; operator ~$200/hr"),
        ("Asphalt millings", None, None, "load", NF, "Baseline $650-850/load"),
        ("GC PM / permitting fee", None, None, "job", NF, "Baseline $11K"),
        ("Home: Champion Prime (DW)", 87000, 90000, "home", CALLS, "$87K + $3K trim"),
        ("Home: Clayton (DW)", 92000, 95000, "home", CALLS, ""),
    ]


def county_rows():
    """County-specific rows, in sheet order, before the shared items."""
    return {
        "St Johns": [
            ("Impact fees (county, MH = res du, 801-1,250 sf)", 13115, 13115, "du", "https://www.sjcfl.us/wp-content/uploads/2025/12/impact-fees-tables-phase-1-2026.pdf", "Phase 1 eff 3/4/2026; steps up yearly to 2030"),
            ("Impact fees (1,251-1,800 sf tier)", 17811, 17811, "du", "https://www.sjcfl.us/wp-content/uploads/2025/12/impact-fees-tables-phase-1-2026.pdf", "Most DWs land here; <800 sf = $6,907; 1,801-2,500 = $22,490"),
            ("Well (complete)", None, None, "job", NF, "No SJC-specific well cost found"),
            ("Septic install (conventional)", 4000, 9000, "job", "https://septicandwell.com/florida/st-johns/septic-installation (via " + T_WELL + ")", "Directory typical range"),
            ("Septic (mound, high water table)", 12000, 28000, "job", S_SEP_FL, "Statewide mound range"),
            ("DOH septic permit fee", None, None, "permit", NF, "DOH-St Johns still permits; fee not published online (904-506-6081)"),
            ("DOH well permit fee", None, None, "permit", NF, ""),
            ("MH building/setup permit", None, None, "permit", NF, "See https://www.sjcfl.us/wp-content/uploads/2026/05/fee-schedule.pdf (not parsed)"),
        ],
        "Clay": [
            ("Mobility fee - Middleburg/West Clay (MH)", 2150, 2150, "du", "https://www.claycountygov.com/government/office-of-management-budget/fy25-26-schedule-of-fees-services-effective-10-1-25", "FY25/26 schedule; revised 2026 schedules eff 6/15/2026 may differ"),
            ("Mobility fee - Keystone Hts/South Clay (MH)", 551, 551, "du", "https://www.claycountygov.com/government/office-of-management-budget/fy25-26-schedule-of-fees-services-effective-10-1-25", "Same caveat"),
            ("School impact fee (MH)", 8948, 8948, "du", "https://www.claycountygov.com/government/planning-and-zoning/impact-mobility-fees/school-concurrency", "Eff 6/1/2026; paid before power release"),
            ("County comprehensive impact fees", 4853.19, 4853.19, "du", "https://impactfees.org/florida-impact-fees/clay-county", "SF 1,501-2,499 sf rate after 10/1/2026; MH rate not confirmed"),
            ("Well (complete) - Clay median 200-220 ft", 6000, 16000, "job", "https://wellwaterinsider.com/well-water/florida/clay-county (via " + T_WELL + ")", "floridawelldata.com says $12-20K complete at 200 ft; baseline ~$10K"),
            ("Well - Keystone Hts avg (130 ft)", 4550, 13000, "job", "https://welldrillingcosts.com/cities/keystone-heights-fl/ (via " + T_WELL + ")", "$4,550 avg; 150 ft complete $8.5-13K; Middleburg avg $3,740"),
            ("Well permit (county/SJRWMD)", 150, 200, "permit", "https://welldrillingcosts.com/cities/keystone-heights-fl/ (via " + T_WELL + ")", "Third-party figure"),
            ("Septic install (North FL)", 5000, 15000, "job", S_SEP_FL, "Region range Duval/St Johns/Clay"),
            ("DOH septic permit fee", None, None, "permit", NF, "DOH-Clay page lists requirements, no fee"),
            ("MH building/setup permit", None, None, "permit", NF, ""),
        ],
        "Duval": [
            ("City mobility fee (consolidated, no county fee)", 900, 4080, "du", "https://impactfees.org/florida-impact-fees/duval-county/jacksonville", "Formula-based by zone; $4,080 = Zone 6 rural; SF basis"),
            ("School impact fee", None, None, "du", NF, "None found for Duval"),
            ("Well (complete)", None, None, "job", NF, ""),
            ("Septic install (North FL)", 5000, 15000, "job", S_SEP_FL, ""),
            ("DOH septic permit fee", None, None, "permit", NF, "Only 2015 sheet found: https://duval.floridahealth.gov/wp-content/uploads/sites/18/2025/04/fee-sheet-2015-ostds-web.pdf"),
            ("MH permit (single/multi-wide)", 343.20, 390, "permit", "https://www.jacksonville.gov/departments/finance/city-fees", "From search synthesis; verify; +$100 move permit"),
            ("JEA water/sewer (if on utility)", None, None, "job", "https://impactfees.org/florida-impact-fees/duval-county/jacksonville", "Sewer tap $8,330 + capacity $5,114 if sewered (not for well/septic lots)"),
        ],
        "Volusia": [
            ("Impact fees total (MH outside park, <=1,200 sf)", 13272.71, 13272.71, "du", "https://impactfees.org/florida-impact-fees/volusia-county", "2026 sched eff 6/3/2026: road 4,864+fire 485.60+EMS 57.41+dist park 527+local park 316+school 7,022.70"),
            ("Impact fees total (1,201-1,700 sf)", 13713.37, 13713.37, "du", "https://impactfees.org/florida-impact-fees/volusia-county", "road 5,097+fire 559.74+EMS 65.93+parks 606+362+school 7,022.70"),
            ("Well (complete)", None, None, "job", NF, ""),
            ("Septic install", 4000, 9000, "job", "https://septicandwell.com/florida/volusia/septic-installation (via " + T_WELL + ")", ""),
            ("DOH well permit", 80, 100, "permit", "https://volusia.floridahealth.gov/wp-content/uploads/sites/65/2026/02/2026-Fee-Increase-Chart.pdf", "Chart line is irrigation well $80 (2025)->$90->$100; potable not explicit"),
            ("DOH septic permit fee", None, None, "permit", NF, ""),
            ("MH setup permit (bldg+elec+plumb)", 201.12, 201.12, "permit", "https://permitfees.org/florida/volusia", "$100.56+$50.28+$50.28; licensed MH installer required"),
        ],
        "Putnam": [
            ("Transportation impact fee (MH)", 1768, 1768, "du", "https://impactfees.org/florida-impact-fees/putnam-county", "Ord 2025-015 eff 6/10/2025"),
            ("Other county impact fees (SF rates)", 2784, 2784, "du", "https://impactfees.org/florida-impact-fees/putnam-county", "Gov bldg 1,270+fire 921+parks 445+law 148; MH rates not confirmed; no school fee"),
            ("Well (complete) - Palatka avg", 3740, None, "job", "https://welldrillingcosts.com/cities/keystone-heights-fl/ (via " + T_WELL + ")", "Palatka avg listed on same page"),
            ("Septic install", None, None, "job", NF, "Only pumping $275-450 found"),
            ("DOH septic permit (new residential)", 475, 475, "permit", "https://main.putnam-fl.com/wp-content/uploads/2020/09/FeeScheduleFY20-21-final-adopted_ada_version.pdf", "FY20-21 ($400 state+$75 county) - stale"),
            ("MH (HUD) permit", None, None, "permit", NF, "Listed in https://www.putnam-fl.gov/wp-content/uploads/2025/09/FY-25-Fee-Schedule-Resolution-2025-118.pdf, amount not extracted"),
        ],
        "Flagler": [
            ("County impact fees (MH)", 2007, 2007, "du", "https://www.flaglercounty.gov/files/assets/county/v/1/growth-management/documents/impact-fee-schedule.pdf", "3/15/2025 schedule; SF = $3,333"),
            ("School impact fee (MH)", 2150, 2150, "du", "https://www.flaglercounty.gov/files/assets/county/v/1/growth-management/documents/impact-fee-schedule.pdf", "SF = $5,450"),
            ("Impact fee total MH / SF", 4157, 8783, "du", "https://www.flaglercounty.gov/files/assets/county/v/1/growth-management/documents/impact-fee-schedule.pdf", "Baseline ~$5K county; Flagler Estates ~$17K quote NOT explained by this schedule - ask what it includes"),
            ("Well", 3500, 4000, "job", CALLS, "$4,000 w/ permit"),
            ("Septic (mound, Bunnell) w/ permit", 12900, 15000, "job", CALLS, "Statewide mound $12-28K (" + S_SEP_FL + ")"),
            ("DOH septic/well permit fee", None, None, "permit", NF, ""),
        ],
    }


def flagler_baseline():
    """Call list, in the order it was given. Amounts are estimates."""
    return [
        {"id": "gc_permitting_pm", "line_item": "GC permitting and project management", "low": 11000, "high": 11000, "unit": "job", "display": "$11,000 flat", "notes": "Flat fee."},
        {"id": "parcel_review", "line_item": "Parcel review", "low": 500, "high": 500, "unit": "batch", "display": "about $500", "notes": "Per batch."},
        {"id": "site_visits", "line_item": "Site visits", "low": 100, "high": 100, "unit": "hour", "display": "about $100", "notes": "Per hour."},
        {"id": "home_markup", "line_item": "Home markup over wholesale", "low": 5000, "high": 5000, "unit": "home", "display": "about $5,000", "notes": "Over wholesale. Stated separately from the $7,500 wholesale fee included in the Tom Layman figure; the two were not reconciled."},
        {"id": "seller_realtor", "line_item": "Seller-side realtor", "low": 2, "high": 2, "unit": "percent", "display": "about 2%", "notes": "The calls did not state the base the percent applies to."},
        {"id": "well", "line_item": "Well", "low": 3500, "high": 4000, "unit": "job", "display": "about $3,500 ($4,000 with permit)", "notes": "High end includes the permit."},
        {"id": "septic", "line_item": "Septic with permit", "low": 14000, "high": 15000, "unit": "job", "display": "$14,000-$15,000", "notes": "With permit. The Bunnell mound range is a separate call figure."},
        {"id": "septic_bunnell_mound", "line_item": "Septic, Bunnell mound, with permit", "low": 12900, "high": 13900, "unit": "job", "display": "$12,900-$13,900", "notes": "Bunnell mound with permit. The county sheet uses a wider $12,900-$15,000 combined range."},
        {"id": "install", "line_item": "Install, including plumbing", "low": 12000, "high": 14000, "unit": "job", "display": "$12,000-$14,000", "notes": "Includes about $2,000 plumbing."},
        {"id": "electric", "line_item": "Electric", "low": 4500, "high": 4500, "unit": "job", "display": "$4,500", "notes": ""},
        {"id": "hvac", "line_item": "HVAC", "low": 6000, "high": 6000, "unit": "job", "display": "about $6,000", "notes": ""},
        {"id": "skirting", "line_item": "Skirting", "low": 1800, "high": 1800, "unit": "job", "display": "about $1,800", "notes": ""},
        {"id": "steps_each", "line_item": "Steps", "low": 800, "high": 800, "unit": "each", "display": "about $800 each", "notes": "Do not add this to the entrances total."},
        {"id": "steps_entrances", "line_item": "Steps for entrances", "low": 2400, "high": 2400, "unit": "entrances", "display": "about $2,400", "notes": "Entrances combined, about $800 each. Do not add this to the per-entrance figure."},
        {"id": "siding", "line_item": "Siding", "low": 1500, "high": 2000, "unit": "job", "display": "$1,500-$2,000", "notes": ""},
        {"id": "interior_trim", "line_item": "Interior trim", "low": 3000, "high": 3000, "unit": "job", "display": "about $3,000", "notes": ""},
        {"id": "cleaning", "line_item": "Cleaning", "low": 200, "high": 200, "unit": "job", "display": "about $200", "notes": ""},
        {"id": "clearing", "line_item": "Clearing, wooded lot, hauled", "low": 8000, "high": 8000, "unit": "job", "display": "about $8,000", "notes": "Hauled."},
        {"id": "survey", "line_item": "Survey", "low": 1000, "high": 1000, "unit": "job", "display": "about $1,000", "notes": "The calls also list an SWA trip charge of $200. They do not say whether that charge is included in the $1,000."},
        {"id": "swa_trip", "line_item": "SWA survey trip charge", "low": 200, "high": 200, "unit": "trip", "display": "$200", "notes": "Trip charge. Not stated as included in or added to the survey figure."},
        {"id": "driveway_millings", "line_item": "Driveway millings", "low": 2400, "high": 2400, "unit": "job", "display": "about $2,400", "notes": "Job figure. Per-load asphalt millings are listed separately and are not a breakdown of this total."},
        {"id": "culverts", "line_item": "Culverts", "low": 3000, "high": 3000, "unit": "each", "display": "about $3,000", "notes": "The calls did not state a count."},
        {"id": "dirt_work", "line_item": "Dirt work", "low": 1800, "high": 2500, "unit": "job", "display": "$1,800-$2,500", "notes": "Sand and operator rates are separate unit prices, not a calculated total."},
        {"id": "sand", "line_item": "Sand", "low": 200, "high": 200, "unit": "load", "display": "$200", "notes": "Per load."},
        {"id": "operator", "line_item": "Operator", "low": 200, "high": 200, "unit": "hour", "display": "about $200", "notes": "Per hour."},
        {"id": "asphalt_millings", "line_item": "Asphalt millings", "low": 650, "high": 850, "unit": "load", "display": "$650-$850", "notes": "Per load."},
        {"id": "impact_flagler_county", "line_item": "Impact fees, Flagler County", "low": 5000, "high": 5000, "unit": "dwelling", "display": "about $5,000", "notes": "Stay under 1,800 sq ft. The published manufactured-home schedule on the Flagler sheet totals $4,157 and is a different figure."},
        {"id": "impact_flagler_estates", "line_item": "Impact fees, Flagler Estates", "low": 17000, "high": 17000, "unit": "dwelling", "display": "about $17,000", "notes": "Stay under 1,800 sq ft. This call figure is not explained by the published county manufactured-home schedule."},
        {"id": "all_in_land_home", "line_item": "All-in land and home", "low": 190000, "high": 210000, "unit": "package", "display": "$190,000-$210,000", "notes": "Package estimate for land plus home. Do not add it on top of the line items. Land price is not itemized in this list."},
        {"id": "champion_prime", "line_item": "Home: Champion Prime", "low": 87000, "high": 90000, "unit": "home", "display": "about $87,000 + $3,000 trim", "notes": "Lead time about 10-12 weeks. The high end is the home plus trim, not a second home price."},
        {"id": "clayton", "line_item": "Home: Clayton", "low": 92000, "high": 95000, "unit": "home", "display": "$92,000-$95,000", "notes": "Availability cited as March 2027."},
        {"id": "tom_layman", "line_item": "Home: Tom Layman quote", "low": 87365, "high": 87365, "unit": "home", "display": "$87,365", "notes": "Includes a $7,500 wholesale fee. The fee is inside the $87,365, not added on top. Recorded as an estimate, not a current bid."},
    ]


def cell(value):
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def sheet_rows(specific):
    return [row + (FIGURE_STATUS,) for row in specific + common()]


def md_cell(value):
    return cell(value).replace("|", "\\|")


def write_markdown(path, by_county):
    lines = [
        "# County manufactured-home sub-cost estimates",
        "",
        DISCLAIMER,
        "",
        "Every row is labeled `estimate`. Shared site and finish rows are statewide or generic ranges, not a county quote. Flagler call amounts that have no published source are written up in [flagler-baseline-quotes.md](flagler-baseline-quotes.md).",
        "",
    ]
    for county, rows in by_county.items():
        lines.append(f"## {county}")
        lines.append("")
        lines.append("All figures in this table are estimates.")
        lines.append("")
        lines.append("| " + " | ".join(HEADERS) + " |")
        lines.append("|" + "---|" * len(HEADERS))
        for row in rows:
            lines.append("| " + " | ".join(md_cell(value) for value in row) + " |")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_baseline_markdown(path, rows):
    lines = [
        "# Flagler baseline quote list",
        "",
        "Every figure below is an **estimate** from the user's Flagler calls. These are not bids, contracts, or quotes for a specific parcel. Fee schedules and contractor prices change; confirm the current amount before using it.",
        "",
        "Recorded in this repo on 2026-11-04. The calls did not include dates.",
        "",
        "The all-in land-and-home range is a package estimate. Do not add it on top of the line items, and do not treat a blank on the county sheets as zero.",
        "",
        "Published fee research for Flagler, St. Johns, Clay, Duval, Volusia, and Putnam is in [county_sub_costs.md](county_sub_costs.md). The same rows are in [county_sub_costs.csv](county_sub_costs.csv), [county_sub_costs.json](county_sub_costs.json), and [county_sub_costs.xlsx](county_sub_costs.xlsx).",
        "",
        "## Call estimates",
        "",
        "All figures in this table are estimates.",
        "",
        "| Line item | Estimate | Unit | Figure status | Notes |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row["line_item"]),
                    md_cell(row["display"]),
                    md_cell(row["unit"]),
                    FIGURE_STATUS,
                    md_cell(row["notes"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## How this sits next to the county sheets",
            "",
            "The Flagler county sheet records the 3/15/2025 published schedule: manufactured-home county impact fees $2,007, school impact fees $2,150, and a combined manufactured-home total of $4,157. Single-family on that schedule is $8,783. The calls estimated about $5,000 for Flagler County and about $17,000 for Flagler Estates, and said to stay under 1,800 sq ft. The Estates figure is not explained by that schedule. Keep the call estimates and the schedule figures separate until someone confirms what the Estates number includes. All of these amounts are estimates or published schedule figures as labeled on the sheet; none of them is a current bill.",
            "",
            "Several call figures are only notes on the county sheets, because no published source was found for them. This list is where those call amounts are recorded as numbers, including GC permitting and project management, parcel review, site visits, home markup, the seller-side realtor percent, survey, clearing, culverts, dirt work, sand, operator time, asphalt millings per load, siding, interior trim, cleaning, and the package all-in.",
            "",
            "The workbook Summary sheet also has a Flagler site-plus-home rollup that excludes the land purchase price. That rollup is not the $190,000-$210,000 land-and-home package estimate.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def record(county, row):
    line_item, low, high, unit, source, notes, status = row
    return {
        "county": county,
        "line_item": line_item,
        "low": low,
        "high": high,
        "unit": unit,
        "source": source,
        "notes": notes,
        "figure_status": status,
    }


def write_json(path, by_county, baseline):
    payload = {
        "schema_version": 1,
        "figure_status": FIGURE_STATUS,
        "disclaimer": DISCLAIMER,
        "recorded": "2026-11-04",
        "counties": list(by_county),
        "line_items": [record(county, row) for county, rows in by_county.items() for row in rows],
        "flagler_baseline": [
            {
                **row,
                "source": CALLS,
                "figure_status": FIGURE_STATUS,
            }
            for row in baseline
        ],
    }
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def write_csv(path, by_county):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["County"] + HEADERS)
        for county, rows in by_county.items():
            for row in rows:
                writer.writerow([county] + [cell(value) for value in row])


def write_workbook(path, by_county):
    workbook = Workbook()
    workbook.remove(workbook.active)
    for county, rows in by_county.items():
        sheet = workbook.create_sheet(county)
        sheet.append(HEADERS)
        for row in rows:
            sheet.append(list(row))
        for header_cell in sheet[1]:
            header_cell.font = Font(bold=True)
        for column, width in zip("ABCDEFG", [44, 12, 12, 12, 70, 70, 16]):
            sheet.column_dimensions[column].width = width

    summary = workbook.create_sheet("Summary", 0)
    counties = list(by_county)
    # Clay low = Keystone mobility $551 + school $8,948 + comprehensive $4,853.19.
    # Clay high uses Middleburg mobility $2,150 instead of $551.
    clay_low = 551 + 8948 + 4853.19
    clay_high = 2150 + 8948 + 4853.19
    items = [
        (
            "Impact/mobility fees (MH)",
            {
                "St Johns": (13115, 17811),
                "Clay": (clay_low, clay_high),
                "Duval": (900, 4080),
                "Volusia": (13272.71, 13713.37),
                "Putnam": (1768, 1768 + 2784),
                "Flagler": (4157, 4157),
            },
        ),
        (
            "Well",
            {
                "St Johns": (None, None),
                "Clay": (4550, 16000),
                "Duval": (None, None),
                "Volusia": (None, None),
                "Putnam": (3740, None),
                "Flagler": (3500, 4000),
            },
        ),
        (
            "Septic",
            {
                "St Johns": (4000, 28000),
                "Clay": (5000, 15000),
                "Duval": (5000, 15000),
                "Volusia": (4000, 9000),
                "Putnam": (None, None),
                "Flagler": (12900, 15000),
            },
        ),
    ]
    generic_low = 7000 + 4000 + 4000 + 1200 + 500 + 1000 + 3000
    generic_high = 20000 + 10000 + 9000 + 3500 + 2000 + 10000 + 8000
    summary.append(["Item"] + [f"{county} Low" if index % 2 == 0 else f"{county} High" for county in counties for index in range(2)])
    for name, values in items:
        summary.append([name] + [amount for county in counties for amount in values[county]])
    summary.append(
        ["Generic site/finish (install, delivery, HVAC, skirting, steps, clearing, driveway) - same all counties"]
        + [generic_low if index % 2 == 0 else generic_high for county in counties for index in range(2)]
    )
    summary.append(["Home (Champion Prime $87K+$3K trim ... Clayton $95K)"] + [90000 if index % 2 == 0 else 95000 for county in counties for index in range(2)])
    last_data_row = summary.max_row
    all_in = ["ALL-IN (sum of above; blanks treated as 0 -> understated)"]
    for column_index in range(2, 2 + 2 * len(counties)):
        letter = get_column_letter(column_index)
        all_in.append(f"=SUM({letter}2:{letter}{last_data_row})")
    summary.append(all_in)
    summary.append(
        [
            "Flagler user-baseline all-in (mid): well 4K+septic 14K+install 13K+elec 4.5K+HVAC 6K+skirt 1.8K+steps 2.4K+siding 1.75K+trim 3K+clean .2K+clear 8K+survey 1K+drive 2.4K+culvert 3K+dirt 2.2K+impact 5K+GC 11K+home 90K",
            "=4000+14000+13000+4500+6000+1800+2400+1750+3000+200+8000+1000+2400+3000+2200+5000+11000+90000",
        ]
    )
    summary.append(
        [
            "Note: impact-fee Clay low = Keystone mobility $551 + school $8,948 + comprehensive $4,853 (SF rate); high uses Middleburg $2,150. Generic items sourced from statewide guides - see county sheets."
        ]
    )
    summary.append(["All figures on every sheet are estimates, not bids, contracts, or parcel-specific quotes. Blanks are unknown, not zero. This Summary rollup is not the Flagler $190,000-$210,000 land-and-home package estimate."])
    for header_cell in summary[1]:
        header_cell.font = Font(bold=True)
    summary.column_dimensions["A"].width = 60
    workbook.save(path)


def check(by_county, baseline):
    expected = {"St Johns": 28, "Clay": 30, "Duval": 27, "Volusia": 27, "Putnam": 26, "Flagler": 26}
    if list(by_county) != list(expected):
        raise SystemExit("county order changed")
    for county, count in expected.items():
        rows = by_county[county]
        if len(rows) != count:
            raise SystemExit(f"{county} has {len(rows)} rows, expected {count}")
        if any(row[-1] != FIGURE_STATUS for row in rows):
            raise SystemExit(f"{county} has a figure that is not labeled estimate")
    required = {
        "gc_permitting_pm": 11000,
        "parcel_review": 500,
        "site_visits": 100,
        "home_markup": 5000,
        "seller_realtor": 2,
        "well": 3500,
        "septic": 14000,
        "septic_bunnell_mound": 12900,
        "install": 12000,
        "electric": 4500,
        "hvac": 6000,
        "skirting": 1800,
        "steps_each": 800,
        "steps_entrances": 2400,
        "siding": 1500,
        "interior_trim": 3000,
        "cleaning": 200,
        "clearing": 8000,
        "survey": 1000,
        "swa_trip": 200,
        "driveway_millings": 2400,
        "culverts": 3000,
        "dirt_work": 1800,
        "sand": 200,
        "operator": 200,
        "asphalt_millings": 650,
        "impact_flagler_county": 5000,
        "impact_flagler_estates": 17000,
        "all_in_land_home": 190000,
        "champion_prime": 87000,
        "clayton": 92000,
        "tom_layman": 87365,
    }
    found = {row["id"]: row for row in baseline}
    if set(found) != set(required):
        raise SystemExit("baseline ids do not match the call list")
    for key, low in required.items():
        if found[key]["low"] != low or found[key]["figure_status"] != FIGURE_STATUS:
            raise SystemExit(f"baseline {key} is missing its estimate")
    highs = {
        "well": 4000,
        "septic": 15000,
        "septic_bunnell_mound": 13900,
        "install": 14000,
        "siding": 2000,
        "dirt_work": 2500,
        "asphalt_millings": 850,
        "all_in_land_home": 210000,
        "champion_prime": 90000,
        "clayton": 95000,
    }
    for key, high in highs.items():
        if found[key]["high"] != high:
            raise SystemExit(f"baseline {key} high end changed")


def main():
    by_county = {county: sheet_rows(rows) for county, rows in county_rows().items()}
    baseline = [{**row, "figure_status": FIGURE_STATUS, "source": CALLS} for row in flagler_baseline()]
    check(by_county, baseline)
    write_workbook(OUT / "county_sub_costs.xlsx", by_county)
    write_csv(OUT / "county_sub_costs.csv", by_county)
    write_markdown(OUT / "county_sub_costs.md", by_county)
    write_json(OUT / "county_sub_costs.json", by_county, baseline)
    write_baseline_markdown(OUT / "flagler-baseline-quotes.md", baseline)
    print(f"wrote {sum(len(rows) for rows in by_county.values())} county rows and {len(baseline)} baseline estimates")


if __name__ == "__main__":
    main()

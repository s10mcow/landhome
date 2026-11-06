# CutSheetRX elevation and drainage screen

Optional desktop check before a vacant lot is called buildable, and before home, pad, well, septic, or driveway placement is frozen. Use it for Rising Tide and Requity land-home lots, including Flagler. It reads public lidar for the parcel in front of you. It is not a farm-field grading product, and it does not replace Flagler permit sources.

Checked against the public page on 2026-11-06. Labels move. Read the controls on the page you opened, and record those labels.

## What the page is

[CutSheetRX](https://www.senterfarms.com/programs/csrx) is a free public web page by Travis Senter (Senter Farms). No account, API key, or paid endpoint.

The page's own help states the data:

- Lidar: [USGS 3DEP](https://apps.nationalmap.gov/3depdem/) bare earth, about 1 m. The flight date is shown at the bottom right once the map is zoomed to the site.
- Imagery: Esri. The map credit line also names Maxar and Earthstar Geographics.
- Figures are estimates. The page tells you to check the flight date and verify with a survey before quoting.

On the 2026-11-06 public page the tools are: hover elevation, an elevation profile (length, start, end, fall or rise, slope percent, low/high), a drawn area with an elevation range and relief, a Drainage view, and a Cut/Fill view.

Drainage draws flow lines that thicken as more acres drain through them, marks standing water 0.1 ft or deeper, and marks outlets. The status line reports outlet count and either standing-water acres and cubic yards, or no standing water. Detail changes which lines draw: Fine 0.25 acre, Normal 1 acre, Main only 5 acres.

Cut/Fill reports cut and fill in yd³, cut per acre, max cut and max fill in feet, and live cut or fill depth under the cursor against the design surface. Field contours are 0.10, 0.20, 0.25, 0.50, or 1.00 ft, separate from the map's 2 ft and 5 ft USGS rendering presets. Existing and design contours can be shown together.

The Nov 5, 2026 demo also shows a 3D view with a rain control and a readout of deepest depth, water still on the field, and water that ran off. That control was not in the public HTML fetched on 2026-11-06. If the page you opened has it, run it and record it. If it does not, the Drainage view is the drainage evidence. A missing 3D button is not missing lidar. Do not open a downloaded or local copy of the page, and do not call elevation servers yourself to rebuild the screen.

The [USGS 3DEP viewer](https://apps.nationalmap.gov/3depdem/) linked from the help text can confirm whether lidar exists. It does not compute pad cut/fill or standing water. Use it only when the CutSheetRX page cannot answer a coverage question.

## When to run it

Run this screen when any of these are still open:

- A vacant lot, or a lot with no finished pad, before anyone calls it buildable.
- Placement of the manufactured-home pad, well, septic reservation, driveway, or delivery path.
- A grading, standing-water, or "how much dirt" question during due diligence, including before survey elevations come back.
- The preferred layout sits in an obvious swale, or the lot looks flat enough that a closed low would not show in imagery.

Skip it only when the request is sourced lot dimensions alone and no buildability or placement decision is being made. Say that the screen was not run.

Order of work: resolve the parcel from official GIS or the appraiser first, as the site-plan skill requires. Then open CutSheetRX on that same parcel. Imagery does not establish elevation, soils, seasonal high water, or flood zone. This screen is the elevation and surface-drainage evidence imagery cannot provide. It still does not establish soils, seasonal high water, or flood zone.

## How to use the public page

1. Open `https://www.senterfarms.com/programs/csrx`. Use the Go box (address or latitude, longitude). Confirm the view is the intended lot by road and the official parcel shape. A search hit is not parcel identity.
2. Zoom in until the bottom-right flight line appears. Record it exactly, including the quality label when shown (`Lidar flown …`). Below a zoomed-out view the date hides; a blank date at county scale is not "no coverage." `No USGS lidar flight here` after zooming in means this check has no source.
3. Turn the Lidar slider up or switch Rendering to a color-elevation mode when you need to see relief. Relief sliders, sun angle, and height stretch change the picture only.
4. Ignore the color-range Low/High until you have fit them to this parcel. The page can open with starter numbers that are not the site. Record the field summary after the area is drawn, plus spot elevations from hover, rather than those starters.
5. Draw an elevation profile along the question you are answering: road to rear, along the proposed driveway, or across the pad. Finish the line the way the page says (double-click or Done). Record length, start, end, fall or rise, slope percent, and low/high.
6. Draw the area you mean and name it: whole lot, pad, or driveway corridor. Keep the outline inside the lot unless you are deliberately looking at offsite water, and say which. Drawn acres stay separate from `legal_acreage`, GIS acreage, and any listing size. Eye-balled corners are not boundary corners.
7. Open Drainage. Leave Detail at Normal unless you record why you changed it. Record the status sentence. Note where standing water and outlets sit relative to the pad, septic reservation, well, and driveway.
8. If a 3D or Start rain control is on the page, run it on that same outline. Record existing versus design surface, the rain rate and storm length shown, playback only as a viewing setting, and the readout's deepest depth and on-field versus ran-off volumes. Height stretch is display exaggeration. The rate you leave on screen is a screen assumption, not a county design storm. Record where water pools relative to the pad and the septic reservation.
9. Open Cut/Fill only for a dirt question. The page starts a field grade near 0.10% slope, heading 180° (south), and a cut:fill ratio of 1.20 (extra cut for shrink), and Best fit solves that grade. Those starters are not a manufactured-home pad specification and not a Flagler standard. For a screening number, record the slope, heading, ratio, and whether Best fit or a hand-entered grade produced the yards. For a pad question, draw the pad, set slope and heading only from an explicit assumption, and label that assumption.
10. Hover the design for the live cut or fill depth. That depth is versus the design surface, not standing-water depth.
11. PDF and CSV exports are optional project notes. Keep them with the project record, outside this repository. The export repeats the page's caveat: bare-earth lidar, the ground may have changed since the flight, verify with a survey before quoting.

If the page shows `No lidar inside this area`, `No lidar along this line`, or `No USGS lidar flight here` on the zoomed parcel, stop. Leave elevation and surface drainage from this check unknown. Do not enter zero, and do not describe the lot as flat.

## What to record

Leave any item null when that tool was not used. Do not store zero for "not run."

- Page URL, the date of the check, and the person or agent run.
- Flight line from the bottom right: date range and quality label if shown. If the line is missing, say whether the map was zoomed in.
- Which outline was drawn (lot, pad, or corridor) and the acres the page reports for it.
- Displayed elevation range and relief from the field summary, and any spot elevation you actually hovered, with what the spot is (pad corner, road edge, low point).
- Profile, if drawn: what the line follows, length, start, end, fall or rise, slope percent, low/high.
- Drainage, if run: Detail setting, the status sentence (outlets, standing-water acres and yd³, or no standing water), and where water sits relative to the improvements. If the page shows a max or deepest pool depth, record that number and its unit. Do not invent a depth from the color.
- Rain view, if that control was present: surface (existing or design), rain rate, storm length, deepest pool depth, on-field and ran-off amounts, and where it pooled. Omit this block when the control is absent.
- Cut/Fill, if run: contour interval, existing and design contours on or off, slope percent, heading, cut:fill ratio, Best fit or manual, cut yd³, fill yd³, max cut / max fill feet, and the cell size when the page states it (`lidar on N ft cells`).
- One line that the figures are approximate USGS 3DEP lidar estimates, not a survey.

Map rendering (shaded relief, slope, 2 ft or 5 ft USGS contours) is a picture setting. Record it only when you relied on that picture. The field contour interval is the number that belongs with cut/fill.

## How it changes the layout and the purchase screen

Use the result as a constraint note on the proposed plan, not as contours traced onto the sheet. The sheet stays on the official parcel polygon. Label the note approximate and preliminary.

- Standing water, a closed low, or a profile that falls toward the pad, septic reservation, well, or driveway: move the concept, or leave that placement unresolved. Do not keep the Laurel-style arrangement when this screen puts those features in the low spot. Mirroring is allowed when the other side is the higher ground; say so.
- No standing water and a gentle fall toward a definite outlet: the concept can continue. Flood zone, septic soils, seasonal water, and surveyed elevations stay open.
- A large max cut or max fill, or a steep profile on the delivery path, is a due-diligence cost and access flag. It is not a sitework quantity for a bid, a culvert size, or a finished-floor elevation.
- Water leaving across a neighbor, or a draw that continues off the outline, stays unresolved until someone looks past the line you drew.
- Purchase, extension, or exit stays with the Requity decision. This screen is one piece of evidence. It does not waive a notice deadline or declare the lot a go.

Put the same facts in the scheduling review when survey elevations are not back yet. Survey, septic evaluation, and the coordinated layout still have to happen. A boundary-only survey does not retire this gap, and this screen does not retire the survey.

## What it must not decide

- Not a boundary, easement, or right-of-way survey. Not the acreage to print as the lot size.
- Not a septic design, soil log, seasonal high water table, or well setback.
- Not a flood zone, base flood elevation, or finished floor. Check those on the official flood and permitting sources when compliance is in question.
- Not a sealed grading plan, cut sheet for construction, or pipe size. Flagler's ROW and culvert requirements stay on the county packet.
- Not proof the lot perc's, drains after a storm, or stays dry in a hurricane. Lidar is a bare-earth surface from the flight date. Fill, ditches, and clearing since that flight are invisible until someone checks the ground.
- Missing lidar stays unknown. Do not borrow a nearby field, a demo property, or the page's starter elevation numbers.

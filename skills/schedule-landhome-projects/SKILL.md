---
name: schedule-landhome-projects
description: Plan and review Rising Tide and Requity manufactured-home land-home schedules from land contract through GC completion and occupancy. Use for scheduling efficiency, parallel preconstruction, ready-now work, blocked tasks, two-week trade plans, completion forecasts, portfolio crew conflicts, scheduling flowcharts, or application-portal scheduling requirements. Keep this workflow specific to land-home packages.
---

# Schedule land-home projects

Turn a contract or current project record into an evidence-based schedule. Identify work that can advance together, explain each hold, and distinguish GC subcontractor scope completion from occupancy approval.

## 1. Establish the project and evidence

- Retrieve available project records, checklists, permit documents, current site-plan revision, home information and crew commitments before asking for information already connected. Discover current tools; do not assume a particular tracker exists. Read records by default; only change project records when the user requests it.
- Record the as-of date and project timezone. Capture the parcel and actual governing jurisdiction, contract and DD notice deadlines, seller access, DD spending authorization, planned closing, home source/model/bedrooms, utility route, project roles and scope of GC completion.
- Distinguish a contractual deadline, internal target, provider estimate, confirmed appointment and actual event. Record the evidence source and observation date. Preserve conflicts rather than silently choosing a convenient checklist value.
- Treat unknown inputs as unknown. Ask only for information needed for the next decision; continue independent preparation. Do not assume Flagler jurisdiction from a Bunnell mailing address, a standard DD window, a stocked home or a fixed permit duration.
- Read [workflow.md](references/workflow.md) for operating phases and release checks. For local permit dependencies, read [flagler-sources.md](references/flagler-sources.md), verify current primary sources and parcel applicability, and record what remains unconfirmed.

## 2. Build the dependency network

- Launch authorized survey, septic evaluation, home information, utility planning and trade pricing at contract acceptance. Model parallel work with shared prerequisites, not a serial checklist.
- Coordinate survey, home/pad elevations, drainage, access, well and septic on one dated layout. Obtain site-plan measurements through the separate `lot-to-proposed-site-plan` workflow when available. Never treat GIS measurements or a generic concept as an approved permit plan.
- While survey elevations are still out, a CutSheetRX lidar screen from that site-plan workflow can show standing water and rough pad dirt. Follow its note. Keep yardage and depths labeled approximate. They do not stand in for surveyed pad elevations, a flood determination, or a drainage design, and they do not decide the purchase.
- Include only applicable tasks: private well versus public water, septic versus sewer, stocked versus factory home, jurisdiction-specific documents and required inspection stages. Use `required`, `not_applicable` with evidence, or `undetermined`; an unchecked box is not proof of applicability.
- Separate document preparation, signatures, submission, accepted-for-review, corrections, issuance, installation, inspection and final clearance. Require the relevant event, not merely an uploaded file.
- Validate all predecessor IDs, conditions and cycles. Keep a blocker attached to its affected branch; allow unrelated work to proceed. Add home availability and shared crew capacity alongside physical and approval dependencies.
- Review the well, septic and delivery sequence for equipment access. Preserve a path for later septic installation and well servicing; do not hardcode every well or drainfield before or after home delivery.

## 3. Evaluate readiness and forecast

- Return `ready`, `blocked`, `undetermined`, `in_progress`, `waiting_external`, `complete`, or `not_applicable` with reasons. A future target date is not evidence that a prerequisite is complete. Identify the accountable owner or flag that assignment is missing.
- Check purchase, filing, sitework, delivery and handover separately. Do not waive a statutory or permit requirement through a portal override. Keep authorized DD access distinct from permission to start construction.
- Give every hold an unmet requirement, accountable owner, next action and follow-up date or explicit missing follow-up. Identify stale documents, expiration, corrections and plan-revision conflicts.
- Forecast separate milestones: packet ready, required permits issued, sitework ready, home set, GC subcontractor scope complete, occupancy/CO, and sale close only if in scope. Tie GC completion to the agreed subcontractor scope; do not silently make it dependent on CO.
- For each branch use remaining work, provider lead-time windows, working calendars and crew availability. Join parallel branches at the latest prerequisite, then add dependent duration. Never add parallel durations together or reuse an elapsed full duration after work has started.
- Show a provisional earliest/expected window only where its assumptions are supportable. Keep unknown timing visible; identify the input needed to bound a forecast. Do not turn a missing duration into zero or an open-ended wait into a promised latest date.
- Recompute affected downstream forecasts after a predecessor or layout change. Show the controlling sequence and main uncertainty. Check shared crews across projects before calling appointments confirmed; use a manual availability calendar until reliable capacity data exists.

## 4. Deliver the useful view

Default to a concise project assessment containing:

1. The next decision and the milestone currently at risk.
2. A ready-now / approaching readiness / blocked table with task, owner, prerequisite or evidence, next action and date type.
3. Separate GC and occupancy forecasts with assumptions and the controlling wait; use “not yet bounded” when necessary.
4. A rolling two-week plan distinguishing conditional holds from confirmed bookings.
5. Missing evidence and contradictions that materially change release or timing.

Adapt to the request. For a high-level picture, use [flowchart.md](references/flowchart.md) and replace conditional branches with the property's actual route. For portal design or code review, read [portal-contract.md](references/portal-contract.md); inspect the actual code or PR before claiming implementation. For a portfolio, add shared-crew conflicts and prioritize DD decisions by actual notice deadlines.

Track contract-to-packet, accepted-submission-to-issuance, permit-to-set, set-to-GC-completion and GC-completion-to-CO as separate intervals. Separate active work, external wait, corrections and crew queues. Treat the first two projects as handoff pilots, not reliable duration averages.

Save requested planning artifacts using available supported storage. Keep private project records and generated schedules outside the public skill source. Do not spend money, file permits, order homes, dispatch crews, send messages, change live records, or establish recurring monitoring solely because this skill was invoked; perform such actions only within the user's specific authorization and available tools.

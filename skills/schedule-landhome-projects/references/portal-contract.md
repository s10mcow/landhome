# Scheduling portal contract

Use these semantics to design or review a portal. Map them to its actual schema/tools; do not claim these fields, integrations or automatic behaviors already exist.

## Minimum records

| Record | Fields / behavior |
| --- | --- |
| Project | ID, parcel, jurisdiction, timezone, as-of, DD/notice deadlines, closing, access/spending authority, home and utility routes, PM, contractual GC scope |
| Task | Unique ID, project, phase, applicability/evidence, owner, predecessors, work/approval type, observed state, next action |
| Evidence | Source/document ID, parcel, issuer/party, observed time, relevant event, layout revision, expiration if relevant |
| Hold | Affected task, unmet requirement, owner, waiting party/category, submitted time, next follow-up, response window or unknown |
| Timing | Remaining duration window, calendar, source/time, target versus estimate versus commitment versus actual |
| Resource | Trade/crew, availability, commitments, capacity, reservation state and cross-project conflicts |
| Milestone | Packet, permits, sitework, set, GC completion, CO; forecast window, controlling prerequisites and assumptions |
| Layout revision | ID/date, approval/use status, changed elements, affected permits/quotes/trades needing review |

Keep raw evidence and computed readiness separate. Preserve submitted, issued and actual dates when forecasts change. Audit corrections, changed prerequisites and documented operational decisions.

## Readiness

1. Resolve applicability. `undetermined` is not a shortcut to `not_applicable`; record evidence for exclusions.
2. Verify predecessor IDs and absence of cycles. A missing predecessor is unresolved, not completed.
3. Evaluate required events against current evidence, correct parcel, validity and layout revision. Separate draft / signed / submitted / accepted / correction required / issued / final states. A signed document can be on file while its permit is under review.
4. Explain immediate blockers and upstream causes while unrelated branches proceed. Distinguish future scheduling constraints from legal/physical readiness and missing assignment.
5. Reconcile disputed completion. An unchecked tracker entry does not prove no field work occurred; an upload does not prove issuance. Identify evidence needed to resolve the conflict.
6. Record operational overrides with who/why/when and authority. A checkbox cannot waive laws, permit conditions or unknown applicability.

## Forecasts

Use a dependency network rather than checklist percentage or a generic total duration. Compute in project timezone and declare working-day calendars/holiday treatment.

Determine each task's earliest supported start from the latest required predecessor finish, its own earliest availability, external commitments and resource availability. Add the remaining supported duration window using that task's calendar. Propagate changes through affected successors, then reconsider shared-resource conflicts elsewhere.

Synthetic example: survey input on day 6, soils on day 8 and home information on day 3 can make layout inputs ready on day 8. Add layout work itself; do not claim layout completion on day 8 or sum 6 + 8 + 3. These are not vendor lead-time defaults.

If controlling timing is unknown, show the milestone unbounded or conditional on an explicit scenario. Avoid invented numerical confidence. Contractual deadlines stay fixed when forecasts move. Mark confirmed appointments at risk or needing reconfirmation when prerequisites slip.

Keep milestone definitions visible. GC completion is the agreed subcontractor scope/evidence; CO is agency occupancy approval; sale close is a commercial event. Do not assume equal dates or force an order unsupported by actual scope.

## Initial screens and acceptance

Start with intake, an evidence-backed ready/blocked list, milestone forecasts and a two-week board. Show hold owner, action and follow-up. A manual crew calendar is sufficient initially; add optimization after capacity data exists.

Use these behavioral cases to review actual implementation:

- Delivery stays blocked/undetermined while required pad/access/installer prerequisites are unmet/unknown, even if its target date arrives.
- A signed uploaded installer document does not become an issued permit. Submission does not require prior review of that same packet.
- A verified private-well route excludes public water-meter tasks with a reason; an unknown route leaves applicability unresolved.
- Septic approval delay moves dependent packet/permit milestones while unrelated home/utility planning continues.
- Expired permits and superseded layouts trigger evidence review; approval never transfers silently to a changed drawing.
- A shared crew cannot have conflicting confirmed reservations; conditional holds stay labeled.
- Unknown durations never become zero. Parallel branches use the latest predecessor plus successor work.
- GC completion can be recorded while utility/agency closeout prevents occupancy when actual contract scope supports it.
- Every blocked task has a reason/action; missing owner or follow-up remains visible.
- Preserve and escalate DD notice deadlines when essential evidence is late.

Measure accepted-review time separately from preparation and corrections. Track remobilizations, missed set appointments, crew waits and milestone forecast error alongside total elapsed time.

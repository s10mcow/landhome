# Landhome on Hermes

This runbook is for an optional **internal** read-only pilot on the Mac mini that already hosts Hermes. Use it for a project whose records live in Build Tracker. First inventory the existing Hermes setup and reuse the profile and skills where they already serve the same purpose.

## Internal pilot setup

On the Mac mini, check out this repository. Create a dedicated internal profile if one has yet to be set up for this pilot.

```sh
hermes profile create landhome --no-skills
```

If the profile exists, reuse it. Configure model access for the profile as needed with `hermes -p landhome setup`. Open the profile's configuration with `hermes -p landhome config edit`. Merge the following keys into its YAML and replace the example path with the absolute path to the checkout's `skills` directory.

```yaml
skills:
  external_dirs:
    - /absolute/path/to/landhome/skills

mcp_servers:
  build_tracker:
    command: npx
    args: ["-y", "build-tracker-mcp"]
    env:
      MCP_API_KEY: "${LANDHOME_BUILD_TRACKER_API_KEY}"
    tools:
      include:
        - get_property
        - get_checklist
        - get_build_tasks
        - get_inspections
        - list_attachments
        - whats_next
      resources: false
      prompts: false
```

Use the Build Tracker org API key from **Settings → API Keys**. Set `LANDHOME_BUILD_TRACKER_API_KEY` in the profile's secret environment (normally `~/.hermes/profiles/landhome/.env`). Use the project's authorized organization key and keep it in the local secret environment. The YAML limits which tools Hermes can see. The permissions of the underlying org key are a separate control. Keep this configuration and the org key internal.

## Run the first project

Set `landhome_pilot_property` locally to the exact name of an authorized pilot property in Build Tracker.

```sh
hermes -p landhome skills list --enabled-only
hermes -p landhome mcp test build_tracker
hermes -p landhome chat --oneshot -s schedule-landhome-projects -q \
  "Use Build Tracker to review ${landhome_pilot_property:?Set the exact Build Tracker property name first}. Give me ready work, blockers, owners, next follow-up dates, separate GC completion and CO forecasts, and any vendor follow-up drafts. Use only the tracker read tools. Report missing or conflicting evidence. Return all drafts here."
```

Confirm that the skill appears, the MCP connection succeeds, and the project run reads the correct lot. Compare the resulting readiness and forecasts against the project record. Verify that the profile exposes only the allowed Build Tracker tools and has no vendor messaging channel attached during the pilot.

## Client Slack and portal

The operating plan uses Trello for execution, the existing client Slack workspace for collaboration, and a portal that displays approved project status. Before integration, map where task status, approvals, and documents already live. Assign each fact a single owner and keep the client view derived from approved records.

Use a separately isolated Hermes runtime for client Slack access, with dedicated credentials and access to an approved, project-scoped dataset. The internal profile and its Build Tracker org key are for internal use. Begin with read-only answers and reviewed drafts. Validate that an authorized client can read its own published information and that another client cannot retrieve it through Slack, the portal, or document links.

## Move from internal briefing to coordination

| Stage | Trigger | Hermes responsibility | Build Tracker responsibility |
|---|---|---|---|
| Pilot | Manual run against one Flagler lot | Read tasks, explain blockers and draft follow-ups | Supply the source records |
| Scheduled review | Hermes cron on the Mac mini after the pilot | Check overdue responses and due diligence risks and surface exceptions | Store deadlines, owners, follow-up timestamps and disposition |
| Contract kickoff | Authenticated portal event after the contract transition is committed | Apply the scheduling and site-plan workflows, prepare requests and route exceptions | Verify access, vendor authorization and spending caps before action. Save evidence, approvals and a stable action ID so retries are safe |
| Trade and closeout handoffs | Verified vendor or agency update | Extract dates, identify impacted work and draft the next follow-up | Verify required evidence and permit states, confirm bookings, and track GC completion and CO independently |

Build Tracker already queues lot enrichment on eligible property transitions and prepares a surveyor draft when eligible lots leave due diligence. Reuse those paths. For contract-day survey outreach, move the existing draft trigger earlier after seller access and spending authorization are verified, and retain the approval step. For the Hermes contract trigger, send a signed webhook with an event ID and project ID. Keep vendor content in the portal or inbox as evidence. The portal should separately record conditional holds and confirmed bookings. Requity decides whether to close, extend, or exit. Rising Tide authorizes sitework and home dispatch. Vendor outreach can be enabled once an approved sender, vendor list, and per-project authorization rules are in place. The portal must check those rules when an action runs.

Start cron only after the manual run works and the Landhome profile has a running gateway. Start with a review job in America/New_York. Enable event-driven kickoff after the authoritative system can publish committed events and record actions without duplicates. If Trello owns execution for the pilot, map its tasks and statuses before enabling any automatic updates.

- [Scheduling skill](../skills/schedule-landhome-projects/SKILL.md)
- [Lot-to-site-plan skill](../SKILL.md)
- [Build Tracker MCP setup](https://github.com/s10mcow/build-tracker#mcp-setup)
- [Build Tracker due diligence and survey outreach](https://github.com/s10mcow/build-tracker/blob/main/docs/DUE_DILIGENCE_ENRICHMENT.md)
- [Hermes profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- [Hermes MCP configuration](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference)
- [Hermes cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
- [Hermes webhook signing](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks#security)

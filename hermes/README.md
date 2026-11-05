# Landhome on Hermes

Run the Requity Landhome workflow on the Mac mini that hosts Hermes. The first run reads Build Tracker and produces a project briefing and vendor-message drafts. Build Tracker remains the source of record for project state, scheduling decisions, and approvals.

## Set up the pilot

On the Mac mini, check out this repository and create a dedicated profile:

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

Use the Build Tracker org API key from **Settings → API Keys**. Set `LANDHOME_BUILD_TRACKER_API_KEY` in the profile's secret environment (normally `~/.hermes/profiles/landhome/.env`). Use the project's authorized organization key. The YAML limits the tools Hermes can see. The permissions of the underlying org key are a separate control. Use a profile dedicated to this work and keep the key in its local secret environment.

## Run the first project

```sh
hermes -p landhome skills list --enabled-only
hermes -p landhome mcp test build_tracker
hermes -p landhome chat --oneshot -s schedule-landhome-projects -q \
  'Use Build Tracker to review 1573 Laurel. Give me ready work, blockers, owners, next follow-up dates, separate GC completion and CO forecasts, and any vendor follow-up drafts. Use only the tracker read tools. Report missing or conflicting evidence. Return all drafts here.'
```

Confirm that the skill appears, the MCP connection succeeds, and the project run reads the correct lot. Compare the resulting readiness and forecasts against the project record. Verify that the profile exposes only the allowed Build Tracker tools and has no vendor messaging channel attached during the pilot.

## Move from briefing to coordination

| Stage | Trigger | Hermes responsibility | Build Tracker responsibility |
|---|---|---|---|
| Pilot | Manual run against one Flagler lot | Read tasks, explain blockers and draft follow-ups | Supply the source records |
| Scheduled review | Hermes cron on the Mac mini after the pilot | Check overdue responses and due diligence risks and surface exceptions | Store deadlines, owners, follow-up timestamps and disposition |
| Contract kickoff | Authenticated portal event after the contract transition is committed | Apply the scheduling and site-plan workflows, prepare requests and route exceptions | Verify access, vendor authorization and spending caps before action. Save evidence, approvals and a stable action ID so retries are safe |
| Trade and closeout handoffs | Verified vendor or agency update | Extract dates, identify impacted work and draft the next follow-up | Verify required evidence and permit states, confirm bookings, and track GC completion and CO independently |

For the contract trigger, send a signed Hermes webhook with an event ID and project ID. Keep vendor content in the portal or inbox as evidence. The portal should separately record conditional holds and confirmed bookings. Requity decides whether to close, extend, or exit. Rising Tide authorizes sitework and home dispatch. Vendor outreach can be enabled once an approved sender, vendor list, and per-project authorization rules are in place. The portal must check those rules when an action runs.

Start cron only after the manual run works and the Landhome profile has a running gateway. Start with a review job in America/New_York. Enable event-driven kickoff after the tracker can publish committed events and record actions without duplicates.

- [Scheduling skill](../skills/schedule-landhome-projects/SKILL.md)
- [Lot-to-site-plan skill](../SKILL.md)
- [Build Tracker MCP setup](https://github.com/s10mcow/build-tracker#mcp-setup)
- [Hermes profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- [Hermes MCP configuration](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference)
- [Hermes cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
- [Hermes webhook signing](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks#security)

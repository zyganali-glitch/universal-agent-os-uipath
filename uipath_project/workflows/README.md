# UiPath Maestro Workflows

This folder contains the process orchestration models for Universal Agent OS.

**Disclaimer**: This repository uses a portable BPMN 2.0 process specification (`phase0_alignment.bpmn`), not a proprietary UiPath `.xaml` export. The live Maestro workflow has been validated and demonstrated via the provided screenshots and demo video.

## Recreating the Live Maestro Workflow

To recreate this flow in your UiPath Automation Cloud / Maestro instance:

1. Open UiPath Automation Cloud and navigate to Maestro.
2. Create a new process named `Phase-0 Alignment Review`.
3. Add a **Start event**.
4. Add a **Service task**: Fetch Master Memory from Data Service.
5. Add an **Agent/coded task**: Phase-0 Alignment.
6. Add a **User task**: Action Center approval.
7. Add an **Exclusive gateway**: approved/rejected.
8. **Approved path**: Add a **Service task** to grant execution.
9. **Rejected path**: Add a **Service task** to update Minefield History.
10. Add **End events** for both paths.

### Component Mapping

| Process Node | UiPath Component | Description |
|---|---|---|
| Fetch Master Memory | Data Service | Retrieves entity records like `CodeSoul` and `MinefieldHistory`. |
| Phase-0 Alignment | Integration Service / Python | Triggers the external agent (Cursor/Gemini) to propose a plan. |
| Action Center Review | Action Center (Form Tasks) | Pauses execution until a Lead Developer approves the plan. |
| Grant Execution | Orchestrator (Jobs) | Unblocks the agent to begin code modifications. |
| Update Minefield | Data Service | Saves lessons learned if rejected. |

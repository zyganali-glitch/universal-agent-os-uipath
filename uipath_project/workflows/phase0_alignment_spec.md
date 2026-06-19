# Phase-0 Alignment Maestro Specification

**Process Name:** Phase-0 Alignment Review
**Actors:** External Agent (Cursor, Gemini), Lead Developer (Human)
**UiPath Components Used:** Maestro BPMN, Data Service, Action Center, Integration Service / Orchestrator API

## Data Entities
- **Inputs:** `task_description` (String), `agent_type` (String)
- **Outputs:** `approval_status` (Boolean), `updated_memory_record_id` (String)
- **Entities Queried:** `CodeSoul`, `MinefieldHistory`, `Persona`, `StateMemory`

## Execution Paths

### Happy Path (Approved)
1. Task is submitted.
2. Maestro queries Data Service for the latest memory files.
3. The Phase-0 Alignment job runs, feeding memory + task to the external agent.
4. The agent formulates a proposed implementation plan.
5. Maestro creates an Action Center task.
6. Lead Developer reviews and clicks "Approve".
7. Maestro grants execution context back to the agent.
8. Process ends successfully.

### Rejection Path (Rejected)
1. Steps 1-5 same as above.
2. Lead Developer reviews the plan and clicks "Reject", providing a reason.
3. Maestro routes to the Rejection path.
4. Maestro triggers a Data Service update to append the rejection reason to `MinefieldHistory`.
5. Process ends. Execution is blocked.

### Failure Handling
- If Data Service is unreachable, Maestro suspends the job and notifies admins.
- If Action Center times out (e.g., 24 hours without review), the job auto-rejects for security.

## Audit Log Expectations
- Every run generates a unique `JobId` in Orchestrator.
- The Action Center task ID is permanently linked to the execution context.
- Memory updates are auditable in Data Service history.

## Track 2 Compliance (Maestro BPMN)
This design deeply integrates Maestro as the central nervous system for autonomous agents, ensuring that AI coding actions are governed by a human-in-the-loop and backed by enterprise-grade persistent memory.

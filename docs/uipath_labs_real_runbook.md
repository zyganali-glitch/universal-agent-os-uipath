# UiPath Labs Real Runbook

## Goal
Run Universal Agent OS through UiPath Labs / Automation Cloud, not only through the offline dashboard.

## Prerequisites
- UiPath Labs access
- Tenant / organization details
- Data Service enabled
- Maestro BPMN enabled
- Action Center enabled
- Access token or integration credentials
- Python 3.11+

## Step 1 — Create Data Service entities
Use these schemas:
- `uipath_project/entities/code_soul.json`
- `uipath_project/entities/minefield_history.json`
- `uipath_project/entities/persona.json`
- `uipath_project/entities/state_memory.json`

Create the entities under your Automation Cloud tenant -> Data Service page, matching the properties and names in the schemas.

## Step 2 — Seed memory records
Create initial records:
- **CodeSoul:** Add rules like `"No eval() code injection allowed"`, `"Always close files after opening"`.
- **MinefieldHistory:** Add records for past failures, e.g., `"Idempotency guard required on payments"`.
- **Persona:** Add a record configuring preference strictness: `"strictness: high"`.
- **StateMemory:** Initialize with empty or default configuration.

## Step 3 — Create Maestro BPMN process
Process name:
`UniversalAgentOS_Phase0_Flow`

Nodes:
1. StartEvent_TaskSubmitted
2. ServiceTask_FetchMasterMemory
3. ServiceTask_RunPhase0Alignment
4. UserTask_ActionCenterReview
5. ExclusiveGateway_ApprovalDecision
6. ServiceTask_GrantExecution
7. ServiceTask_SaveStateMemory
8. ServiceTask_UpdateMinefieldHistory
9. EndEvent_Approved
10. EndEvent_Rejected

## Step 4 — Connect Action Center
Create a human approval task named:
`Phase-0 Alignment Review`

Required fields:
- Agent
- Requested task
- Minefield matches
- Proposed plan
- Approval decision
- Reviewer notes

## Step 5 — Configure strict real mode
Create `.env` from `.env.example`.

Required environment variables:
- `UIPATH_MOCK_MODE=false`
- `UIPATH_TENANT_NAME`
- `UIPATH_OU_ID`
- `UIPATH_ACCESS_TOKEN`
- `UIPATH_TIMEOUT_SECONDS=30`

If endpoint auto-generation does not match the Labs tenant, add full endpoint variables and update connector accordingly:
- `UIPATH_ORCHESTRATOR_ODATA_URL`
- `UIPATH_DATA_SERVICE_API_URL`
- `UIPATH_ACTION_CENTER_ODATA_URL`

## Step 6 — Run smoke test
Run:
```bash
python -m py_compile backend/sync_markdown_to_uipath.py backend/uipath_api_connector.py
python backend/uipath_api_connector.py
python backend/sync_markdown_to_uipath.py
```

## Step 7 — Capture evidence
Capture all items listed in `docs/labs_evidence_checklist.md`.

## How to Record the Hackathon Demo Video (Step-by-Step)

To produce a compelling and honest submission that shows your solution running on UiPath Labs:

1. **Setup & Logging In:**
   - Log in to your UiPath Automation Cloud using your authorized credentials.
   - Show your Organization and Tenant dashboard to establish that this is a real UiPath cloud instance.
2. **Data Service Verification (0:00 - 1:00):**
   - Navigate to the **Data Service** tab.
   - Show the created entities (`CodeSoulRule`, `MinefieldHistory`, etc.) and show the records seeded inside. Highlight the severity column and rules schemas.
3. **Maestro BPMN Design (1:00 - 2:00):**
   - Open **UiPath Studio** or the Maestro canvas.
   - Briefly explain the node transitions of `UniversalAgentOS_Phase0_Flow` (Fetch Memory -> Agent Phase-0 -> Action Center human gateway).
4. **Trigger & Execution (2:00 - 3:30):**
   - Submit a task from the developer dashboard or run `python backend/labs_smoke_test.py` with `UIPATH_MOCK_MODE=false` to execute in strict real mode.
   - Show the terminal or application log indicating the API requests being sent live.
5. **Action Center Gate (3:30 - 4:30):**
   - Go to **Action Center** in Automation Cloud.
   - Click on the newly created task: `Phase-0 Alignment Review`. Show the form containing the agent's proposed plan.
   - Click **Approve**. Explain that the agent is blocked and cannot write any code until this human gate is cleared.
6. **Data Service Audit Persistence (4:30 - 5:00):**
   - Go back to Data Service and show that the status has updated to `Approved` or that a new entry was appended to the history ledger.
   - Wrap up by showing the GitHub repository.

## Failure handling

If strict real mode fails:
- Do not silently fall back to mock.
- Record the error.
- Fix credentials/endpoints.
- Only mark real evidence as verified after a successful Labs run.

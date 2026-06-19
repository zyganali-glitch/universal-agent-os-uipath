# Phase-0 Alignment Review — UiPath Maestro Implementation Spec

## 1. Purpose
The purpose of the Phase-0 Alignment Review process is to govern autonomous AI coding agents before they make any modifications to a codebase. By fetching persistent rules ("Code Soul") and lessons from past mistakes ("Minefield History"), the orchestrator aligns the agent's behavior with architectural standards and ensures a human-in-the-loop gatekeeper reviews all planned modifications prior to execution.

## 2. Track alignment
This specification aligns with **Track 2: UiPath Maestro BPMN**. The orchestrator manages the state, routing, and persistence of the agent SSDL (Secure Software Development Lifecycle) pipeline, coordinating between Data Service, Action Center, external AI models, and human reviewers.

## 3. UiPath components
- **UiPath Maestro (BPMN):** The main process engine managing state transitions, conditional gateways, and user/service tasks.
- **UiPath Data Service:** Persists and serves structured entity data representing the agent's memory (`CodeSoul`, `MinefieldHistory`, `Persona`, `StateMemory`).
- **UiPath Action Center:** Serves as the Human-in-the-Loop gatekeeper, raising high-priority Form Tasks for lead developer plan review.
- **UiPath Integration Service / API Workflows:** Connects Maestro to the Python connector and AI backend.

## 4. Inputs
- `task_description` (String): The coding task or issue requested by the developer (e.g., "Add Stripe payment integration").
- `agent_name` (String): The designated AI agent framework (e.g., Cursor, Claude Code, Gemini CLI).
- `session_id` (String): Unique session identifier to correlate execution logs.

## 5. Outputs
- `approved` (Boolean): The final plan approval decision from the Lead Developer.
- `reviewer_notes` (String): Feedback and notes provided during the human review gate.
- `state_record_id` (String): The Data Service record ID showing the updated audit state.

## 6. Data Service entities
- **CodeSoul:** Corporate architectural rules and forbidden code patterns.
- **MinefieldHistory:** Log of past deployment failures, vulnerabilities, and hard-earned lessons.
- **Persona:** System preferences and strictness configurations.
- **StateMemory:** Runtime execution tracking and session history.

## 7. BPMN nodes

| BPMN Node | UiPath Component | Evidence |
| :--- | :--- | :--- |
| **Fetch Master Memory** | Data Service/API Workflow | entity schemas + screenshot |
| **Phase-0 Alignment** | Coding Agent / API Workflow | frontend demo + prompt evidence |
| **Human Review** | Action Center | screenshot/task id required |
| **Approval Decision** | Maestro BPMN Gateway | BPMN screenshot required |
| **Save Memory** | Data Service | record id/screenshot required |

## 8. Happy path
1. The developer triggers the workflow by submitting a task.
2. `Fetch Master Memory` retrieves governance schemas and rules from UiPath Data Service.
3. `Phase-0 Alignment` invokes the AI model, presenting the task alongside retrieved rules. The agent responds with a step-by-step implementation plan.
4. `Human Review` pauses execution, creating an Action Center task for review.
5. The Lead Developer approves the plan.
6. `Approval Decision` gateway routes to the `Grant Execution` service task, saving details and letting the agent proceed with code generation.
7. `Save Memory` updates the execution state in `StateMemory`.

## 9. Rejection path
1. Steps 1-4 are identical to the happy path.
2. The Lead Developer rejects the plan in Action Center.
3. `Approval Decision` gateway routes to `Update Minefield History`.
4. Maestro writes the rejected plan pattern and developer notes into `MinefieldHistory` to ensure future agents do not repeat the same mistake.
5. Execution stops.

## 10. Failure handling
- **API Timeout:** If the external AI agent fails to respond within the `UIPATH_TIMEOUT_SECONDS` threshold, the orchestrator raises a system alert and routes to manual support.
- **Data Service Offline:** If the connection to Data Service drops, Maestro suspends the process, avoiding execution in an unaligned state.

## 11. Human-in-the-loop behavior
No code modification is permitted until a physical human reviewer approves the agent's proposed plan. Action Center enforces this by suspending the active execution context until the Form Task is completed.

## 12. Auditability
Every process run is tracked in the UiPath Orchestrator Jobs ledger. The Action Center task ID is permanently bound to the Data Service record state for forensic and compliance review.

## 13. Real UiPath Labs deployment checklist
- [ ] Connect to UiPath Automation Cloud tenant.
- [ ] Deploy entities using JSON schemas in `uipath_project/entities/`.
- [ ] Import `phase0_alignment.bpmn` or manually build the process flow canvas.
- [ ] Configure environment variables in `.env` or Orchestrator assets.
- [ ] Verify that Action Center is enabled and cataloged for Agent Governance.

## 14. Evidence required for final submission
- Portable BPMN process file (`phase0_alignment.bpmn`).
- Connector verification logs.
- Screenshots of entities, Studio canvas, and Action Center tasks.

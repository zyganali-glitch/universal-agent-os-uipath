# Universal Agent OS — Evidence Manifest

This document serves as the single source of truth for the judging panel, outlining exactly what is fully implemented in the repository, what is a portable specification, what is simulated for demo purposes, and what requires external verification (e.g., via video or screenshots).

| Claim | Evidence File / Link | Status | Notes |
|---|---|---|---|
| **Public GitHub repo** | This repository | Verified in repo | Code is fully accessible and open source. |
| **MIT license** | [`LICENSE`](../LICENSE) | Verified in repo | Included in root directory. |
| **Track 2 Maestro BPMN alignment** | [`uipath_project/workflows/phase0_alignment.bpmn`](../uipath_project/workflows/phase0_alignment.bpmn) | Portable spec | Portable BPMN 2.0 specification provided. |
| **UiPath Data Service entity schemas** | `uipath_project/entities/*.json` | Verified in repo | `CodeSoul`, `MinefieldHistory`, `Persona`, `StateMemory` schemas included. |
| **Action Center task creation** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py), [final demo](https://www.youtube.com/watch?v=d-AZzY-8DgU) | Live API and tenant evidence | Final demo task `4205597` was created by the IDE agent's strict-real flow. |
| **Action Center decision verification** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py), [`backend/labs_smoke_test.py`](../backend/labs_smoke_test.py), [`demo_screenshots/final/02_action_center_explicit_approval.png`](demo_screenshots/final/02_action_center_explicit_approval.png) | Implemented and shown live | Reads task completion and task data through UiPath APIs; Phase-0 starts only after explicit approval is verified. |
| **Data Fabric / Data Service memory** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py), [`demo_screenshots/final/03_data_fabric_governance_memory.png`](demo_screenshots/final/03_data_fabric_governance_memory.png) | Implemented; tenant entities shown live | The doctor verifies `CodeSoul`, `MinefieldHistory`, `Persona`, and `StateMemory` before registration. |
| **Mock demo mode** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py) | Verified in repo | Activated via `UIPATH_MOCK_MODE=true`. |
| **Strict real mode** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py) | Verified in repo | Strict environment variable checks; no fallback. |
| **Beginner IDE bootstrap** | [`../AGENTS.md`](../AGENTS.md), [`../CLAUDE.md`](../CLAUDE.md), [`../GEMINI.md`](../GEMINI.md), [`../.cursor/rules/universal-agent-os.mdc`](../.cursor/rules/universal-agent-os.mdc) | Verified in repo | A nontechnical prompt triggers the same governed workflow across supported agent discovery surfaces. |
| **Auditable Phase-0 interview** | [`../backend/phase0_interview.py`](../backend/phase0_interview.py), [`../tests/test_phase0_interview.py`](../tests/test_phase0_interview.py) | Verified and tested | Requires an approved gate, asks one question at a time, and persists the contract. |
| **Coding agents used during build** | [`coding_agents_evidence.md`](coding_agents_evidence.md) | Verified in repo | Prompt excerpts, visual evidence, and public commit history are identified explicitly. |
| **Frontend dashboard simulation** | [`frontend/agent_builder_mockup.html`](../frontend/agent_builder_mockup.html) | Verified in repo | Offline interactive demo of SSDL flow. |
| **Final demo video** | [YouTube](https://www.youtube.com/watch?v=d-AZzY-8DgU) | Published | 3:51 silent walkthrough with burned-in English captions and live UiPath evidence. |
| **Refreshed screenshot set** | [`demo_screenshots/final`](demo_screenshots/final) | Verified in repo | Eight chronological frames covering IDE registration, Action Center approval, Data Fabric, BPMN canvas, Phase-0, and repository evidence. |
| **Devpost page** | [Universal Agent OS: UiPath Edition](https://devpost.com/software/universal-agent-os-uipath-edition) | Published; copy review in progress | See `devpost_submission_update.md` for the refreshed answer set. |
| **Presentation deck** | Presentation URL | Manual action required | Required before final submission. |
| **BPMN / Agentic Process canvas** | [`demo_screenshots/final/04_bpmn_agentic_process_canvas.png`](demo_screenshots/final/04_bpmn_agentic_process_canvas.png) | UiPath design evidence | The portable BPMN is in the repo and the UiPath design canvas is shown. No completed Maestro runtime instance is claimed. |
| **Orchestrator jobs** | [final demo](https://www.youtube.com/watch?v=d-AZzY-8DgU) | Tenant evidence with limitation | Submitted jobs were visible as `Pending`; completed unattended execution is not claimed. |

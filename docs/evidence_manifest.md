# Universal Agent OS — Evidence Manifest

This document serves as the single source of truth for the judging panel, outlining exactly what is fully implemented in the repository, what is a portable specification, what is simulated for demo purposes, and what requires external verification (e.g., via video or screenshots).

| Claim | Evidence File / Link | Status | Notes |
|---|---|---|---|
| **Public GitHub repo** | This repository | Verified in repo | Code is fully accessible and open source. |
| **MIT license** | [`LICENSE`](../LICENSE) | Verified in repo | Included in root directory. |
| **Track 2 Maestro BPMN alignment** | [`uipath_project/workflows/phase0_alignment.bpmn`](../uipath_project/workflows/phase0_alignment.bpmn) | Portable spec | Portable BPMN 2.0 specification provided. |
| **UiPath Data Service entity schemas** | `uipath_project/entities/*.json` | Verified in repo | `CodeSoul`, `MinefieldHistory`, `Persona`, `StateMemory` schemas included. |
| **Action Center task creation** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py), [`labs/strict_real_mode_output.txt`](labs/strict_real_mode_output.txt) | Live API evidence | Strict real run created Form Task ID `4173555`. |
| **Action Center decision verification** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py), [`backend/labs_smoke_test.py`](../backend/labs_smoke_test.py) | Implemented; fresh tenant run required | Reads task completion and task data through UiPath APIs; requires explicit `Approved=true`. |
| **Data Service memory read/write** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py) | Implemented; write proven live | Entity names are configurable; doctor verifies all four before registration. Existing strict-real evidence proves a live write. |
| **Mock demo mode** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py) | Verified in repo | Activated via `UIPATH_MOCK_MODE=true`. |
| **Strict real mode** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py) | Verified in repo | Strict environment variable checks; no fallback. |
| **Beginner IDE bootstrap** | [`../AGENTS.md`](../AGENTS.md), [`../CLAUDE.md`](../CLAUDE.md), [`../GEMINI.md`](../GEMINI.md), [`../.cursor/rules/universal-agent-os.mdc`](../.cursor/rules/universal-agent-os.mdc) | Verified in repo | A nontechnical prompt triggers the same governed workflow across supported agent discovery surfaces. |
| **Auditable Phase-0 interview** | [`../backend/phase0_interview.py`](../backend/phase0_interview.py), [`../tests/test_phase0_interview.py`](../tests/test_phase0_interview.py) | Verified and tested | Requires an approved gate, asks one question at a time, and persists the contract. |
| **Coding agents used during build** | [`coding_agents_evidence.md`](coding_agents_evidence.md) | Verified in repo | Prompt excerpts, visual evidence, and public commit history are identified explicitly. |
| **Frontend dashboard simulation** | [`frontend/agent_builder_mockup.html`](../frontend/agent_builder_mockup.html) | Verified in repo | Offline interactive demo of SSDL flow. |
| **Demo video** | YouTube Link | Manual action required | To be submitted on Devpost showing live UiPath Labs. |
| **Devpost page** | Devpost Project URL | Manual action required | See `devpost_submission_update.md` for text submission. |
| **Presentation deck** | Presentation URL | Manual action required | Required before final submission. |
| **Live Maestro Flow** | `labs/maestro_bpmn_canvas.png` | Requires fresh external screenshot | Portable BPMN is in the repo; live Maestro canvas/run evidence must be captured from the tenant. |

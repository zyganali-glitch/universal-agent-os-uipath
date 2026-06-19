# Universal Agent OS — Evidence Manifest

This document serves as the single source of truth for the judging panel, outlining exactly what is fully implemented in the repository, what is a portable specification, what is simulated for demo purposes, and what requires external verification (e.g., via video or screenshots).

| Claim | Evidence File / Link | Status | Notes |
|---|---|---|---|
| **Public GitHub repo** | This repository | Verified in repo | Code is fully accessible and open source. |
| **MIT license** | [`LICENSE`](../LICENSE) | Verified in repo | Included in root directory. |
| **Track 2 Maestro BPMN alignment** | [`uipath_project/workflows/phase0_alignment.bpmn`](../uipath_project/workflows/phase0_alignment.bpmn) | Verified in repo | Portable BPMN spec provided. |
| **UiPath Data Service entity schemas** | `uipath_project/entities/*.json` | Verified in repo | `CodeSoul`, `MinefieldHistory`, `Persona`, `StateMemory` schemas included. |
| **Action Center / human approval concept** | [`frontend/agent_builder_mockup.html`](../frontend/agent_builder_mockup.html) | Demo mode | Modal simulation of the Action Center gate. |
| **Mock demo mode** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py) | Verified in repo | Activated via `UIPATH_MOCK_MODE=true`. |
| **Strict real mode** | [`backend/uipath_api_connector.py`](../backend/uipath_api_connector.py) | Verified in repo | Strict environment variable checks; no fallback. |
| **Coding agents used during build** | [`docs/coding_agents_evidence.md`](coding_agents_evidence.md) | Verified in repo | Documentation of agents and their contributions. |
| **Frontend dashboard simulation** | [`frontend/agent_builder_mockup.html`](../frontend/agent_builder_mockup.html) | Verified in repo | Offline interactive demo of SSDL flow. |
| **Demo video** | YouTube Link | Requires external link | To be submitted on Devpost. |
| **Devpost page** | Devpost Project URL | Requires external link | See `devpost_submission_update.md` for text. |
| **Presentation deck** | Placeholder URL | Missing | Required before final submission. |
| **Live Maestro Flow** | `docs/maestro_flow.png` | Requires external screenshot | To be provided by the user if available. |

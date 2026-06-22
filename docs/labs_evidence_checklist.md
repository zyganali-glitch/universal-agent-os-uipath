# UiPath Evidence Checklist

Final demo: https://www.youtube.com/watch?v=d-AZzY-8DgU

| Evidence | Status | Repository artifact / limitation |
|---|---|---|
| Beginner IDE prompt and governed registration | Complete | [`demo_screenshots/final/01_agent_registers_uipath_gate.png`](demo_screenshots/final/01_agent_registers_uipath_gate.png) |
| Action Center explicit approval | Complete | Task `4205597`; [`demo_screenshots/final/02_action_center_explicit_approval.png`](demo_screenshots/final/02_action_center_explicit_approval.png) |
| Data Fabric entity list | Complete | [`demo_screenshots/final/03_data_fabric_governance_memory.png`](demo_screenshots/final/03_data_fabric_governance_memory.png) |
| CodeSoul, MinefieldHistory, Persona, StateMemory availability | Complete | Visible in the Data Fabric frame and checked by `labs_smoke_test.py doctor` |
| API-backed approval verification | Complete | Shown in the final demo and implemented by `labs_smoke_test.py verify` |
| Phase-0 one-question-at-a-time interview | Complete | [`demo_screenshots/final/05_phase0_plain_language_interview.png`](demo_screenshots/final/05_phase0_plain_language_interview.png) |
| Phase-0 master-plan artifact | Complete | [`demo_screenshots/final/06_phase0_complete_master_plan.png`](demo_screenshots/final/06_phase0_complete_master_plan.png) |
| BPMN / Agentic Process design canvas | Complete as design evidence | [`demo_screenshots/final/04_bpmn_agentic_process_canvas.png`](demo_screenshots/final/04_bpmn_agentic_process_canvas.png); no completed Maestro runtime is claimed |
| Orchestrator jobs | Partial tenant evidence | Submitted jobs were visible as `Pending`; no completed unattended execution is claimed |
| June 22 strict-real API validation | Complete | [`labs/live_validation_2026-06-22.md`](labs/live_validation_2026-06-22.md); task `4222982` completed and approval was written to StateMemory |
| Published/deployed Maestro runtime instance | Open | Follow [`maestro_end_to_end_runbook_tr.md`](maestro_end_to_end_runbook_tr.md); capture an instance ending as `Completed` |
| Public repository and agent rules | Complete | [`demo_screenshots/final/07_repository_agent_rules.png`](demo_screenshots/final/07_repository_agent_rules.png) |
| Final under-five-minute video | Complete | 3:51, burned-in English captions |

For the full claim boundary, use [`evidence_manifest.md`](evidence_manifest.md).

# PLAN: Competition Readiness

## Goal
Make the `universal-agent-os-uipath` repo competition-ready for UiPath AgentHack Track 2 by enforcing strict real/mock separation, adding evidence artifacts, and ensuring 100% honesty in claims.

## Governance Locks
- No-New-Debt: 0 debt delta.
- Integrity Lock: All tasks tracked here.
- Strict Real Mode: No fallback.

## Tasks

### Phase 1: Environment & Tooling
- [ ] Create `.env.example`
- [ ] Add `pytest>=8.0.0` to `backend/requirements.txt`
- [ ] Add `.github/workflows/ci.yml`
- [ ] Create `tests/test_uipath_connector_modes.py`

### Phase 2: Strict Real / Mock Mode
- [ ] Refactor `backend/uipath_api_connector.py` for Strict Real vs Mock mode.
- [ ] Update `backend/sync_markdown_to_uipath.py` to log mode and handle mock IDs.

### Phase 3: Workflow Specification
- [ ] Delete `uipath_project/workflows/phase0_alignment.xaml` (if exists) or remove references.
- [ ] Create `uipath_project/workflows/README.md`
- [ ] Create `uipath_project/workflows/phase0_alignment_spec.md`
- [ ] Create `uipath_project/workflows/phase0_alignment.bpmn`

### Phase 4: Documentation & Evidence
- [ ] Create `docs/evidence_manifest.md`
- [ ] Create `docs/coding_agents_evidence.md` & `docs/agent_prompt_log_template.md`
- [ ] Create `docs/demo_transcript.md`
- [ ] Create `docs/devpost_submission_update.md`

### Phase 5: UI & README Polishing
- [ ] Update `frontend/agent_builder_mockup.html` text.
- [ ] Update `README.md` to reflect strict reality/demo disclosure.

### Phase 6: Final Verification
- [ ] Run automated tests and pipeline checks locally.

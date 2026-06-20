# PLAN: UiPath Orchestrator Machine Configuration & Smoke Test Normalization

## Goal
Map Unattended machines/runtimes in the UiPath Orchestrator Shared folder to resolve the 409 Conflict error, then normalize `backend/labs_smoke_test.py` to verify actual Job states (Pending, Running, or Successful) rather than bypassing the error.

## Governance Locks
- No-New-Debt: 0 debt delta.
- Integrity Lock: All tasks tracked here.
- Strict Real Mode: No fallback to mock mode.

## Tasks

### Phase 1: Orchestrator Machine Mapping Guide
- [x] Document and provide clear step-by-step instructions to configure Unattended Machine template and map it to the "Shared" folder.

### Phase 2: Smoke Test Normalization
- [x] Modify `backend/labs_smoke_test.py` to remove the 409 Conflict bypass and print actual job status if started successfully.

### Phase 3: Verification
- [x] Run pytest to verify unit tests.
- [x] Run smoke test after user configures Orchestrator to confirm job creation, execution, and Action Center task generation.

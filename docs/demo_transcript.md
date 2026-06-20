# Demo Transcript / Walkthrough

## 0:00–0:30 — Beginner promise
- **Narrative:** "The user does not need to know software terminology. They start with one sentence: 'Bir fikrim var, birlikte yapalım.' The repository tells the IDE agent how to register governance, request human approval, and begin a safe interview."
- **Visuals:** Show the single prompt in the IDE and the agent discovering the root governance contract.

## 0:30–1:05 — Register the real governance gate
- **Narrative:** "The coding agent runs the register command before scoping. Strict Real Mode reads Code Soul and Minefield History from Data Service, starts the deployed UiPath process, and creates an Action Center task. The command returns `AWAITING_HUMAN`; no execution grant exists."
- **Visuals:** Run `python backend/labs_smoke_test.py register`. Zoom into the returned job ID, task ID, memory counts, and `gate_status`.

## 1:05–1:35 — Prove that chat confirmation is not enough
- **Narrative:** "Even if a user says they approved, the agent does not trust chat. The verification command reads the Action Center task from UiPath. While it is pending, Phase-0 stays blocked."
- **Visuals:** Run `python backend/labs_smoke_test.py verify` before completing the task and show `AWAITING_HUMAN`.

## 1:35–2:05 — Human review in Action Center
- **Narrative:** "A lead developer reviews the proposed plan, explicitly checks the approval field, and submits the decision."
- **Visuals:** Open the exact task ID in Action Center, show the plan, check `I approve this plan and grant execution permission`, and submit.

## 2:05–2:35 — Verify and persist the grant
- **Narrative:** "The same verification command now reads the completed server-side task and requires `Approved=true`. Only then does it write the approved audit state to Data Service and return `APPROVED`."
- **Visuals:** Run `python backend/labs_smoke_test.py verify`, then show the new StateMemory row in Data Service.

## 2:35–3:05 — Maestro model and coding-agent bonus
- **Narrative:** "The repository includes the portable BPMN 2.0 lifecycle model, and the UiPath tenant shows the live process canvas/run. We dogfooded the project using Gemini and GitLab Duo."
- **Visuals:** Show the live Maestro canvas/run, then briefly show coding-agent evidence and the public GitHub repository.

## 3:05–3:30 — Phase-0 begins
- **Narrative:** "Only after verified approval does the beginner interview start. The agent asks one everyday-language question, saves the answer, and advances to exactly one next question."
- **Visuals:** Answer the first question and show the second question returned by the Phase-0 engine.

## What the video proves
- Live Orchestrator process triggering, Data Service reads/writes, and Action Center decision verification.
- Maestro BPMN lifecycle model plus separate tenant evidence of the live canvas/run.
- Honest separation between local interactive demo (offline simulation) and backend integration code.
- Verification of agent involvement during the build process.

## What remains external/manual
- Operating-system-level enforcement against a deliberately malicious agent.
- Reproduction in the judge's tenant without their own UiPath credentials and deployed process.

## Recommended next video improvements
- Use voiceover or burned-in captions.
- Keep IDs and statuses large enough to read.
- Show a pending verification failure before approval and a successful verification afterward.
- Show the live Maestro canvas/run and the portable BPMN file as two distinct artifacts.

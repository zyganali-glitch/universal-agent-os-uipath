# Devpost Submission Update Text

## One-liner
Universal Agent OS is a UiPath Maestro BPMN governance layer for autonomous coding agents, enforcing Phase-0 alignment, human approval, and collective memory before code execution.

## What it does
Universal Agent OS wraps around any autonomous coding agent (Cursor, Claude Code, Gemini CLI, etc.) and integrates it into a Secure Software Development Lifecycle (SSDL). The process is orchestrated by UiPath Maestro BPMN. Before an agent can write code, it must align its proposal with global architectural guidelines ("Code Soul") and lessons from past errors ("Minefield History") stored in UiPath Data Service. The plan must then pass an approval gate in UiPath Action Center before code execution is unblocked.

## Inspiration
Enterprises are racing to adopt AI coding assistants, but the lack of governance is a huge barrier. Coding agents are brilliant but lack architectural compliance, context-aware guardrails, and persistent memory. We designed a framework where agents are governed like junior developers who need alignment sessions and code approvals.

## How we built it
The orchestration workflow is modeled in BPMN and executed via the UiPath stack. We implemented a Python connector that communicates with Orchestrator, Data Service, and Action Center APIs. The system runs in two modes: an offline interactive simulation dashboard (Demo Mode) and a robust integration checking mode (Strict Real Mode) that enforces strict environment validation and API responses without silent mock fallbacks. We dogfooded our governance rules using Google Gemini and GitLab Duo to build the project.

## UiPath components used
- **UiPath Maestro (BPMN):** Manages the process orchestration lifecycle.
- **UiPath Data Service:** Stores and serves the 4 Collective Memory tables.
- **UiPath Action Center:** Acts as the Human-in-the-Loop approval gate task server.
- **UiPath Integration Service & API:** Links Python agent processes with Orchestrator.

## What is real vs simulated
- **Real in repo:**
  - Python connector with mock and strict real mode.
  - Data Service entity schemas.
  - Portable BPMN process specification.
  - Frontend dashboard simulation.
  - Governance markdown parser.
- **Real in UiPath Labs if shown:**
  - Maestro BPMN process.
  - Data Service entity.
  - Action Center task.
  - Run id / task id / screenshot evidence.
- **Simulated:**
  - Offline dashboard approval modal.
  - Mock API mode.
- **Strict mode:**
  - No fallback to mock.
  - Missing env vars fail fast.

## Coding agents used
- **GitLab Duo:** Assisted with markdown sync script design.
- **Google Gemini 3.5 Flash:** Assisted with Python connector strict separation, test suite, and spec documentation.

## Challenges
Creating a non-blocking asynchronous callback mechanism that allows a synchronous BPMN workflow to pause until the agent plan is reviewed required careful endpoint designing. Designing strict real mode tests that fail fast on environment configuration issues without accidentally mocking was also a key challenge.

## Accomplishments
Successfully showing that UiPath Maestro can act as the governance layer for modern AI software development. We transitioned coding agents from unsupervised black-boxes into managed, auditable assets.

## What we learned
Persistent memory makes AI code generation significantly safer. Feeding past mistakes back to the agent before plan generation reduces repeating the same security or logic bugs.

## What’s next
- Publishing the Orchestrator/Data Service integrations to the UiPath Marketplace.
- Implementing automated risk scoring based on modified files before showing the task in Action Center.
- Supporting concurrent multi-agent team workflows.

## Built with tags
- `uipath`, `bpmn`, `python`, `data-service`, `action-center`, `ai-agents`, `gemini`

## Demo video checklist
- [ ] Present the SSDL coding agent problem.
- [ ] Show the offline simulation dashboard running.
- [ ] Explain how Maestro orchestrates and pauses for Action Center.
- [ ] Display the Data Service tables inside UiPath Automation Cloud.
- [ ] Display the Maestro BPMN workflow in Studio.
- [ ] Walk through the repository files.

## Manual Devpost checklist
- [ ] Verify GitHub repository is public.
- [ ] Add the 5-minute screencast link.
- [ ] Input live tenant IDs and runbook references.
- [ ] Check links to all evidence files.

# Devpost Submission Update Text

## One-liner
Universal Agent OS is a UiPath-based governance prototype for autonomous coding agents. It models the lifecycle in Maestro BPMN, reads persistent governance memory, creates a human review task, and verifies the Action Center decision before Phase-0 can continue.

## What it does
Universal Agent OS wraps around coding agents such as Cursor, Claude Code, and Gemini CLI and integrates them into a Secure Software Development Lifecycle (SSDL). The process is modeled in UiPath Maestro BPMN. Before Phase-0, the strict connector reads architectural guidelines ("Code Soul") and lessons from past errors ("Minefield History") from UiPath Data Service. It then creates an Action Center task. A separate verification step reads the server-side task result and proceeds only when the task is completed with explicit approval.

A nontechnical user can start with only: **“Bir fikrim var, birlikte
yapalım.”** Repository-native adapters teach supported IDE agents to run the
governance flow themselves. After verified approval, an auditable Phase-0
engine asks eight plain-language questions one at a time and persists the
answers before technical planning begins.

## Inspiration
Enterprises are racing to adopt AI coding assistants, but the lack of governance is a huge barrier. Coding agents are brilliant but lack architectural compliance, context-aware guardrails, and persistent memory. We designed a framework where agents are governed like junior developers who need alignment sessions and code approvals.

## How we built it
The orchestration workflow is modeled in portable BPMN 2.0 and connected to live UiPath Orchestrator, Data Service, and Action Center APIs. The system runs in two explicit modes: an offline interactive simulation dashboard and Strict Real Mode, which validates configuration and never silently falls back to mock responses. Strict Real Mode supports memory reads, process triggering, review-task creation, server-side decision verification, and approval/rejection persistence. We dogfooded our governance rules using Google Gemini and GitLab Duo to build the project.

## UiPath components used
- **UiPath Maestro (BPMN):** Models the process orchestration lifecycle; the portable BPMN is included in the repository.
- **UiPath Data Service:** Stores and serves the 4 Collective Memory tables.
- **UiPath Action Center:** Acts as the Human-in-the-Loop approval gate task server.
- **UiPath Orchestrator and platform APIs:** Link Python agent processes with the deployed UiPath runtime.

## What is real vs simulated
- **Real in repo:**
  - Python connector with mock and strict real mode.
  - Data Service entity schemas.
  - Portable BPMN process specification.
  - Frontend dashboard simulation.
  - Governance markdown parser.
  - Data Service memory reads and writes.
  - Action Center completion and explicit approval verification.
  - Root-level discovery instructions for Codex-compatible agents, Claude,
    Gemini, Cursor, and GitHub Copilot.
  - A stateful one-question-at-a-time beginner Phase-0 interview.
- **Real in UiPath Labs if shown:**
  - Maestro BPMN process.
  - Data Service entity.
  - Action Center task.
  - Run id / task id / screenshot evidence.
- **Simulated:**
  - Offline dashboard approval modal.
  - Mock API mode.
  - Operating-system-level prevention of a deliberately malicious agent bypassing repository instructions.
- **Strict mode:**
  - No fallback to mock.
  - Missing env vars fail fast.

## Coding agents used
- **GitLab Duo:** Assisted with markdown sync script design.
- **Google Gemini 3.5 Flash:** Assisted with Python connector strict separation, test suite, and spec documentation.

## Challenges
Separating task creation from server-side approval verification was a key challenge. The agent must not trust a chat message claiming approval; it verifies the completed Action Center task through UiPath before proceeding. Designing strict real mode tests that fail fast without silently mocking was another challenge.

## Accomplishments
Successfully demonstrating live UiPath job creation, Action Center task creation, Data Service persistence, an API-backed approval verifier, and a beginner experience that converts a nontechnical idea into a governed Phase-0 contract.

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
- [ ] Show `register`, the pending Action Center task, and blocked `verify`.
- [ ] Approve in Action Center and show successful API-backed `verify`.
- [ ] Explain the portable Maestro BPMN model and show the live tenant canvas/run separately.
- [ ] Display the Data Service tables inside UiPath Automation Cloud.
- [ ] Display the Maestro BPMN workflow in Studio.
- [ ] Walk through the repository files.

## Manual Devpost checklist
- [ ] Verify GitHub repository is public.
- [ ] Add the 5-minute screencast link.
- [ ] Input live tenant IDs and runbook references.
- [ ] Check links to all evidence files.

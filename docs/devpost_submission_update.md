# Devpost Submission Update Text

## Final links
- **Demo:** https://www.youtube.com/watch?v=d-AZzY-8DgU
- **GitHub:** https://github.com/zyganali-glitch/universal-agent-os-uipath
- **GitLab mirror:** https://gitlab.com/zyganali/universal-agent-os-uipath

## One-liner
Universal Agent OS is a UiPath-based governance prototype for autonomous coding agents. It models the lifecycle in Maestro BPMN, reads persistent governance memory, creates a human review task, and verifies the Action Center decision before Phase-0 can continue.

## What it does
Universal Agent OS wraps around coding agents such as Cursor, Claude Code, and Gemini CLI and integrates them into a Secure Software Development Lifecycle (SSDL). The process is modeled in UiPath Maestro BPMN. Before Phase-0, the strict connector reads architectural guidelines ("Code Soul") and lessons from past errors ("Minefield History") from UiPath Data Service. It then creates an Action Center task. A separate verification step reads the server-side task result and proceeds only when the task is completed with explicit approval.

A nontechnical user can start with only: **"I have an idea. Please help me turn
it into a project."** Repository-native adapters teach supported IDE agents to
run the governance flow themselves. After verified approval, an auditable
Phase-0 engine asks eight plain-language questions one at a time and persists
the answers before technical planning begins.

## Inspiration
Enterprises are racing to adopt AI coding assistants, but the lack of governance is a huge barrier. Coding agents are brilliant but lack architectural compliance, context-aware guardrails, and persistent memory. We designed a framework where agents are governed like junior developers who need alignment sessions and code approvals.

## How we built it
The orchestration workflow is modeled in portable BPMN 2.0 and connected to live UiPath Orchestrator, Data Service, and Action Center APIs. The system runs in two explicit modes: an offline interactive simulation dashboard and Strict Real Mode, which validates configuration and never silently falls back to mock responses. Strict Real Mode supports memory reads, process triggering, review-task creation, server-side decision verification, and approval/rejection persistence. We dogfooded our governance rules using Google Gemini and GitLab Duo to build the project.

## UiPath components used
- **UiPath Maestro / Agentic Process (BPMN):** Models the process orchestration lifecycle; the portable BPMN is included in the repository and the UiPath design canvas appears in the final demo.
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
- **Shown live in the final demo:**
  - Action Center task creation and explicit completed approval.
  - Data Fabric entities for CodeSoul, MinefieldHistory, Persona, and StateMemory.
  - UiPath Agentic Process BPMN design canvas.
  - API-backed approval verification and the Phase-0 interview.
  - Orchestrator job submissions visible in `Pending`.
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
Successfully demonstrated live Action Center task creation, explicit human approval, API-backed decision verification, Data Fabric governance memory, and a beginner experience that converts one nontechnical sentence into a governed Phase-0 contract and formal master plan. Orchestrator job submissions were visible in the tenant as `Pending`; completed unattended execution is not claimed.

## What we learned
Persistent memory makes AI code generation significantly safer. Feeding past mistakes back to the agent before plan generation reduces repeating the same security or logic bugs.

## What’s next
- Publishing the Orchestrator/Data Service integrations to the UiPath Marketplace.
- Implementing automated risk scoring based on modified files before showing the task in Action Center.
- Supporting concurrent multi-agent team workflows.

## Built with tags
- `uipath`, `bpmn`, `python`, `data-service`, `action-center`, `ai-agents`, `gemini`

## Final demo evidence
- [x] Beginner starts with a single nontechnical prompt.
- [x] IDE agent runs the doctor and registers the live Action Center gate.
- [x] Explicit approval is completed in Action Center.
- [x] API verification unlocks Phase-0.
- [x] Data Fabric governance-memory entities are shown.
- [x] UiPath BPMN / Agentic Process design canvas is shown.
- [x] One-question-at-a-time Phase-0 interview completes.
- [x] Formal master plan appears before implementation.
- [x] Repository rules and evidence are shown.

## Manual Devpost checklist
- [ ] Verify GitHub repository is public.
- [x] Add the under-5-minute screencast link.
- [x] Link the public evidence manifest and refreshed screenshots.
- [ ] Check links to all evidence files.

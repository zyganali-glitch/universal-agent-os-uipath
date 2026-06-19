# Devpost Submission Update Template

*Copy and paste the relevant sections below into your Devpost submission to ensure 100% honesty and alignment with the repository evidence.*

---

## Elevator Pitch
Universal Agent OS is a governance framework that wraps around coding agents (like Cursor or Gemini), enforcing a Secure Software Development Lifecycle via UiPath Maestro BPMN and Collective Memory before a single line of code is written.

## Inspiration
Enterprises are adopting AI coding agents at an unprecedented rate, but no one trusts them to push code to production without oversight. Agents lack corporate memory and ignore architectural rules. We wanted to treat agents like employees who must pass an onboarding gate, read company rules, and get human approval before touching the codebase.

## What it does
It uses UiPath Maestro BPMN to orchestrate the entire agent lifecycle. When a task is assigned, Maestro fetches architectural rules ("Code Soul") and past mistakes ("Minefield History") from UiPath Data Service. The agent formulates a plan, which Maestro suspends and sends to a Lead Developer via UiPath Action Center. Only upon human approval does the agent get execution rights.

## How we built it
We utilized the core UiPath Automation Cloud stack for orchestration and Python for the agent integration layer. We also dogfooded the concept: this entire prototype was built using Google Gemini 3.1 Pro and GitLab Duo, actively using our governance rules to keep the agents on track.

## UiPath Components Used
- **UiPath Maestro (BPMN)**: Orchestrates the Phase-0 alignment and approval flow.
- **UiPath Data Service**: Stores the "Code Soul" and "Minefield History" entities.
- **UiPath Action Center**: Provides the human-in-the-loop approval gate.

## What is Real vs Simulated (Strict Reality Disclosure)
We believe in 100% transparency for hackathon judging.
- **Real in repo**: The Python UiPath Integration Connector, Data Service entity schemas, the portable BPMN process spec, and the Markdown rule parser.
- **Real in UiPath Cloud**: [Update this if you provide screenshots: The live Maestro flow, Data Service entities, and Action Center tasks.]
- **Strict Mode**: Our `backend/uipath_api_connector.py` features a Strict Real Mode that enforces environment variables and never falls back to mock data, ensuring enterprise readiness.
- **Simulated / Offline Demo**: The frontend interactive dashboard features an offline simulation of the Action Center approval modal, and the backend has an explicit `MOCK_MODE` for offline judging without cloud credentials.

## Coding Agents Used
- **GitLab Duo**: Pair-programmed the Python backend logic.
- **Google Gemini 3.1 Pro**: Refactored the architecture, implemented the Strict Real/Mock mode separation, wrote the CI pipelines, and generated the BPMN specifications.

## Challenges we ran into
Integrating async agent workflows into a synchronous BPMN process required us to build a robust pausing mechanism. Ensuring that the mock mode didn't accidentally pass as "real" required strict architectural separation in our Python connector.

## Accomplishments that we're proud of
Successfully proving that AI coding agents can be governed by UiPath Maestro. We transformed an unsupervised liability into an auditable, enterprise-ready workflow.

## What we learned
We learned that "Collective Memory" is the missing piece in AI dev tools. When we fed past agent mistakes back into the prompt via Data Service, the success rate of subsequent code generation improved dramatically.

## What's next for Universal Agent OS
- Publishing the integration connector to the UiPath Marketplace.
- Adding AI-powered risk scoring before the human Action Center review.
- Supporting multi-agent swarms orchestrated by Maestro.

# Demo Transcript / Walkthrough

## 0:00–0:30 — Problem
- **Narrative:** "AI coding agents like Cursor or Gemini are fast, but they have no persistent memory of past mistakes and no concept of corporate guidelines. They can easily push unsafe code to production. Universal Agent OS solves this by placing UiPath Maestro BPMN as a governance layer over coding agents."
- **Visuals:** Showing the problem slide or code editor showing raw uncontrolled agent changes.

## 0:30–0:56 — Offline dashboard simulation
- **Narrative:** "We start with the developer dashboard. We submit a task to add Stripe payment integration. The orchestrator triggers and fetches master memory records from Data Service. The agent proposes a plan, but execution is immediately suspended. A human approval gate is created in UiPath Action Center."
- **Visuals:** Interacting with the offline dashboard (`frontend/agent_builder_mockup.html`), inputting the payment task, advancing phases, and displaying the Action Center approval modal.

## 0:57–1:29 — Coding agents bonus / dogfooding
- **Narrative:** "To build this governance tool, we dogfooded our own product. We pair-programmed our integration connector with Google Gemini and GitLab Duo. Here you can see GitLab Duo assisting in writing the markdown parsing logic."
- **Visuals:** GitLab Web IDE showing GitLab Duo prompt logs or screenshots of interaction.

## 1:30–1:33 — UiPath Data Service evidence
- **Narrative:** "In our UiPath Automation Cloud tenant, we defined entities for Code Soul rules, Minefield History, Persona guidelines, and State Memory. This provides our agents with a centralized persistent database memory."
- **Visuals:** Navigating the Data Service UI in Automation Cloud, displaying the schema and columns of the entities.

## 1:34–1:37 — UiPath Maestro BPMN evidence
- **Narrative:** "The process engine is defined in UiPath Studio using Maestro BPMN workflows. It models the happy path (approving execution) and the rejection path (updating Minefield History so future agents learn from the refusal)."
- **Visuals:** UiPath Studio Maestro BPMN process canvas showing task boxes and gateways.

## 1:38–End — Repository overview
- **Narrative:** "The repository is public on GitHub and contains the portable BPMN spec, entity schemas, connector tests, and a strict real mode that communicates directly with Automation Cloud APIs without fallbacks."
- **Visuals:** Scrolling the README and showing the folder structure on GitHub.

## What the video proves
- Deep integration concept using UiPath stack (Maestro, Data Service, Action Center).
- Honest separation between local interactive demo (offline simulation) and backend integration code.
- Verification of agent involvement during the build process.

## What remains external/manual
- Live execution logs of the Maestro runner, since they require manual tenant execution.
- Actual production deployment of the BPMN workflow in the judge's own tenant.

## Recommended next video improvements
- Add voiceover or captions.
- Spend more seconds on UiPath Labs screens.
- Show real Maestro run id.
- Show Action Center task id.
- Show Data Service record creation/update.
- Show GitHub repo instead of GitLab if final Devpost links to GitHub.

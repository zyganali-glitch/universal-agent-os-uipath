<p align="center">
  <img src="https://img.shields.io/badge/Track-2%20·%20Maestro%20BPMN-FA4616?style=for-the-badge&logo=uipath&logoColor=white" />
  <img src="https://img.shields.io/badge/UiPath-AgentHack%202026-0066FF?style=for-the-badge&logo=uipath&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<h1 align="center">🛡️ Universal Agent OS</h1>
<h3 align="center">Secure Software Development Lifecycle for Autonomous Coding Agents</h3>
<p align="center"><em>Orchestrated by UiPath Maestro BPMN · Human-in-the-Loop Governance · Collective Memory</em></p>

---

## 🎯 The Problem

Enterprises are adopting AI coding agents (Cursor, Claude Code, Gemini CLI, GitHub Copilot) at an unprecedented rate. But here's the uncomfortable truth:

> **No one trusts an autonomous agent to push code to production without oversight.**

These agents are brilliant — but they have no memory of past mistakes, no awareness of architectural rules, and no concept of human accountability. They'll happily repeat the same bug that took your team 3 weeks to fix last quarter.

## 💡 The Solution: Universal Agent OS

**Universal Agent OS** is a governance framework that wraps around any coding agent and enforces a **Secure Software Development Lifecycle (SSDL)** before the agent writes a single line of code.

The entire orchestration is powered by **UiPath Maestro BPMN**, making it enterprise-grade, auditable, and deeply integrated with human-in-the-loop approval workflows.

### How It Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        UiPath Maestro BPMN                              │
│                                                                         │
│  ┌──────────┐    ┌────────────┐    ┌──────────┐    ┌─────────────────┐  │
│  │  Start    │───▶│ Fetch      │───▶│ Phase-0  │───▶│ Human Review    │  │
│  │  Process  │    │ Memory     │    │ Alignment│    │ (Action Center) │  │
│  └──────────┘    └────────────┘    └──────────┘    └────────┬────────┘  │
│                                                             │           │
│                       ┌─────────────┐    ┌──────────┐       │           │
│                       │ Save to     │◀───│ Agent    │◀──────┘           │
│                       │ Memory      │    │ Executes │   (if approved)   │
│                       └─────────────┘    └──────────┘                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### The 4 Master Memory Files (UiPath Data Service)

| Memory File | Purpose | Example |
|---|---|---|
| 🔴 **State Memory** | Current session state & task history | `{ sessions: 5, last_task: "Add OAuth2" }` |
| 👤 **Your Persona** | Developer preferences & review strictness | `{ style: "functional", strictness: "high" }` |
| 💣 **Minefield History** | Past failures & lessons learned | `"Payment gateways MUST be idempotent"` |
| 📜 **Code Soul** | Architectural principles & forbidden patterns | `"No eval(), no SELECT *, no console.log"` |

## 🤖 Agent Type
**Explicit Statement:** This solution utilizes **Both** (Coded Agents & Low-code Agents).
It uses **Low-code Agents** (UiPath Maestro BPMN and Action Center) for the orchestration, alignment, and human approval workflows, and connects to **Coded Agents** (Python Backend, Gemini CLI) for the actual backend synchronization and coding tasks.

## 🏗️ UiPath Components Used

To ensure true enterprise governance, Universal Agent OS relies heavily on the core UiPath Automation Cloud stack.

| UiPath Component | Role in Universal Agent OS |
|---|---|
| **UiPath Maestro (BPMN)** | **Process Orchestrator:** Controls the entire agent lifecycle. Routes the workflow from "Phase-0 Interview" to "Human Approval", and ultimately "Code Execution". |
| **UiPath Data Service** | **Collective Memory Storage:** Stores and serves the 4 Master Memory Files as structured entities (`CodeSoulRule`, `MinefieldHistory`, etc.), allowing programmatic retrieval and updates by the AI. |
| **UiPath Action Center** | **Human Approval Gate:** Pauses the AI's execution plan and creates a high-priority task for a Lead Developer to review. The agent cannot proceed without a human `APPROVED` state. |
| **UiPath Integration Service** | **Agent Connector:** Acts as the secure bridge linking Maestro workflows to external AI agent APIs (like Gemini, Cursor, or Claude). |
| **UiPath Apps** | **Task Dashboard:** The frontend interface where developers submit their coding requests to trigger the Maestro orchestration. |

## 🏆 Why This Wins

### Innovation
- **First framework** to treat coding agents as "employees" who must go through onboarding (Phase-0), read company rules (Code Soul), and learn from past mistakes (Minefield History).
- **Collective Memory** persists across agents and sessions — when one agent learns a lesson, all future agents benefit.

### UiPath Integration Depth
- Full BPMN lifecycle management via **Maestro**
- Human-in-the-loop via **Action Center** (not just a checkbox — real enterprise approval workflow)
- Persistent entity storage via **Data Service** (not files — real database entities)

### Coding Agents Bonus (Built-With) ✅
- Native integration designed for **Cursor** (Claude), **Gemini CLI**, and **GitHub Copilot**.
- **How we used agents to build this:** This entire prototype, including the SSDL logic, Python `uipath_api_connector.py`, and interactive frontend dashboard, was pair-programmed using **Google Gemini 3.1 Pro** and **GitLab Duo**. 
- *Proof/Artifacts:* The repository includes `sync_markdown_to_uipath.py` which was iteratively developed inside GitLab Web IDE aided by the Duo agent. See the screenshot section below for prompt logs and IDE setup.

## 📂 Repository Structure

```
universal-agent-os-uipath/
├── README.md                           # You are here
├── .agent_governance/                  # Physical markdown rules synced from Universal-Agent-OS
├── backend/
│   ├── sync_markdown_to_uipath.py      # Syncs file-based governance to UiPath Data Service
│   ├── uipath_api_connector.py         # UiPath Orchestrator & Data Service API bridge
│   └── requirements.txt                # Python dependencies
├── frontend/
│   └── agent_builder_mockup.html       # Interactive SSDL dashboard (demo)
├── docs/
│   └── architecture_bpmn.mermaid       # BPMN sequence diagram
└── uipath_project/
    ├── entities/                        # UiPath Data Service entity schemas
    │   ├── code_soul.json
    │   ├── minefield_history.json
    │   ├── state_memory.json
    │   └── persona.json
    └── workflows/
        └── phase0_alignment.xaml        # UiPath Studio workflow definition
```

## 🚀 Setup & Execution

### 1. Pre-requisites & Sanity Check
Before running, verify that the Python backend compiles correctly:
```bash
python -m py_compile backend/sync_markdown_to_uipath.py backend/uipath_api_connector.py
```
*(No output means successful compilation without syntax errors).*

### 2. Demo Mode (Mock API)
If you do not have UiPath tokens configured, the system falls back to a graceful Demo Mode.
1. **Clone** this repository.
2. **Open** `frontend/agent_builder_mockup.html` in your browser.
3. **Select** a coding agent and type a task (try: "Add Stripe payment integration").
4. **Click** "Start Maestro Process" and use the **Next Step** button to manually progress through the BPMN phases.
5. **Run** `python backend/sync_markdown_to_uipath.py` to see the simulated syncing of local governance rules to Data Service.

### 3. Production Mode (Real UiPath Automation Cloud)
To connect to a real UiPath tenant:
1. Set the environment variables:
   ```bash
   export UIPATH_MOCK_MODE="false"
   export UIPATH_TENANT_NAME="your_tenant"
   export UIPATH_OU_ID="your_ou_id"
   export UIPATH_ACCESS_TOKEN="your_oauth_token"
   ```
2. Run the connector. The `uipath_api_connector.py` will now make live `requests.post()` calls to your UiPath Orchestrator, Data Service, and Action Center endpoints.

---

## 📸 Proof of Concept (Live UiPath Cloud)

*(Below are the artifacts proving the live integration with UiPath Automation Cloud and the Coding Agent IDE)*

**1. UiPath Data Service (Central Governance Entity)**
We use Data Service to store the `MinefieldHistory` and `CodeSoul` rules globally. Here is our live entity configured in the UiPath Automation Cloud Data Fabric:
![Data Service Entity](docs/data_service.png)

**2. UiPath Maestro BPMN (Process Orchestrator)**
The entire AI orchestration lifecycle is built around a Maestro BPMN workflow (`Phase-0 Alignment Review`), acting as the enterprise gatekeeper.
![Maestro BPMN Flow](docs/maestro_flow.png)

**3. UiPath Action Center & Dashboard Simulation**
For the frontend developer experience, we created an interactive terminal dashboard. In production, this ties into Action Center for human approval:
![Agent Dashboard](docs/screenshot1.png)

**2. GitLab Duo / Gemini Building the Connector**
This entire project was pair-programmed with AI. Here is the interaction in the GitLab Web IDE with the Duo agent actively syncing the governance model.
![GitLab Duo IDE](docs/screenshot2.png)

**3. Repository View**
Our project resides securely in GitLab/GitHub, maintaining full history and SSDL components.
![GitLab Repo](docs/screenshot3.png)

## 🔮 Future Vision

- **UiPath Marketplace Integration**: Publish as a reusable automation component
- **Multi-Agent Orchestration**: Multiple agents collaborating on the same codebase with shared memory
- **Risk Scoring**: AI-powered risk assessment before human review
- **Audit Trail**: Complete compliance log for regulated industries (SOC 2, HIPAA)

## 📄 License

MIT License — Built for the UiPath AgentHack 2026

---

<p align="center"><strong>Universal Agent OS</strong> — Because autonomous doesn't mean unsupervised.</p>

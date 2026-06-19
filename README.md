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

## 🏗️ Architecture (UiPath Mapping)

| Universal Agent OS Component | UiPath Product | Role |
|---|---|---|
| Task Dashboard | **UiPath Apps** | Developer submits coding requests |
| Process Orchestrator | **UiPath Maestro (BPMN)** | Controls the entire agent lifecycle |
| Collective Memory | **UiPath Data Service** | Stores & serves the 4 Master Memory Files |
| Human Approval Gate | **UiPath Action Center** | Lead developer reviews & approves/rejects agent plans |
| Agent Connector | **UiPath Integration Service** | Bridges Maestro to external AI agents (Cursor, Gemini) |

## 🏆 Why This Wins

### Innovation
- **First framework** to treat coding agents as "employees" who must go through onboarding (Phase-0), read company rules (Code Soul), and learn from past mistakes (Minefield History).
- **Collective Memory** persists across agents and sessions — when one agent learns a lesson, all future agents benefit.

### UiPath Integration Depth
- Full BPMN lifecycle management via **Maestro**
- Human-in-the-loop via **Action Center** (not just a checkbox — real enterprise approval workflow)
- Persistent entity storage via **Data Service** (not files — real database entities)

### Coding Agents Bonus ✅
- Native integration with **Cursor** (Claude), **Gemini CLI**, and **GitHub Copilot**
- The agents don't just exist in the project — **they are the core subjects being governed**

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

## 🚀 Quick Start (Demo)

1. **Clone** this repository
2. **Open** `frontend/agent_builder_mockup.html` in your browser
3. **Select** a coding agent (Cursor, Gemini, or Copilot)
4. **Type** a task (try: "Add Stripe payment integration")
5. **Click** "Start Maestro Process" and use the **Next Step** button to manually progress through the BPMN phases
6. **Approve or Reject** the agent's plan when the Action Center modal appears
7. **Run** `python backend/sync_markdown_to_uipath.py` to sync local governance rules to Data Service

## 🔮 Future Vision

- **UiPath Marketplace Integration**: Publish as a reusable automation component
- **Multi-Agent Orchestration**: Multiple agents collaborating on the same codebase with shared memory
- **Risk Scoring**: AI-powered risk assessment before human review
- **Audit Trail**: Complete compliance log for regulated industries (SOC 2, HIPAA)

## 📄 License

MIT License — Built for the UiPath AgentHack 2026

---

<p align="center"><strong>Universal Agent OS</strong> — Because autonomous doesn't mean unsupervised.</p>

# UiPath Maestro BPMN Workflow Artifacts

This folder contains the process-level artifacts for the Universal Agent OS Track 2 submission.

## Important disclosure

`phase0_alignment.bpmn` is a portable BPMN 2.0 specification for repository review. It is not a proprietary UiPath export unless replaced by an actual export from UiPath Studio / UiPath Maestro.

If a real UiPath Labs export is later added, place it in this folder and update this README and `docs/evidence_manifest.md`.

## Process

**Name:** Universal Agent OS - Phase-0 Alignment Review  
**Track:** UiPath Maestro BPMN  
**Purpose:** Govern autonomous coding agents before they write code.

## Actors

| Actor | Role |
|---|---|
| Developer | Submits coding task |
| UiPath Maestro BPMN | Orchestrates the process |
| UiPath Data Service | Stores Code Soul, Minefield History, Persona and State Memory |
| Coding Agent | Generates implementation plan and later writes code |
| Lead Developer | Reviews plan via Action Center approval gate |

## Required UiPath Labs implementation

1. Create Data Service entities from `uipath_project/entities/*.json`.
2. Create a Maestro BPMN process named `UniversalAgentOS_Phase0_Flow`.
3. Add service task: Fetch Master Memory.
4. Add agent/service task: Run Phase-0 Alignment.
5. Add user task: Action Center Review.
6. Add exclusive gateway: approved/rejected.
7. Approved path: Grant execution permission and save State Memory.
8. Rejected path: Update Minefield History and stop execution.
9. Capture screenshots and run ids listed in `docs/labs_evidence_checklist.md`.

# Coding Agents Evidence

This document outlines how autonomous coding agents were used to build the Universal Agent OS. 

## Which coding agents were used?
- **GitLab Duo**: Used within the GitLab Web IDE for iterative Python scripting.
- **Google Gemini 3.1 Pro (High)**: Used via Antigravity SDK to strictly enforce governance, refactor the repository for competition readiness, build testing pipelines, and generate precise documentation.

## What did each agent contribute?
- **GitLab Duo**:
  - `backend/sync_markdown_to_uipath.py`: Assisted in writing regex parsing for markdown rule extraction.
- **Google Gemini 3.1 Pro (High)**:
  - `backend/uipath_api_connector.py`: Refactored to separate Mock vs Strict Real modes, ensuring robust failure handling for judging.
  - `tests/test_uipath_connector_modes.py`: Generated pytest assertions covering environmental variables and mock behaviors.
  - `.github/workflows/ci.yml`: Added continuous integration and evidence manifestation checks.
  - Process specs: Wrote the `phase0_alignment.bpmn` spec and accompanying markdown specs to honestly reflect the architecture.

## Evidence artifacts
- `docs/screenshot2.png`: Shows GitLab Duo IDE interaction.
- `docs/agent_prompt_log_template.md`: Template for capturing interaction logs.
- Git Commit History: Demonstrates iterative build patterns using the agents.

## Bonus Point Narrative for Judges
We didn't just build a governance system *for* coding agents—we used coding agents to build it. By dogfooding our own philosophies, we experienced firsthand the necessity of "Minefield History" and "Code Soul." When Gemini or Duo attempted to use non-strict error handling or hallucinated an export file, our manual and automated governance checks (like `opradox-qa` rules) caught them, proving the exact problem this project solves.

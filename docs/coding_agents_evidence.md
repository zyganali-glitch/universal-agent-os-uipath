# Coding Agents Evidence

## Summary

This project was built with assistance from coding agents. The purpose of this document is to make the contribution evidence explicit for UiPath AgentHack judging.

## Agents used

| Agent | Claimed use | Evidence status | Evidence file |
|---|---|---|---|
| GitLab Duo | Assisted with connector/governance sync implementation | Screenshot evidence | `docs/screenshot2.png` |
| Gemini CLI / Gemini 3.5 Flash | Assisted with prototype planning and code generation | Requires prompt/session log if available | `docs/agent_prompt_log_template.md` |
| GitHub Copilot / Cursor | Integration target and optional development assistant | Requires evidence if claimed as build assistant | Manual evidence required |

## Files influenced

| File | Agent contribution | Evidence |
|---|---|---|
| `backend/sync_markdown_to_uipath.py` | Governance sync script design and iteration | GitLab Duo screenshot |
| `backend/uipath_api_connector.py` | Connector structure and strict/mock mode iteration | Prompt log or commit notes required |
| `frontend/agent_builder_mockup.html` | Interactive dashboard prototype | Prompt log or manual note required |

## Judge narrative

Universal Agent OS dogfoods the same problem it solves: coding agents helped build the governance system that governs coding agents. The repo includes explicit proof where available and marks missing evidence honestly instead of overstating it.

## Missing evidence

- Add real prompt logs or screenshots before final submission if available.
- Do not claim full bonus points unless prompt/session evidence is present.

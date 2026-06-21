# Coding Agents Evidence

## Summary

This project was built with assistance from coding agents. The purpose of this document is to make the contribution evidence explicit for UiPath AgentHack judging.

## Agents used

| Agent | Claimed use | Evidence status | Evidence file |
|---|---|---|---|
| GitLab Duo | Assisted with connector/governance sync implementation | Prompt excerpts, commit history, and submitted video | [`agent_prompt_log_gemini.md`](agent_prompt_log_gemini.md) |
| Gemini (Antigravity) | Assisted with prototype planning, code generation, and strict mode testing | Prompt excerpts available | `agent_prompt_log_gemini.md` |
| GitHub Copilot / Cursor | Integration target and optional development assistant | N/A | Manual evidence required |

## Files influenced

| File | Agent contribution | Evidence |
|---|---|---|
| `backend/sync_markdown_to_uipath.py` | Governance sync script design and iteration | Prompt excerpts and public commit history |
| `backend/uipath_api_connector.py` & `backend/labs_smoke_test.py` | Connector structure and Strict Real Mode iteration | Prompt excerpts (`agent_prompt_log_gemini.md`) plus commit history |
| `README.md` & `docs/demo_transcript.md` | Narrative construction and sequential demo mapping | Prompt excerpts (`agent_prompt_log_gemini.md`) plus commit history |

## Judge narrative

Universal Agent OS dogfoods the same problem it solves: coding agents helped build the governance system that governs coding agents. The repo includes explicit proof where available and marks missing evidence honestly instead of overstating it.

## Evidence boundary

The prompt file contains selected session excerpts, not a cryptographically complete transcript. The strongest reproducible evidence is the public commit history, working code, CI, and submitted video. This document intentionally avoids claiming more than those artifacts prove.

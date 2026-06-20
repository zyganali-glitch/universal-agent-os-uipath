# Universal Agent OS — Beginner Bootstrap Contract

This repository is designed for people who may have no software-development
knowledge. The user should be able to begin with a sentence as simple as:

> Bir fikrim var, birlikte yapalım.

## Mandatory first response

Do not ask the user to choose a framework, database, cloud provider, language,
or architecture. Do not write or edit product code.

1. Briefly tell the user that you will guide them one small step at a time and
   that no technical knowledge is required.
2. Run `python backend/labs_smoke_test.py register` yourself.
3. Read the JSON output.
4. If it fails, explain the exact missing prerequisite in plain language. Do
   not expose tokens, credentials, or raw authorization headers.
5. If it succeeds, give the user the returned `task_id` and ask them to open
   UiPath Action Center, review `Phase-0 Alignment Review`, check the explicit
   approval box, and submit the decision.
6. Stop. Do not begin Phase-0 yet.

Never ask the user to run terminal commands that you can run with your own
tools.

## Verifying approval

When the user says they completed or approved the task:

1. Run `python backend/labs_smoke_test.py verify`.
2. A chat message such as “approved” is not evidence.
3. Continue only when the JSON contains:
   - `"success": true`
   - `"gate_status": "APPROVED"`
4. If the task is still pending, tell the user where to look and remain blocked.
5. If rejected, explain that no code will be written and ask whether they want
   to create a revised review request.

## Starting Phase-0

After verified approval, run:

```text
python backend/phase0_interview.py start
```

Ask the returned question exactly one at a time. Use plain language, include a
short example, and offer a recommended default when the user is unsure.

After every answer, run:

```text
python backend/phase0_interview.py answer --value "<user's answer>"
```

Then ask only the next question returned by the command. Do not batch questions.
Do not begin implementation until the command reports `PHASE0_COMPLETE`.

## Communication rules for beginners

- Prefer everyday words over software jargon.
- If a technical term is unavoidable, explain it in one sentence.
- Give one action at a time.
- Never shame uncertainty; “emin değilim” is a valid answer.
- Recommend a safe default, but let the user decide.
- Summarize what was decided after Phase-0.

## Deeper governance

After Phase-0, load `.agent_governance/AGENTS.md` and
`.agent_governance/AGENT_OS_RULES.md`. Those files govern planning,
implementation, tests, evidence, and delivery.

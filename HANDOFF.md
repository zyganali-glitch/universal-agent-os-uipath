# Home PC Handoff - UiPath Maestro End-to-End

Last updated: June 22, 2026

## Read this first

This is an existing competition project, not a new-project bootstrap session.
Do not run the beginner Phase-0 flow automatically. Continue the work below.

The next objective is:

> Build, publish, deploy, run, and record one real UiPath Maestro agentic
> process instance that includes a human Action Center task and finishes as
> `Completed`.

Detailed browser instructions are in
[`docs/maestro_end_to_end_runbook_tr.md`](docs/maestro_end_to_end_runbook_tr.md).

## Current verified state

- Branch: `main`
- GitHub remote: `github`
- GitLab remote: `origin`
- Automation Cloud organization: `zyganaligroup`
- Tenant: `DefaultTenant`
- Orchestrator folder / OU ID: `7950291`
- External application authentication works with the organization-scoped
  client-credentials endpoint.
- `python backend/labs_smoke_test.py doctor` returned `ready: true`.
- All four Data Fabric entities were reachable:
  `CodeSoul`, `MinefieldHistory`, `Persona`, `StateMemory`.
- A strict-real Action Center task was created and verified:
  task ID `4222982`, status `Completed`, `approved: true`.
- The approval result was written to `StateMemory`.
- An Orchestrator job was submitted:
  job ID `692461706`, job key
  `49edc447-f393-4ef9-8893-4821f3f440b9`.
- That job was still `Pending`. It is an Orchestrator RPA job, not proof of a
  completed Maestro process instance.
- The portable BPMN and a Maestro design canvas exist, but a completed Maestro
  runtime instance is still the main competition gap.

Sanitized evidence is recorded in
[`docs/labs/live_validation_2026-06-22.md`](docs/labs/live_validation_2026-06-22.md).

## Security action required on the home PC

The previous app secret was exposed in chat. Treat it as compromised.

1. Open Automation Cloud Admin > External Applications > OAuth apps.
2. Open `UniversalAgentOS`.
3. Delete the exposed secret and generate a new secret.
4. Put the new value only in the home PC's local `.env`.
5. Never paste the new secret into chat, screenshots, commits, issues, or
   Devpost.

The `.env` file is intentionally ignored by Git and is not included in this
handoff.

## First commands on the home PC

```powershell
git clone https://github.com/zyganali-glitch/universal-agent-os-uipath.git
cd universal-agent-os-uipath
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
Copy-Item .env.example .env
```

Fill `.env` locally:

```dotenv
UIPATH_MOCK_MODE=false
UIPATH_ORGANIZATION_NAME=zyganaligroup
UIPATH_TENANT_NAME=DefaultTenant
UIPATH_OU_ID=7950291
UIPATH_ACCESS_TOKEN=
UIPATH_CLIENT_ID=<copy the App ID from UniversalAgentOS>
UIPATH_CLIENT_SECRET=<new secret; local only>
UIPATH_OAUTH_SCOPES=
UIPATH_RELEASE_KEY=
```

Then run:

```powershell
python -m pytest -q
python backend\labs_smoke_test.py doctor
```

Do not run `register` merely to resume work. The live API gate has already been
proved. The next work is in Maestro / Studio Web.

## First unchecked implementation step

- [ ] Create and deploy the `Phase-0 Alignment Review` Action App.
- [ ] Create or open the Maestro Agentic Process
  `UniversalAgentOS_Phase0_Flow`.
- [ ] Bind every BPMN task to a real implementation.
- [ ] Debug the approved and rejected paths.
- [ ] Publish the solution.
- [ ] Deploy it to the same Orchestrator folder.
- [ ] Configure execution identity for every child RPA/agent dependency.
- [ ] Start a real Maestro process instance.
- [ ] Complete its Action Center task.
- [ ] Confirm the Maestro instance itself reaches `Completed`.
- [ ] Capture instance ID, version, execution trail, Action task ID, and final
  StateMemory record.
- [ ] Update README/evidence files and replace the competition video only if
  the Devpost submission still permits it.

## Recommended message to the home agent

> `HANDOFF.md` ve `docs/maestro_end_to_end_runbook_tr.md` dosyalarını oku.
> Bu yeni proje bootstrap'i değil. İlk iş olarak git durumunu ve güncel
> UiPath erişimini kontrol et; sonra ilk işaretlenmemiş Maestro adımından devam
> et. Secret isteme veya sohbete yazdırma.

## Definition of done

This work is complete only when the UiPath Maestro Process Instances screen
shows a real `UniversalAgentOS_Phase0_Flow` instance with:

- a published and deployed version;
- a completed human task created by the Maestro User Task;
- the approved or rejected gateway path visible in the execution trail;
- a terminal process status of `Completed`;
- no task left with implementation type `None`;
- no required child job left in `Pending`;
- screenshots and IDs added to the repository evidence.

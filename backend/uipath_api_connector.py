import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass



class UiPathConfigurationError(RuntimeError):
    pass


class UiPathApiError(RuntimeError):
    pass


@dataclass(frozen=True)
class UiPathConfig:
    organization_name: str
    tenant_name: str
    organization_unit_id: str
    access_token: str
    client_id: str
    client_secret: str
    mock_mode: bool
    release_key: str = ""
    request_timeout_seconds: int = 30

    @classmethod
    def from_env(cls) -> "UiPathConfig":
        mock_mode = os.getenv("UIPATH_MOCK_MODE", "true").strip().lower() == "true"
        configured_organization = os.getenv(
            "UIPATH_ORGANIZATION_NAME",
            "",
        ).strip()
        configured_tenant = os.getenv("UIPATH_TENANT_NAME", "").strip()
        organization_name = configured_organization or configured_tenant
        tenant_name = (
            configured_tenant
            if configured_organization
            else os.getenv("UIPATH_ACTUAL_TENANT_NAME", "DefaultTenant").strip()
        )
        cfg = cls(
            organization_name=organization_name,
            tenant_name=tenant_name or "DefaultTenant",
            organization_unit_id=os.getenv("UIPATH_OU_ID", "").strip(),
            access_token=os.getenv("UIPATH_ACCESS_TOKEN", "").strip(),
            client_id=os.getenv("UIPATH_CLIENT_ID", "").strip(),
            client_secret=os.getenv("UIPATH_CLIENT_SECRET", "").strip(),
            mock_mode=mock_mode,
            release_key=os.getenv("UIPATH_RELEASE_KEY", "").strip(),
            request_timeout_seconds=int(os.getenv("UIPATH_TIMEOUT_SECONDS", "30")),
        )
        if not cfg.mock_mode:
            missing = []
            if not cfg.organization_name:
                missing.append("UIPATH_ORGANIZATION_NAME")
            if not cfg.organization_unit_id:
                missing.append("UIPATH_OU_ID")
            if not cfg.access_token and (not cfg.client_id or not cfg.client_secret):
                missing.append("UIPATH_ACCESS_TOKEN (or UIPATH_CLIENT_ID and UIPATH_CLIENT_SECRET)")
            if missing:
                raise UiPathConfigurationError(
                    "Strict real mode requires these environment variables: "
                    + ", ".join(missing)
                )
        return cfg


class UiPathMaestroConnector:
    """
    Bridge between Universal Agent OS and UiPath Automation Cloud.

    Modes:
    - UIPATH_MOCK_MODE=true:
      Offline demo mode. Returns clearly labeled mock ids.
    - UIPATH_MOCK_MODE=false:
      Strict real mode. Sends live requests and NEVER falls back to mock.
    """

    def __init__(self, config: Optional[UiPathConfig] = None):
        self.config = config or UiPathConfig.from_env()
        self.base_url = (
            f"https://cloud.uipath.com/{self.config.organization_name}/"
            f"{self.config.tenant_name}/orchestrator_/odata"
        )
        self.orchestrator_odata_url = os.getenv("UIPATH_ORCHESTRATOR_ODATA_URL", "").strip() or self.base_url
        self.data_service_api_url = os.getenv("UIPATH_DATA_SERVICE_API_URL", "").strip()
        self.action_center_odata_url = os.getenv("UIPATH_ACTION_CENTER_ODATA_URL", "").strip() or self.orchestrator_odata_url
        
        token = self.config.access_token
        if not self.config.mock_mode and not token and self.config.client_id and self.config.client_secret:
            token = self._fetch_oauth_token()

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-UIPATH-OrganizationUnitId": self.config.organization_unit_id,
        }

    def _fetch_oauth_token(self) -> str:
        url = "https://cloud.uipath.com/identity_/connect/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(
                url,
                data=payload,
                headers=headers,
                timeout=self.config.request_timeout_seconds
            )
            if response.status_code != 200:
                raise UiPathConfigurationError(f"OAuth failed with status {response.status_code}: {response.text}")
            res_data = response.json()
            return res_data.get("access_token", "")
        except Exception as exc:
            raise UiPathConfigurationError(f"OAuth authentication failed: {exc}") from exc

    @property
    def mock_mode(self) -> bool:
        return self.config.mock_mode

    def _post(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.config.request_timeout_seconds,
            )
            if response.status_code not in (200, 201, 202, 204):
                raise UiPathApiError(f"UiPath API failed with status {response.status_code}: {response.text}")
            return response.json() if response.content else {}
        except requests.RequestException as exc:
            raise UiPathApiError(f"UiPath API request failed: {url} :: {exc}") from exc

    def _get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=self.config.request_timeout_seconds,
            )
            if response.status_code != 200:
                raise UiPathApiError(
                    f"UiPath API failed with status {response.status_code}: {response.text}"
                )
            return response.json() if response.content else {}
        except requests.RequestException as exc:
            raise UiPathApiError(f"UiPath API request failed: {url} :: {exc}") from exc

    def start_maestro_process(self, process_name: str, input_args: Dict[str, Any]) -> Dict[str, Any]:
        if not process_name:
            raise ValueError("process_name is required")

        if self.mock_mode:
            return {
                "status": "mock_success",
                "job_id": f"mock_job_{int(time.time())}",
                "message": "MOCK MODE: Maestro Phase-0 process simulated.",
                "mock": True,
            }

        # Resolve release key: either from env or dynamically query Releases endpoint
        release_key = self.config.release_key
        if not release_key:
            try:
                releases_url = f"{self.orchestrator_odata_url.rstrip('/')}/Releases?$filter=ProcessKey eq '{process_name}' or contains(ProcessKey, '{process_name}')"
                response = requests.get(releases_url, headers=self.headers, timeout=self.config.request_timeout_seconds)
                if response.status_code == 200:
                    releases = response.json().get("value", [])
                    if releases:
                        release_key = releases[0].get("Key")
                if not release_key:
                    raise UiPathConfigurationError(
                        f"Could not find Release Key for process '{process_name}' in folder '{self.config.organization_unit_id}'. "
                        "Please configure UIPATH_RELEASE_KEY in .env or grant OR.Releases/OR.Releases.Read scope to the application."
                    )
            except Exception as exc:
                if isinstance(exc, UiPathConfigurationError):
                    raise
                raise UiPathConfigurationError(
                    f"Failed to fetch Release Key dynamically for process '{process_name}': {exc}. "
                    "Make sure the process is deployed and either UIPATH_RELEASE_KEY is set in .env "
                    "or OR.Releases scope is granted to the application."
                ) from exc

        payload = {
            "startInfo": {
                "ReleaseKey": release_key,
                "Strategy": "JobsCount",
                "JobsCount": 1,
                "InputArguments": json.dumps(input_args),
            }
        }

        endpoint = f"{self.orchestrator_odata_url.rstrip('/')}/Jobs/UiPath.Server.Configuration.OData.StartJobs"
        result = self._post(endpoint, payload)
        result["mock"] = False
        return result

    def update_master_memory(self, entity_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if not entity_name:
            raise ValueError("entity_name is required")
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary")

        if self.mock_mode:
            return {
                "status": "mock_success",
                "record_id": f"mock_record_{entity_name}_{int(time.time())}",
                "entity": entity_name,
                "mock": True,
            }

        if self.data_service_api_url:
            endpoint = f"{self.data_service_api_url.rstrip('/')}/{entity_name}/insert"
        else:
            endpoint = (
                f"https://cloud.uipath.com/{self.config.organization_name}/"
                f"{self.config.tenant_name}/dataservice_/api/EntityService/"
                f"{entity_name}/insert"
            )
        result = self._post(endpoint, data)
        result["mock"] = False
        return result

    def read_master_memory(
        self,
        entity_name: str,
        limit: int = 100,
    ) -> Dict[str, Any]:
        if not entity_name:
            raise ValueError("entity_name is required")
        if limit < 1:
            raise ValueError("limit must be greater than zero")

        if self.mock_mode:
            return {
                "status": "mock_success",
                "entity": entity_name,
                "records": [],
                "count": 0,
                "mock": True,
            }

        if self.data_service_api_url:
            endpoint = f"{self.data_service_api_url.rstrip('/')}/{entity_name}/read"
        else:
            endpoint = (
                f"https://cloud.uipath.com/{self.config.organization_name}/"
                f"{self.config.tenant_name}/"
                f"dataservice_/api/EntityService/{entity_name}/read"
            )

        payload = self._get(endpoint, params={"start": 0, "limit": limit})
        if isinstance(payload, list):
            records = payload[:limit]
        elif isinstance(payload, dict):
            raw_records = payload.get(
                "Value",
                payload.get("value", payload.get("records", [])),
            )
            records = raw_records[:limit] if isinstance(raw_records, list) else []
        else:
            records = []

        return {
            "entity": entity_name,
            "records": records,
            "count": len(records),
            "mock": False,
        }

    def request_human_approval(self, agent_plan: str) -> Dict[str, Any]:
        if not agent_plan.strip():
            raise ValueError("agent_plan is required")

        if self.mock_mode:
            return {
                "status": "mock_pending",
                "task_id": f"mock_task_{int(time.time())}",
                "approved": False,
                "mock": True,
                "message": "MOCK MODE: approval task created.",
            }

        payload = {
            "Title": "Phase-0 Alignment Review",
            "Priority": "High",
            "Data": {
                "AgentProposedPlan": agent_plan,
                "Approved": False,
                "ReviewerNotes": "",
            },
            "FormLayout": {
                "components": [
                    {
                        "label": "Agent Proposed Plan",
                        "key": "AgentProposedPlan",
                        "type": "textarea",
                        "input": True
                    },
                    {
                        "label": "I approve this plan and grant execution permission",
                        "key": "Approved",
                        "type": "checkbox",
                        "input": True
                    },
                    {
                        "label": "Reviewer Notes",
                        "key": "ReviewerNotes",
                        "type": "textarea",
                        "input": True
                    },
                    {
                        "label": "Submit Decision",
                        "key": "submit",
                        "type": "button",
                        "input": True
                    }
                ]
            }
        }

        base_url = self.action_center_odata_url.rstrip('/')
        if base_url.endswith('/odata'):
            base_url = base_url[:-6]
        endpoint = f"{base_url}/forms/TaskForms/CreateFormTask"
        
        result = self._post(endpoint, payload)
        result["mock"] = False
        if "id" in result:
            result["task_id"] = str(result["id"])
        return result

    def get_human_approval(self, task_id: str) -> Dict[str, Any]:
        if not str(task_id).strip():
            raise ValueError("task_id is required")

        if self.mock_mode:
            return {
                "task_id": str(task_id),
                "title": "Phase-0 Alignment Review",
                "status": "Completed",
                "completed": True,
                "approved": True,
                "reviewer_notes": "MOCK MODE: approval simulated.",
                "mock": True,
            }

        odata_endpoint = (
            f"{self.action_center_odata_url.rstrip('/')}/Tasks({task_id})"
        )
        task = self._get(odata_endpoint)
        status = str(task.get("Status", "")).strip()
        completed = bool(task.get("IsCompleted")) or status.lower() in {
            "completed",
            "done",
        }

        task_data: Dict[str, Any] = {}
        action = None
        if completed:
            base_url = self.action_center_odata_url.rstrip("/")
            if base_url.endswith("/odata"):
                base_url = base_url[:-6]
            detail_endpoint = (
                f"{base_url}/tasks/GenericTasks/GetTaskDataById"
            )
            detail = self._get(detail_endpoint, params={"taskId": task_id})
            if isinstance(detail, dict):
                raw_data = detail.get("data", {})
                task_data = raw_data if isinstance(raw_data, dict) else {}
                action = detail.get("action")

        raw_decision = task_data.get(
            "Approved",
            task_data.get("ApprovalDecision", task_data.get("approved")),
        )
        if isinstance(raw_decision, str):
            approved = raw_decision.strip().lower() in {
                "true",
                "approved",
                "approve",
                "yes",
            }
        else:
            approved = raw_decision is True

        return {
            "task_id": str(task_id),
            "title": str(task.get("Title", "")),
            "status": status or "Unknown",
            "completed": completed,
            "approved": completed and approved,
            "reviewer_notes": str(task_data.get("ReviewerNotes", "")),
            "action": action,
            "mock": False,
        }

    def wait_for_human_approval(
        self,
        task_id: str,
        timeout_seconds: int = 900,
        poll_interval_seconds: int = 5,
    ) -> Dict[str, Any]:
        if timeout_seconds < 1:
            raise ValueError("timeout_seconds must be greater than zero")
        if poll_interval_seconds < 1:
            raise ValueError("poll_interval_seconds must be greater than zero")

        deadline = time.monotonic() + timeout_seconds
        while True:
            decision = self.get_human_approval(task_id)
            if decision["completed"]:
                return decision
            if time.monotonic() >= deadline:
                raise UiPathApiError(
                    f"Timed out waiting for Action Center task {task_id}"
                )
            time.sleep(poll_interval_seconds)


if __name__ == "__main__":
    connector = UiPathMaestroConnector()
    print("Mode:", "MOCK" if connector.mock_mode else "STRICT_REAL")

    job = connector.start_maestro_process(
        "UniversalAgentOS_Phase0_Flow",
        {"task": "Add login page"},
    )
    print("Job:", job)

    approval = connector.request_human_approval(
        "I will inspect existing auth and UI patterns before changing code."
    )
    print("Approval:", approval)

    memory = connector.read_master_memory("MinefieldHistory", limit=10)
    print("Memory:", memory)

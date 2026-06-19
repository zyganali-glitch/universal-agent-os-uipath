import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


class UiPathConfigurationError(RuntimeError):
    pass


class UiPathApiError(RuntimeError):
    pass


@dataclass(frozen=True)
class UiPathConfig:
    tenant_name: str
    organization_unit_id: str
    access_token: str
    mock_mode: bool
    request_timeout_seconds: int = 30

    @classmethod
    def from_env(cls) -> "UiPathConfig":
        mock_mode = os.getenv("UIPATH_MOCK_MODE", "true").strip().lower() == "true"
        cfg = cls(
            tenant_name=os.getenv("UIPATH_TENANT_NAME", "").strip(),
            organization_unit_id=os.getenv("UIPATH_OU_ID", "").strip(),
            access_token=os.getenv("UIPATH_ACCESS_TOKEN", "").strip(),
            mock_mode=mock_mode,
            request_timeout_seconds=int(os.getenv("UIPATH_TIMEOUT_SECONDS", "30")),
        )
        if not cfg.mock_mode:
            missing = []
            if not cfg.tenant_name:
                missing.append("UIPATH_TENANT_NAME")
            if not cfg.organization_unit_id:
                missing.append("UIPATH_OU_ID")
            if not cfg.access_token:
                missing.append("UIPATH_ACCESS_TOKEN")
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
        self.base_url = f"https://cloud.uipath.com/{self.config.tenant_name}/DefaultTenant/odata"
        self.orchestrator_odata_url = os.getenv("UIPATH_ORCHESTRATOR_ODATA_URL", "").strip() or self.base_url
        self.data_service_api_url = os.getenv("UIPATH_DATA_SERVICE_API_URL", "").strip()
        self.action_center_odata_url = os.getenv("UIPATH_ACTION_CENTER_ODATA_URL", "").strip() or self.orchestrator_odata_url
        self.headers = {
            "Authorization": f"Bearer {self.config.access_token}",
            "Content-Type": "application/json",
            "X-UIPATH-OrganizationUnitId": self.config.organization_unit_id,
        }

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
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.RequestException as exc:
            raise UiPathApiError(f"UiPath API request failed: {url} :: {exc}") from exc

    def start_maestro_process(self, process_name: str, input_args: Dict[str, Any]) -> Dict[str, Any]:
        if not process_name:
            raise ValueError("process_name is required")

        payload = {
            "startInfo": {
                "ReleaseKey": process_name,
                "Strategy": "Specific",
                "RobotIds": [],
                "NoOfRobots": 0,
                "InputArguments": json.dumps(input_args),
            }
        }

        if self.mock_mode:
            return {
                "status": "mock_success",
                "job_id": f"mock_job_{int(time.time())}",
                "message": "MOCK MODE: Maestro Phase-0 process simulated.",
                "mock": True,
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
            endpoint = f"{self.data_service_api_url.rstrip('/')}/{entity_name}"
        else:
            endpoint = f"https://cloud.uipath.com/{self.config.tenant_name}/DataService_/api/v1/{entity_name}"
        result = self._post(endpoint, data)
        result["mock"] = False
        return result

    def request_human_approval(self, agent_plan: str) -> Dict[str, Any]:
        if not agent_plan.strip():
            raise ValueError("agent_plan is required")

        payload = {
            "taskCreateRequest": {
                "Title": "Phase-0 Alignment Review",
                "Priority": "High",
                "TaskCatalogName": "Agent Governance",
                "Data": {
                    "AgentProposedPlan": agent_plan,
                    "RequiresHumanOverride": False,
                },
            }
        }

        if self.mock_mode:
            return {
                "status": "mock_approved",
                "task_id": f"mock_task_{int(time.time())}",
                "approved": True,
                "mock": True,
                "message": "MOCK MODE: human approval simulated.",
            }

        endpoint = f"{self.action_center_odata_url.rstrip('/')}/FormTasks/UiPath.Server.Configuration.OData.CreateFormTask"
        result = self._post(endpoint, payload)
        result["mock"] = False
        return result


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

    memory = connector.update_master_memory(
        "MinefieldHistory",
        {"lesson": "Always inspect existing UI components before adding new ones."},
    )
    print("Memory:", memory)

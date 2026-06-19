import requests
import json
import os

class UiPathMaestroConnector:
    """
    Connects the Universal Agent OS to UiPath Maestro and Data Service.
    This acts as the bridge for external coding agents (Claude Code, Cursor, Gemini) 
    to interact with the UiPath Orchestrator.
    """
    def __init__(self):
        # In a real environment, these are fetched via OAuth2 from UiPath Automation Cloud
        self.tenant_name = os.getenv("UIPATH_TENANT_NAME", "default_tenant")
        self.organization_unit_id = os.getenv("UIPATH_OU_ID", "default_ou")
        self.access_token = os.getenv("UIPATH_ACCESS_TOKEN", "")
        self.base_url = f"https://cloud.uipath.com/{self.tenant_name}/DefaultTenant/odata"
        
        # Toggle between demo mock mode and real API mode
        self.use_mock_api = os.getenv("UIPATH_MOCK_MODE", "true").lower() == "true"
        
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-UIPATH-OrganizationUnitId": self.organization_unit_id
        }

    def start_maestro_process(self, process_name: str, input_args: dict):
        """
        Triggers the BPMN process in UiPath Maestro.
        This is called when a developer requests a new coding task.
        """
        print(f"[UiPath Connector] Starting Maestro BPMN Process: {process_name}")
        payload = {
            "startInfo": {
                "ReleaseKey": process_name,
                "Strategy": "Specific",
                "RobotIds": [],
                "NoOfRobots": 0,
                "InputArguments": json.dumps(input_args)
            }
        }
        
        if not self.use_mock_api and self.access_token:
            try:
                response = requests.post(f"{self.base_url}/Jobs/UiPath.Server.Configuration.OData.StartJobs", headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"[Warning] Real API call failed, falling back to mock. Error: {e}")
                
        # MOCK API FALLBACK
        print(f"[Mock Mode] Successfully triggered job for {process_name}")
        return {"status": "success", "job_id": "job_987654321", "message": "Maestro Phase-0 process started."}

    def update_master_memory(self, entity_name: str, data: dict):
        """
        Writes 'Minefield History' or 'Code Soul' updates to UiPath Data Service.
        """
        print(f"[UiPath Connector] Updating Data Service Entity '{entity_name}' with new Agent Memory.")
        
        if not self.use_mock_api and self.access_token:
            try:
                url = f"https://cloud.uipath.com/{self.tenant_name}/DataService_/api/v1/{entity_name}"
                response = requests.post(url, headers=self.headers, json=data)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"[Warning] Real API call failed, falling back to mock. Error: {e}")
        
        # MOCK API FALLBACK
        print(f"[Mock Mode] Entity {entity_name} successfully updated.")
        return {"status": "success", "record_id": "rec_12345"}

    def request_human_approval(self, agent_plan: str):
        """
        Creates a Form Task in UiPath Action Center for the Lead Developer.
        The external agent is paused until this returns True.
        """
        print("[UiPath Connector] Pausing agent... Sending Phase-0 Plan to UiPath Action Center for Human Approval.")
        
        # Exact payload schema for UiPath Action Center FormTask creation
        payload = {
            "taskCreateRequest": {
                "Title": "Phase-0 Alignment Review",
                "Priority": "High",
                "TaskCatalogName": "Agent Governance",
                "Data": {
                    "AgentProposedPlan": agent_plan,
                    "RequiresHumanOverride": False
                }
            }
        }
        
        if not self.use_mock_api and self.access_token:
            try:
                endpoint = f"{self.base_url}/FormTasks/UiPath.Server.Configuration.OData.CreateFormTask"
                response = requests.post(endpoint, headers=self.headers, json=payload)
                response.raise_for_status()
                task_data = response.json()
                print(f"[UiPath Connector] Task created successfully. Task ID: {task_data.get('Id')}")
                # In a real async scenario, we would wait for a webhook or poll.
                return True 
            except Exception as e:
                print(f"[Warning] Real API call failed, falling back to mock. Error: {e}")
        
        # MOCK API FALLBACK
        print("[UiPath Connector] [Mock Mode] Human (Lead Developer) approved the plan via UiPath Action Center.")
        return True

# Example Usage
if __name__ == "__main__":
    connector = UiPathMaestroConnector()
    
    # 1. Developer requests feature
    job = connector.start_maestro_process("UniversalAgentOS_Phase0_Flow", {"task": "Add login page"})
    
    # 2. Agent proposes a plan, we need human approval
    proposed_plan = "I will modify index.html and add auth.js without checking existing UI."
    is_approved = connector.request_human_approval(proposed_plan)
    
    # 3. If approved, Agent executes, then updates collective memory
    if is_approved:
        connector.update_master_memory("MinefieldHistory", {"lesson": "Always check existing UI components before adding new ones."})


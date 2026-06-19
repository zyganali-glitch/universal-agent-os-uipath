import os
import json
import re
from uipath_api_connector import UiPathMaestroConnector

class GovernanceSyncService:
    """
    Parses the Universal Agent OS markdown governance files (from the GitHub repo)
    and syncs them to UiPath Data Service so they can be consumed by Maestro workflows.
    """
    def __init__(self, governance_dir="../.agent_governance"):
        self.governance_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), governance_dir))
        self.uipath_connector = UiPathMaestroConnector()

    def parse_markdown_rules(self, file_name):
        """Extracts rule sections from the markdown file."""
        file_path = os.path.join(self.governance_dir, file_name)
        if not os.path.exists(file_path):
            print(f"[Warning] Governance file not found: {file_path}")
            return []

        rules = []
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Find bullet points or numbered lists that represent rules
            matches = re.findall(r'^[-\*]\s+(.*)$|^\d+\.\s+(.*)$', content, re.MULTILINE)
            for match in matches:
                rule_text = match[0] if match[0] else match[1]
                if rule_text.strip():
                    rules.append(rule_text.strip())
        
        return rules

    def sync_to_data_service(self):
        print(f"--- Universal Agent OS: Data Service Sync ---")
        print(f"Reading physical governance files from {self.governance_dir}...")
        
        # 1. Sync Code Soul (AGENT_OS_RULES.md)
        print("Parsing AGENT_OS_RULES.md...")
        code_soul_rules = self.parse_markdown_rules("AGENT_OS_RULES.md")
        if code_soul_rules:
            payload = {
                "Title": "Code Soul Core Principles",
                "RulesCount": len(code_soul_rules),
                "Rules": code_soul_rules[:10] # send top 10 for demo
            }
            res = self.uipath_connector.update_master_memory("CodeSoul", payload)
            print(f"  -> Synced Code Soul rules to Data Service. (Record ID: {res.get('record_id')})")
            
        # 2. Sync Minefield History (AGENT_MEMORY_AND_LESSONS.md)
        print("Parsing AGENT_MEMORY_AND_LESSONS.md...")
        memory_rules = self.parse_markdown_rules("AGENT_MEMORY_AND_LESSONS.md")
        if memory_rules:
            payload = {
                "Title": "Minefield History & Lessons Learned",
                "RulesCount": len(memory_rules),
                "Rules": memory_rules[:10]
            }
            res = self.uipath_connector.update_master_memory("MinefieldHistory", payload)
            print(f"  -> Synced Minefield History to Data Service. (Record ID: {res.get('record_id')})")

        print("--- Sync Complete ---")


if __name__ == "__main__":
    sync_service = GovernanceSyncService()
    sync_service.sync_to_data_service()

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from backend.uipath_api_connector import (
    UiPathMaestroConnector,
    UiPathConfigurationError,
    UiPathApiError,
)


def test_mock_mode_returns_explicit_mock_ids(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "true")
    connector = UiPathMaestroConnector()

    job = connector.start_maestro_process("DemoFlow", {"task": "demo"})
    assert job["mock"] is True
    assert job["job_id"].startswith("mock_job_")

    approval = connector.request_human_approval("Approve this test plan")
    assert approval["mock"] is True
    assert approval["task_id"].startswith("mock_task_")
    assert approval["approved"] is False

    memory = connector.update_master_memory("MinefieldHistory", {"lesson": "demo"})
    assert memory["mock"] is True
    assert memory["record_id"].startswith("mock_record_")

    records = connector.read_master_memory("MinefieldHistory")
    assert records["mock"] is True
    assert records["records"] == []

    decision = connector.get_human_approval(approval["task_id"])
    assert decision["completed"] is True
    assert decision["approved"] is True


def test_strict_real_mode_requires_env(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "false")
    monkeypatch.delenv("UIPATH_ORGANIZATION_NAME", raising=False)
    monkeypatch.delenv("UIPATH_TENANT_NAME", raising=False)
    monkeypatch.delenv("UIPATH_OU_ID", raising=False)
    monkeypatch.delenv("UIPATH_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("UIPATH_CLIENT_ID", raising=False)
    monkeypatch.delenv("UIPATH_CLIENT_SECRET", raising=False)

    with pytest.raises(UiPathConfigurationError):
        UiPathMaestroConnector()


def test_real_mode_never_falls_back_to_mock(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "false")
    monkeypatch.setenv("UIPATH_TENANT_NAME", "tenant")
    monkeypatch.setenv("UIPATH_OU_ID", "ou")
    monkeypatch.setenv("UIPATH_ACCESS_TOKEN", "token")
    monkeypatch.setenv("UIPATH_ORCHESTRATOR_ODATA_URL", "https://example.invalid/odata")

    connector = UiPathMaestroConnector()

    def fake_post(*args, **kwargs):
        raise RuntimeError("network down")

    monkeypatch.setattr("requests.post", fake_post)

    with pytest.raises(Exception):
        connector.start_maestro_process("DemoFlow", {"task": "demo"})


def test_completed_action_center_task_requires_explicit_approval(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "false")
    monkeypatch.setenv("UIPATH_TENANT_NAME", "tenant")
    monkeypatch.setenv("UIPATH_OU_ID", "ou")
    monkeypatch.setenv("UIPATH_ACCESS_TOKEN", "token")
    monkeypatch.setenv(
        "UIPATH_ACTION_CENTER_ODATA_URL",
        "https://example.invalid/odata",
    )

    connector = UiPathMaestroConnector()

    def fake_get(url, params=None):
        if url.endswith("/Tasks(42)"):
            return {
                "Title": "Phase-0 Alignment Review",
                "Status": "Completed",
                "IsCompleted": True,
            }
        assert params == {"taskId": "42"}
        return {
            "data": {
                "Approved": True,
                "ReviewerNotes": "Plan is safe.",
            },
            "action": "submit",
        }

    monkeypatch.setattr(connector, "_get", fake_get)
    decision = connector.get_human_approval("42")

    assert decision["completed"] is True
    assert decision["approved"] is True
    assert decision["reviewer_notes"] == "Plan is safe."


def test_pending_action_center_task_keeps_execution_blocked(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "false")
    monkeypatch.setenv("UIPATH_TENANT_NAME", "tenant")
    monkeypatch.setenv("UIPATH_OU_ID", "ou")
    monkeypatch.setenv("UIPATH_ACCESS_TOKEN", "token")
    monkeypatch.setenv(
        "UIPATH_ACTION_CENTER_ODATA_URL",
        "https://example.invalid/odata",
    )

    connector = UiPathMaestroConnector()
    monkeypatch.setattr(
        connector,
        "_get",
        lambda url, params=None: {
            "Title": "Phase-0 Alignment Review",
            "Status": "Unassigned",
            "IsCompleted": False,
        },
    )

    decision = connector.get_human_approval("43")

    assert decision["completed"] is False
    assert decision["approved"] is False


def test_approval_form_requires_explicit_checkbox(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "false")
    monkeypatch.setenv("UIPATH_TENANT_NAME", "tenant")
    monkeypatch.setenv("UIPATH_OU_ID", "ou")
    monkeypatch.setenv("UIPATH_ACCESS_TOKEN", "token")
    monkeypatch.setenv(
        "UIPATH_ACTION_CENTER_ODATA_URL",
        "https://example.invalid/odata",
    )

    connector = UiPathMaestroConnector()
    captured = {}

    def fake_post(url, payload):
        captured["url"] = url
        captured["payload"] = payload
        return {"id": 123}

    monkeypatch.setattr(connector, "_post", fake_post)
    approval = connector.request_human_approval("Start Phase 0 discovery.")

    components = {
        item["key"]: item
        for item in captured["payload"]["FormLayout"]["components"]
    }
    assert approval["task_id"] == "123"
    assert components["Approved"]["validate"]["required"] is True
    assert components["submit"]["action"] == "submit"
    assert components["submit"]["disableOnInvalid"] is True


def test_data_service_read_uses_official_response_shape(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "false")
    monkeypatch.setenv("UIPATH_TENANT_NAME", "tenant")
    monkeypatch.setenv("UIPATH_OU_ID", "ou")
    monkeypatch.setenv("UIPATH_ACCESS_TOKEN", "token")
    monkeypatch.setenv(
        "UIPATH_DATA_SERVICE_API_URL",
        "https://example.invalid/api/EntityService",
    )

    connector = UiPathMaestroConnector()

    def fake_get(url, params=None):
        assert url.endswith("/CodeSoul/read")
        assert params == {"start": 0, "limit": 2}
        return {
            "TotalRecordCount": 3,
            "Value": [{"Id": "1"}, {"Id": "2"}],
        }

    monkeypatch.setattr(connector, "_get", fake_get)
    result = connector.read_master_memory("CodeSoul", limit=2)

    assert result["count"] == 2
    assert result["records"] == [{"Id": "1"}, {"Id": "2"}]


def test_cloud_urls_use_separate_organization_and_tenant(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "false")
    monkeypatch.setenv("UIPATH_ORGANIZATION_NAME", "acme")
    monkeypatch.setenv("UIPATH_TENANT_NAME", "Production")
    monkeypatch.setenv("UIPATH_OU_ID", "ou")
    monkeypatch.setenv("UIPATH_ACCESS_TOKEN", "token")
    monkeypatch.delenv("UIPATH_ORCHESTRATOR_ODATA_URL", raising=False)
    monkeypatch.delenv("UIPATH_DATA_SERVICE_API_URL", raising=False)
    monkeypatch.delenv("UIPATH_ACTION_CENTER_ODATA_URL", raising=False)

    connector = UiPathMaestroConnector()

    assert connector.orchestrator_odata_url == (
        "https://cloud.uipath.com/acme/Production/orchestrator_/odata"
    )
    assert connector.action_center_odata_url == connector.orchestrator_odata_url


def test_memory_entity_api_names_are_configurable(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "true")
    monkeypatch.setenv("UIPATH_CODE_SOUL_ENTITY", "CodeSoulApiName")
    monkeypatch.setenv("UIPATH_MINEFIELD_ENTITY", "MinefieldApiName")
    monkeypatch.setenv("UIPATH_PERSONA_ENTITY", "PersonaApiName")
    monkeypatch.setenv("UIPATH_STATE_MEMORY_ENTITY", "StateApiName")

    connector = UiPathMaestroConnector()
    memories = connector.read_governance_memory(limit=1)

    assert connector.memory_entities == {
        "code_soul": "CodeSoulApiName",
        "minefield": "MinefieldApiName",
        "persona": "PersonaApiName",
        "state": "StateApiName",
    }
    assert set(memories) == {"code_soul", "minefield", "persona", "state"}

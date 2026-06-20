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

    memory = connector.update_master_memory("MinefieldHistory", {"lesson": "demo"})
    assert memory["mock"] is True
    assert memory["record_id"].startswith("mock_record_")


def test_strict_real_mode_requires_env(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "false")
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

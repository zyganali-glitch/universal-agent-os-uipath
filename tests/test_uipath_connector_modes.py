import os
import pytest

from backend.uipath_api_connector import (
    UiPathConfig,
    UiPathMaestroConnector,
    UiPathConfigurationError,
    UiPathApiError,
)

def test_mock_mode_returns_explicit_mock_ids(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "true")
    connector = UiPathMaestroConnector()
    result = connector.start_maestro_process("DemoFlow", {"task": "demo"})
    assert result["mock"] is True
    assert result["job_id"].startswith("mock_job_")

def test_strict_real_mode_requires_env(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "false")
    monkeypatch.delenv("UIPATH_TENANT_NAME", raising=False)
    monkeypatch.delenv("UIPATH_OU_ID", raising=False)
    monkeypatch.delenv("UIPATH_ACCESS_TOKEN", raising=False)

    with pytest.raises(UiPathConfigurationError):
        UiPathMaestroConnector()

def test_real_mode_never_falls_back_to_mock(monkeypatch):
    monkeypatch.setenv("UIPATH_MOCK_MODE", "false")
    monkeypatch.setenv("UIPATH_TENANT_NAME", "tenant")
    monkeypatch.setenv("UIPATH_OU_ID", "ou")
    monkeypatch.setenv("UIPATH_ACCESS_TOKEN", "token")

    connector = UiPathMaestroConnector()

    def fake_post(*args, **kwargs):
        raise RuntimeError("network down")

    monkeypatch.setattr("requests.post", fake_post)

    with pytest.raises(Exception):
        connector.start_maestro_process("DemoFlow", {"task": "demo"})

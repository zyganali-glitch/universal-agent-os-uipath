import json

import pytest

from backend import phase0_interview


def configure_paths(monkeypatch, tmp_path, gate_status="APPROVED"):
    gate_path = tmp_path / "gate.json"
    phase0_path = tmp_path / "phase0.json"
    gate_path.write_text(
        json.dumps({"task_id": "42", "status": gate_status}),
        encoding="utf-8",
    )
    monkeypatch.setattr(phase0_interview, "GATE_STATE_PATH", gate_path)
    monkeypatch.setattr(phase0_interview, "PHASE0_STATE_PATH", phase0_path)
    monkeypatch.setattr(phase0_interview, "ARTIFACT_DIR", tmp_path)
    return phase0_path


def test_phase0_cannot_start_before_verified_approval(monkeypatch, tmp_path):
    configure_paths(monkeypatch, tmp_path, gate_status="AWAITING_HUMAN")

    with pytest.raises(phase0_interview.Phase0Error):
        phase0_interview.start()


def test_phase0_asks_one_question_at_a_time(monkeypatch, tmp_path):
    configure_paths(monkeypatch, tmp_path)

    first = phase0_interview.start()
    second = phase0_interview.answer("Mahalle esnafı için kolay sipariş sistemi")

    assert first["question_number"] == 1
    assert first["id"] == "project_idea"
    assert second["question_number"] == 2
    assert second["id"] == "target_users"


def test_phase0_completes_and_persists_contract(monkeypatch, tmp_path):
    phase0_path = configure_paths(monkeypatch, tmp_path)
    phase0_interview.start()

    result = None
    for index in range(len(phase0_interview.QUESTIONS)):
        result = phase0_interview.answer(f"answer-{index}")

    state = json.loads(phase0_path.read_text(encoding="utf-8"))
    assert result["phase0_status"] == "PHASE0_COMPLETE"
    assert state["status"] == "PHASE0_COMPLETE"
    assert len(state["answers"]) == len(phase0_interview.QUESTIONS)

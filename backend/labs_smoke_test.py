import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from uipath_api_connector import (
    UiPathApiError,
    UiPathConfigurationError,
    UiPathMaestroConnector,
)


ARTIFACT_DIR = Path("run_artifacts")
GATE_STATE_PATH = ARTIFACT_DIR / "approval_gate.sanitized.json"
RESULT_PATH = ARTIFACT_DIR / "labs_smoke_result.sanitized.json"
PHASE0_STATE_PATH = ARTIFACT_DIR / "phase0_contract.sanitized.json"
DEFAULT_TASK = "Add Stripe payment integration with idempotency guard"


def sanitize(value):
    if isinstance(value, dict):
        return {
            key: sanitize(item)
            for key, item in value.items()
            if "token" not in key.lower() and "authorization" not in key.lower()
        }
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    return value


def write_json(path: Path, payload):
    ARTIFACT_DIR.mkdir(exist_ok=True)
    path.write_text(
        json.dumps(sanitize(payload), indent=2),
        encoding="utf-8",
    )


def print_and_save(result):
    write_json(RESULT_PATH, result)
    print(json.dumps(sanitize(result), indent=2))


def register_gate(connector: UiPathMaestroConnector, task_description: str):
    if PHASE0_STATE_PATH.exists():
        PHASE0_STATE_PATH.unlink()

    result = {
        "mode": "MOCK" if connector.mock_mode else "STRICT_REAL",
        "command": "register",
        "steps": [],
        "success": False,
    }

    code_soul = connector.read_master_memory("CodeSoul", limit=10)
    minefields = connector.read_master_memory("MinefieldHistory", limit=10)
    result["steps"].append(
        {
            "step": "read_master_memory",
            "result": {
                "code_soul_count": code_soul["count"],
                "minefield_count": minefields["count"],
                "mock": connector.mock_mode,
            },
        }
    )

    job = connector.start_maestro_process(
        "UniversalAgentOS_Phase0_Flow",
        {
            "task": task_description,
            "codeSoulCount": code_soul["count"],
            "minefieldCount": minefields["count"],
        },
    )
    result["steps"].append(
        {"step": "start_maestro_process", "result": sanitize(job)}
    )

    plan = (
        f"Requested task: {task_description}\n"
        f"Loaded Code Soul records: {code_soul['count']}\n"
        f"Loaded Minefield History records: {minefields['count']}\n"
        "Proposed plan: inspect the existing payment module, enforce "
        "idempotency, add tests, and make no code changes until this "
        "Action Center decision is verified through the UiPath API."
    )
    approval = connector.request_human_approval(plan)
    result["steps"].append(
        {"step": "request_human_approval", "result": sanitize(approval)}
    )

    task_id = str(approval["task_id"])
    gate_state = {
        "task_id": task_id,
        "task_description": task_description,
        "mode": result["mode"],
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "status": "AWAITING_HUMAN",
    }
    write_json(GATE_STATE_PATH, gate_state)

    result.update(
        {
            "success": True,
            "gate_status": "AWAITING_HUMAN",
            "task_id": task_id,
            "next_command": "python backend/labs_smoke_test.py verify",
            "message": (
                "No execution permission has been granted. Complete the "
                "Action Center task, then run the verification command."
            ),
        }
    )
    return result


def load_gate_state():
    if not GATE_STATE_PATH.exists():
        raise UiPathConfigurationError(
            "No approval gate state found. Run "
            "'python backend/labs_smoke_test.py register' first."
        )
    return json.loads(GATE_STATE_PATH.read_text(encoding="utf-8"))


def verify_gate(connector: UiPathMaestroConnector, task_id=None):
    gate_state = load_gate_state()
    resolved_task_id = str(task_id or gate_state["task_id"])
    if resolved_task_id != str(gate_state["task_id"]):
        raise UiPathConfigurationError(
            "The requested task ID does not match the registered gate."
        )
    if gate_state.get("status") != "AWAITING_HUMAN":
        raise UiPathConfigurationError(
            f"Approval gate is already finalized as {gate_state.get('status')}."
        )
    decision = connector.get_human_approval(resolved_task_id)

    result = {
        "mode": "MOCK" if connector.mock_mode else "STRICT_REAL",
        "command": "verify",
        "task_id": resolved_task_id,
        "steps": [
            {
                "step": "verify_human_approval",
                "result": sanitize(decision),
            }
        ],
        "success": False,
    }

    if not decision["completed"]:
        result.update(
            {
                "gate_status": "AWAITING_HUMAN",
                "message": (
                    "The Action Center task is not completed. Execution "
                    "remains blocked."
                ),
            }
        )
        return result, 2

    if decision["title"] != "Phase-0 Alignment Review":
        raise UiPathConfigurationError(
            "The completed task is not a Universal Agent OS approval task."
        )

    if not decision["approved"]:
        rejection = connector.update_master_memory(
            "MinefieldHistory",
            {
                "MinefieldId": f"REJECT-{resolved_task_id}"[-20:],
                "Lesson": (
                    decision["reviewer_notes"]
                    or "The proposed coding plan was rejected by a human reviewer."
                ),
                "Severity": "high",
                "OriginAgent": "labs_smoke_test",
                "AffectedModules": "[\"payments\", \"checkout\"]",
                "DateDiscovered": datetime.now(timezone.utc).isoformat(),
                "IsActive": True,
            },
        )
        result["steps"].append(
            {"step": "record_rejection", "result": sanitize(rejection)}
        )
        gate_state["status"] = "REJECTED"
        write_json(GATE_STATE_PATH, gate_state)
        result.update(
            {
                "gate_status": "REJECTED",
                "message": "Human rejected the plan. Execution remains blocked.",
            }
        )
        return result, 1

    execution_grant = connector.update_master_memory(
        "StateMemory",
        {
            "SessionCount": 1,
            "LastTaskDescription": gate_state["task_description"],
            "LastAgentUsed": "Universal Agent OS",
            "LastResult": "approved",
            "TaskHistory": json.dumps(
                [
                    {
                        "task": gate_state["task_description"],
                        "agent": "Universal Agent OS",
                        "result": "approved",
                        "action_center_task_id": resolved_task_id,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                ]
            ),
            "CreatedAt": gate_state["registered_at"],
            "UpdatedAt": datetime.now(timezone.utc).isoformat(),
        },
    )
    result["steps"].append(
        {"step": "persist_execution_grant", "result": sanitize(execution_grant)}
    )

    gate_state.update(
        {
            "status": "APPROVED",
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    write_json(GATE_STATE_PATH, gate_state)
    result.update(
        {
            "success": True,
            "gate_status": "APPROVED",
            "message": (
                "UiPath API verification succeeded. Phase-0 scoping may begin."
            ),
        }
    )
    return result, 0


def parse_args():
    parser = argparse.ArgumentParser(
        description="Register and verify the Universal Agent OS approval gate."
    )
    subparsers = parser.add_subparsers(dest="command")

    register = subparsers.add_parser(
        "register",
        help="Read governance memory, start the process, and create a gate.",
    )
    register.add_argument("--task", default=DEFAULT_TASK)

    verify = subparsers.add_parser(
        "verify",
        help="Verify the Action Center decision through the UiPath API.",
    )
    verify.add_argument("--task-id")

    wait = subparsers.add_parser(
        "wait",
        help="Poll until the Action Center task is completed.",
    )
    wait.add_argument("--task-id")
    wait.add_argument("--timeout", type=int, default=900)
    wait.add_argument("--poll-interval", type=int, default=5)

    return parser.parse_args()


def main():
    args = parse_args()
    command = args.command or "register"

    try:
        connector = UiPathMaestroConnector()

        if command == "register":
            result = register_gate(connector, getattr(args, "task", DEFAULT_TASK))
            print_and_save(result)
            return

        if command == "wait":
            gate_state = load_gate_state()
            task_id = str(args.task_id or gate_state["task_id"])
            connector.wait_for_human_approval(
                task_id,
                timeout_seconds=args.timeout,
                poll_interval_seconds=args.poll_interval,
            )

        result, exit_code = verify_gate(
            connector,
            getattr(args, "task_id", None),
        )
        print_and_save(result)
        raise SystemExit(exit_code)

    except (UiPathConfigurationError, UiPathApiError, ValueError) as exc:
        result = {
            "command": command,
            "success": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
        print_and_save(result)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

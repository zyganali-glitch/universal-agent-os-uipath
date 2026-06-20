import json
import os
from pathlib import Path

from uipath_api_connector import UiPathMaestroConnector, UiPathApiError, UiPathConfigurationError


def sanitize(value):
    if isinstance(value, dict):
        return {k: sanitize(v) for k, v in value.items() if "token" not in k.lower() and "authorization" not in k.lower()}
    if isinstance(value, list):
        return [sanitize(v) for v in value]
    return value


def main():
    out_dir = Path("run_artifacts")
    out_dir.mkdir(exist_ok=True)

    result = {
        "mode": None,
        "steps": [],
        "success": False,
    }

    try:
        connector = UiPathMaestroConnector()
        result["mode"] = "MOCK" if connector.mock_mode else "STRICT_REAL"

        job = connector.start_maestro_process(
            "UniversalAgentOS_Phase0_Flow",
            {"task": "Add Stripe payment integration with idempotency guard"},
        )
        result["steps"].append({"step": "start_maestro_process", "result": sanitize(job)})

        approval = connector.request_human_approval(
            "Agent proposes to inspect existing payment module, enforce idempotency, add tests, and wait for approval before code execution."
        )
        result["steps"].append({"step": "request_human_approval", "result": sanitize(approval)})

        memory = connector.update_master_memory(
            "MinefieldHistory",
            {
                "MinefieldId": "MF-SMOKE-001",
                "Lesson": "Payment integrations require idempotency checks before implementation.",
                "Severity": "high",
                "OriginAgent": "labs_smoke_test",
                "AffectedModules": "[\"payments\", \"checkout\"]",
                "IsActive": True,
            },
        )
        result["steps"].append({"step": "update_master_memory", "result": sanitize(memory)})
        result["success"] = True

    except (UiPathConfigurationError, UiPathApiError, Exception) as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["success"] = False

    output_path = out_dir / "labs_smoke_result.sanitized.json"
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

    if result["mode"] == "STRICT_REAL" and not result["success"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

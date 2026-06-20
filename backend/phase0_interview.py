import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ARTIFACT_DIR = Path("run_artifacts")
GATE_STATE_PATH = ARTIFACT_DIR / "approval_gate.sanitized.json"
PHASE0_STATE_PATH = ARTIFACT_DIR / "phase0_contract.sanitized.json"

QUESTIONS = [
    {
        "id": "project_idea",
        "question": "Ne yapmak istiyorsun? Fikrini günlük dille bir veya iki cümleyle anlat.",
        "example": "Örnek: Mahalledeki kayıp hayvanları sahipleriyle buluşturan kolay bir sistem.",
        "default": "Henüz net değilse, çözmek istediğin problemi anlatman yeterli.",
    },
    {
        "id": "target_users",
        "question": "Bunu en çok kim kullanacak?",
        "example": "Örnek: küçük işletme sahipleri, öğrenciler veya yalnızca şirket çalışanları.",
        "default": "Emin değilsen, ilk sürümü tek ve net bir kullanıcı grubu için hazırlamayı öneririm.",
    },
    {
        "id": "usage_place",
        "question": "İnsanlar bunu en rahat nerede kullanmalı?",
        "example": "İnternet sitesi, telefon uygulaması, bilgisayar programı veya 'emin değilim' diyebilirsin.",
        "default": "Emin değilsen, kurulumsuz açıldığı için internet sitesiyle başlamayı öneririm.",
    },
    {
        "id": "accounts_and_privacy",
        "question": "Kullanıcıların hesap açması veya özel bilgi saklaması gerekiyor mu?",
        "example": "Örnek: e-posta ile giriş, adres, ödeme bilgisi; ya da hiçbiri.",
        "default": "Gerekmiyorsa hesap ve özel veri toplamadan başlamayı öneririm.",
    },
    {
        "id": "business_model",
        "question": "Bu proje ücretsiz mi olacak, para kazandıracak mı, yoksa şimdilik karar vermedin mi?",
        "example": "Örnek: tamamen ücretsiz, aylık üyelik, işletmelere satış veya emin değilim.",
        "default": "Emin değilsen, ilk çalışan sürümü ücretsiz doğrulamayı öneririm.",
    },
    {
        "id": "language",
        "question": "İlk sürüm hangi dilde kullanılacak?",
        "example": "Yalnızca Türkçe, yalnızca İngilizce veya birden fazla dil.",
        "default": "İlk kullanıcıların Türkiye'deyse yalnızca Türkçeyle başlamayı öneririm.",
    },
    {
        "id": "visual_style",
        "question": "Proje kullanıcıya nasıl hissettirmeli?",
        "example": "Sade ve güvenilir, eğlenceli ve renkli, ciddi ve kurumsal veya emin değilim.",
        "default": "Emin değilsen, sade ve güvenilir bir görünüm öneririm.",
    },
    {
        "id": "first_success",
        "question": "İlk çalışan sürümde kullanıcı hangi tek işi başarabilirse 'bu proje çalışıyor' dersin?",
        "example": "Örnek: ilan oluşturmak, randevu almak veya bir raporu indirmek.",
        "default": "Tek bir ana işi kusursuz tamamlayan küçük bir ilk sürüm öneririm.",
    },
]


class Phase0Error(RuntimeError):
    pass


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload):
    ARTIFACT_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def require_approved_gate():
    if not GATE_STATE_PATH.exists():
        raise Phase0Error(
            "No UiPath approval gate exists. Register and verify the gate first."
        )
    gate = load_json(GATE_STATE_PATH)
    if gate.get("status") != "APPROVED":
        raise Phase0Error(
            f"UiPath gate is {gate.get('status', 'UNKNOWN')}; Phase-0 remains blocked."
        )
    return gate


def question_payload(index: int):
    question = QUESTIONS[index]
    return {
        "phase0_status": "IN_PROGRESS",
        "question_number": index + 1,
        "total_questions": len(QUESTIONS),
        **question,
    }


def start():
    gate = require_approved_gate()
    if PHASE0_STATE_PATH.exists():
        state = load_json(PHASE0_STATE_PATH)
        if state.get("status") == "PHASE0_COMPLETE":
            return {
                "phase0_status": "PHASE0_COMPLETE",
                "answers": state["answers"],
                "message": "Phase-0 is already complete.",
            }
        return question_payload(state["current_question_index"])

    state = {
        "status": "IN_PROGRESS",
        "action_center_task_id": gate["task_id"],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "current_question_index": 0,
        "answers": {},
    }
    save_json(PHASE0_STATE_PATH, state)
    return question_payload(0)


def answer(value: str):
    require_approved_gate()
    if not value.strip():
        raise Phase0Error("The answer cannot be empty.")
    if not PHASE0_STATE_PATH.exists():
        raise Phase0Error("Phase-0 has not started.")

    state = load_json(PHASE0_STATE_PATH)
    if state.get("status") == "PHASE0_COMPLETE":
        raise Phase0Error("Phase-0 is already complete.")

    index = state["current_question_index"]
    question = QUESTIONS[index]
    state["answers"][question["id"]] = value.strip()
    next_index = index + 1

    if next_index >= len(QUESTIONS):
        state.update(
            {
                "status": "PHASE0_COMPLETE",
                "current_question_index": next_index,
                "completed_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        save_json(PHASE0_STATE_PATH, state)
        return {
            "phase0_status": "PHASE0_COMPLETE",
            "answers": state["answers"],
            "message": (
                "Phase-0 contract is complete. Summarize the decisions and create "
                "the implementation plan before writing product code."
            ),
        }

    state["current_question_index"] = next_index
    save_json(PHASE0_STATE_PATH, state)
    return question_payload(next_index)


def status():
    gate = require_approved_gate()
    if not PHASE0_STATE_PATH.exists():
        return {
            "phase0_status": "NOT_STARTED",
            "action_center_task_id": gate["task_id"],
        }
    return load_json(PHASE0_STATE_PATH)


def parse_args():
    parser = argparse.ArgumentParser(description="Universal Agent OS Phase-0 interview")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("start")
    answer_parser = subparsers.add_parser("answer")
    answer_parser.add_argument("--value", required=True)
    subparsers.add_parser("status")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        if args.command == "start":
            result = start()
        elif args.command == "answer":
            result = answer(args.value)
        else:
            result = status()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Phase0Error as exc:
        print(
            json.dumps(
                {"success": False, "error": str(exc)},
                indent=2,
                ensure_ascii=False,
            )
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()

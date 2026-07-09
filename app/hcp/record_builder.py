from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _clean_text(value: object) -> str:
    if value is None:
        return ""

    return str(value).strip()


def _clean_optional_text(value: object) -> str | None:
    text = _clean_text(value)

    if not text:
        return None

    return text


def _clean_age(value: object) -> int | None:
    try:
        age = int(value)
    except (TypeError, ValueError):
        return None

    if age <= 0:
        return None

    return age


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_hcp_record(user_data: dict[str, Any]) -> dict[str, Any]:
    """
    Builds a canonical HCP Humanitarian Record from Telegram conversation data.

    This function is the boundary between the Telegram form and the HCP record
    format. Telegram-specific state should not leak beyond this point.
    """

    subject_type = user_data.get("subject_type", "human")

    base_record: dict[str, Any] = {
        "id": str(uuid4()),
        "schema_version": "0.1",
        "created_at": _now_iso(),
        "source_client": "hcp-client-telegram",
        "subject_type": subject_type,
        "event_type": _clean_text(user_data.get("event_type")),
        "status": "reported",
        "reported_name": _clean_text(user_data.get("reported_name")),
        "reported_location": _clean_text(user_data.get("reported_location")),
        "recognition_features": _clean_text(
            user_data.get("recognition_features")
        ),
        "source": _clean_text(user_data.get("source")),
    }

    if subject_type == "animal":
        base_record.update(
            {
                "animal_species": _clean_text(user_data.get("animal_species")),
                "animal_size": _clean_text(user_data.get("animal_size")),
                "animal_breed": _clean_text(user_data.get("animal_breed")),
            }
        )
    else:
        base_record["estimated_age"] = _clean_age(
            user_data.get("estimated_age")
        )

    return base_record

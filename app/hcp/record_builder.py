from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


SCHEMA_VERSION = "0.3"
SOURCE_CLIENT = "hcp-client-telegram"


HUMAN_EVENT_TYPES = {
    "missing": "missing_person",
    "hospitalized": "hospitalized_person",
    "sheltered": "sheltered_person",
    "safe": "safe_person",
}


ANIMAL_EVENT_TYPES = {
    "missing": "missing_animal",
    "found": "found_animal",
}


def _clean_text(value: object) -> str:
    """
    Converts a value to a stripped string.

    Returns an empty string when the value is missing.
    """

    if value is None:
        return ""

    return str(value).strip()


def _clean_optional_text(value: object) -> str | None:
    """
    Cleans an optional text field.

    Returns None when no meaningful value is available.
    """

    text = _clean_text(value)

    if not text:
        return None

    if text.lower() in {
        "omitir",
        "omit",
        "ninguno",
        "ninguna",
        "none",
    }:
        return None

    return text


def _clean_age(value: object) -> int | None:
    """
    Converts the estimated age to a positive integer.

    Invalid, missing or non-positive values are omitted.
    """

    try:
        age = int(value)
    except (TypeError, ValueError):
        return None

    if age <= 0:
        return None

    return age


def _now_iso() -> str:
    """
    Returns the current UTC timestamp in ISO 8601 format.
    """

    return datetime.now(timezone.utc).isoformat()


def _normalize_subject_type(value: object) -> str:
    """
    Normalizes Telegram subject values to canonical HCP values.
    """

    subject_type = _clean_text(value).lower()

    if subject_type in {"animal"}:
        return "animal"

    return "human"


def _normalize_event_type(
    subject_type: str,
    event_type: object,
) -> str:
    """
    Converts Telegram event callbacks into canonical HCP event types.

    Examples:

    human + missing -> missing_person
    animal + missing -> missing_animal
    animal + found -> found_animal
    """

    event = _clean_text(event_type).lower()

    if subject_type == "animal":
        return ANIMAL_EVENT_TYPES.get(event, event)

    return HUMAN_EVENT_TYPES.get(event, event)


def _remove_empty_optional_fields(
    record: dict[str, Any],
) -> dict[str, Any]:
    """
    Removes optional fields whose value is None.

    Empty required text fields are preserved so validation problems remain
    visible during development.
    """

    return {
        key: value
        for key, value in record.items()
        if value is not None
    }


def build_hcp_record(
    user_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Builds a canonical HCP Humanitarian Record from Telegram conversation data.

    This function is the boundary between the Telegram user experience and the
    canonical HCP representation.

    Telegram-specific state names and callback values must not leak beyond
    this function.
    """

    subject_type = _normalize_subject_type(
        user_data.get("subject_type")
    )

    event_type = _normalize_event_type(
        subject_type=subject_type,
        event_type=user_data.get("event_type"),
    )

    record: dict[str, Any] = {
        "id": str(uuid4()),
        "schema_version": SCHEMA_VERSION,
        "source_client": SOURCE_CLIENT,
        "subject_type": subject_type,
        "event_type": event_type,
        "status": "reported",
        "reported_name": _clean_text(
            user_data.get("reported_name")
        ),
        "reported_location": _clean_text(
            user_data.get("reported_location")
        ),
        "recognition_features": _clean_text(
            user_data.get("recognition_features")
        ),
        "public_contact": _clean_optional_text(
            user_data.get("public_contact")
        ),
        "source": _clean_text(
            user_data.get("source")
        ),
        "created_at": _now_iso(),
    }

    if subject_type == "animal":
        record.update(
            {
                "animal_species": _clean_text(
                    user_data.get("animal_species")
                ),
                "animal_size": _clean_optional_text(
                    user_data.get("animal_size")
                ),
                "animal_breed": _clean_optional_text(
                    user_data.get("animal_breed")
                ),
            }
        )
    else:
        record["estimated_age"] = _clean_age(
            user_data.get("estimated_age")
        )

    return _remove_empty_optional_fields(record)

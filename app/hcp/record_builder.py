from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


SCHEMA_VERSION = "0.5"
SOURCE_CLIENT = "hcp-client-telegram"


HUMAN_EVENT_TYPES = {
    "missing": "missing",
    "hospitalized": "hospitalized",
    "sheltered": "sheltered",
    "safe": "safe",
    "public_emergency": "public_emergency",
}


ANIMAL_EVENT_TYPES = {
    "missing": "missing",
    "found": "found",
}


REPORTED_BY_TYPES = {
    "family": "family",
    "hospital": "hospital",
    "firefighters": "firefighters",
    "volunteer": "volunteer",
    "police": "police",
    "friend": "friend",
    "known_person": "known_person",
    "unknown": "unknown",
}


def _clean_text(value: object) -> str:
    """
    Convert a value to a stripped string.

    Return an empty string when the value is missing.
    """
    if value is None:
        return ""

    return str(value).strip()


def _clean_optional_text(value: object) -> str | None:
    """
    Clean an optional text field.

    Return None when no meaningful value is available.
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
    Convert the estimated age to a non-negative integer.

    Invalid or missing values are omitted.
    """
    try:
        age = int(value)
    except (TypeError, ValueError):
        return None

    if age < 0:
        return None

    return age


def _now_iso() -> str:
    """
    Return the current UTC timestamp in canonical RFC 3339 format.
    """
    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _normalize_subject_type(value: object) -> str:
    """
    Normalize Telegram subject values to canonical HCP values.
    """
    subject_type = _clean_text(value).lower()

    if subject_type == "animal":
        return "animal"

    return "human"


def _normalize_event_type(
    subject_type: str,
    event_type: object,
) -> str:
    """
    Convert Telegram event callbacks into canonical HCP event tokens.
    """
    event = _clean_text(event_type).lower()

    if subject_type == "animal":
        return ANIMAL_EVENT_TYPES.get(event, event)

    return HUMAN_EVENT_TYPES.get(event, event)


def _normalize_reported_by(value: object) -> str:
    """
    Normalize Telegram reporter values to canonical HCP tokens.

    The fallback value keeps the record valid when a legacy or incomplete
    conversation state does not contain a recognized reporter value.
    """
    reported_by = _clean_text(value).lower()

    if not reported_by:
        return "unknown"

    return REPORTED_BY_TYPES.get(
        reported_by,
        reported_by,
    )


def _remove_none_values(
    data: dict[str, Any],
) -> dict[str, Any]:
    """
    Remove optional fields whose value is None.

    Empty required strings are preserved so validation problems remain
    visible during development and testing.
    """
    return {
        key: value
        for key, value in data.items()
        if value is not None
    }


def _build_human_subject(
    user_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Build the canonical Subject section for a human.
    """
    return _remove_none_values(
        {
            "type": "human",
            "reported_label": _clean_optional_text(
                user_data.get("reported_name")
            ),
            "estimated_age": _clean_age(
                user_data.get("estimated_age")
            ),
            "recognition_features": _clean_optional_text(
                user_data.get("recognition_features")
            ),
        }
    )


def _build_animal_subject(
    user_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Build the canonical Subject section for an animal.

    Animal-specific properties are preserved as compatible HCP extension
    fields supported by the reference implementation.
    """
    return _remove_none_values(
        {
            "type": "animal",
            "reported_label": _clean_optional_text(
                user_data.get("reported_name")
            ),
            "recognition_features": _clean_optional_text(
                user_data.get("recognition_features")
            ),
            "species": _clean_optional_text(
                user_data.get("

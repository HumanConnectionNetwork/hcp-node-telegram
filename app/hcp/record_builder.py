from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


SCHEMA_VERSION = "0.5"
SOURCE_CLIENT = "hcp-client-telegram"


HUMAN_EVENT_TYPES = {
    "missing": "missing_report",
    "hospitalized": "hospital_admission",
    "sheltered": "shelter_registration",
    "safe": "safe",
    "public_emergency": "public_emergency",
}


ANIMAL_EVENT_TYPES = {
    "missing": "animal_missing",
    "found": "animal_found",
}


REPORTER_TYPES = {
    "family": "family",
    "hospital": "hospital",
    "fire_department": "fire_department",
    "volunteer": "volunteer",
    "police": "police",
    "friend": "friend",
    "unknown": "unknown",
}


EMPTY_OPTIONAL_VALUES = {
    "",
    "omitir",
    "omit",
    "ninguno",
    "ninguna",
    "none",
    "null",
}


def _clean_text(value: object) -> str:
    """
    Convert an arbitrary value to stripped text.

    An empty string is returned when the value is missing.
    """
    if value is None:
        return ""

    return str(value).strip()


def _clean_optional_text(value: object) -> str | None:
    """
    Normalize optional text.

    Values representing omission are converted to None so they are not
    included in the canonical Humanitarian Record.
    """
    text = _clean_text(value)

    if text.lower() in EMPTY_OPTIONAL_VALUES:
        return None

    return text


def _clean_age(value: object) -> int | None:
    """
    Convert an estimated age to a non-negative integer.

    Missing or invalid values are omitted. Zero is accepted because HCP allows
    an estimated age greater than or equal to zero.
    """
    if value is None:
        return None

    try:
        age = int(value)
    except (TypeError, ValueError):
        return None

    if age < 0:
        return None

    return age


def _now_iso() -> str:
    """
    Return the current UTC timestamp using the RFC 3339 Z suffix.
    """
    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _normalize_timestamp(value: object) -> str:
    """
    Normalize an optional timestamp to an RFC 3339-compatible UTC value.

    Telegram currently creates observations at submission time. The function
    also accepts an existing ISO 8601 timestamp for future compatibility.
    """
    text = _clean_text(value)

    if not text:
        return _now_iso()

    try:
        parsed = datetime.fromisoformat(
            text.replace("Z", "+00:00")
        )
    except ValueError:
        return _now_iso()

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return (
        parsed.astimezone(timezone.utc)
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
    Convert Telegram callback values to canonical HCP Event Types.

    Unknown valid values are preserved to support protocol extensibility.
    """
    event = _clean_text(event_type).lower()

    if subject_type == "animal":
        return ANIMAL_EVENT_TYPES.get(event, event)

    return HUMAN_EVENT_TYPES.get(event, event)


def _normalize_reported_by(value: object) -> str:
    """
    Normalize the Telegram reporter source to an HCP canonical token.

    The Observation model requires reported_by, so unknown or missing values
    fall back to the canonical token "unknown".
    """
    reporter = _clean_text(value).lower()

    if not reporter:
        return "unknown"

    return REPORTER_TYPES.get(reporter, reporter)


def _remove_none_values(
    data: dict[str, Any],
) -> dict[str, Any]:
    """
    Remove optional fields whose value is None.

    Empty required fields are preserved so validation errors remain visible
    instead of being silently hidden.
    """
    return {
        key: value
        for key, value in data.items()
        if value is not None
    }


def _build_subject(
    user_data: dict[str, Any],
    subject_type: str,
) -> dict[str, Any]:
    """
    Build the canonical HCP Subject section.

    Animal-specific properties are preserved as compatible extension fields
    because HCP allows additional Subject properties.
    """
    subject: dict[str, Any] = {
        "type": subject_type,
        "reported_label": _clean_optional_text(
            user_data.get("reported_name")
        ),
        "recognition_features": _clean_optional_text(
            user_data.get("recognition_features")
        ),
    }

    if subject_type == "human":
        subject["estimated_age"] = _clean_age(
            user_data.get("estimated_age")
        )

    if subject_type == "animal":
        subject.update(
            {
                "species": _clean_optional_text(
                    user_data.get("animal_species")
                ),
                "size": _clean_optional_text(
                    user_data.get("animal_size")
                ),
                "breed": _clean_optional_text(
                    user_data.get("animal_breed")
                ),
            }
        )

    return _remove_none_values(subject)


def _build_observation(
    user_data: dict[str, Any],
    event_type: str,
) -> dict[str, Any]:
    """
    Build the canonical HCP Observation section.
    """
    observation: dict[str, Any] = {
        "event_type": event_type,
        "reported_location": _clean_optional_text(
            user_data.get("reported_location")
        ),
        "reported_by": _normalize_reported_by(
            user_data.get("source")
        ),
        "observed_at": _normalize_timestamp(
            user_data.get("observed_at")
        ),
        "public_contact": _clean_optional_text(
            user_data.get("public_contact")
        ),
    }

    return _remove_none_values(observation)


def build_hcp_record(
    user_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Build one canonical HCP Humanitarian Record from Telegram conversation data.

    This function is the boundary between Telegram-specific conversation
    state and the protocol representation exchanged with HCP Nodes.

    Telegram callback names, temporary state values and presentation labels
    must not leak beyond this function.
    """
    subject_type = _normalize_subject_type(
        user_data.get("subject_type")
    )

    event_type = _normalize_event_type(
        subject_type=subject_type,
        event_type=user_data.get("event_type"),
    )

    return {
        "id": str(uuid4()),
        "schema_version": SCHEMA_VERSION,
        "source_client": SOURCE_CLIENT,
        "subject": _build_subject(
            user_data=user_data,
            subject_type=subject_type,
        ),
        "observation": _build_observation(
            user_data=user_data,
            event_type=event_type,
        ),
    }

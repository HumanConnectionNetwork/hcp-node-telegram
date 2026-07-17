from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class HumanitarianSubject:
    """
    Subject described by a Humanitarian Record.

    The subject contains descriptive and correlation-related attributes.
    It does not represent a verified identity.
    """

    type: str

    reported_label: str | None = None
    estimated_age: int | None = None
    recognition_features: str | None = None

    species: str | None = None
    size: str | None = None
    breed: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """
        Return the subject as a dictionary without empty optional fields.
        """
        return {
            key: value
            for key, value in asdict(self).items()
            if value is not None
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "HumanitarianSubject":
        """
        Create a HumanitarianSubject from canonical HCP data.
        """
        return cls(
            type=str(data.get("type", "")).strip(),
            reported_label=_optional_text(
                data.get("reported_label")
            ),
            estimated_age=_optional_integer(
                data.get("estimated_age")
            ),
            recognition_features=_optional_text(
                data.get("recognition_features")
            ),
            species=_optional_text(
                data.get("species")
            ),
            size=_optional_text(
                data.get("size")
            ),
            breed=_optional_text(
                data.get("breed")
            ),
        )


@dataclass
class HumanitarianObservation:
    """
    Humanitarian observation associated with a subject.

    An observation describes what was reported, where it was observed,
    who reported it and when it was observed.
    """

    event_type: str
    reported_by: str
    observed_at: str

    reported_location: str | None = None
    public_contact: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """
        Return the observation as a dictionary without empty optional fields.
        """
        return {
            key: value
            for key, value in asdict(self).items()
            if value is not None
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "HumanitarianObservation":
        """
        Create a HumanitarianObservation from canonical HCP data.
        """
        return cls(
            event_type=str(
                data.get("event_type", "")
            ).strip(),
            reported_by=str(
                data.get("reported_by", "unknown")
            ).strip(),
            observed_at=str(
                data.get("observed_at", "")
            ).strip(),
            reported_location=_optional_text(
                data.get("reported_location")
            ),
            public_contact=_optional_text(
                data.get("public_contact")
            ),
        )


@dataclass
class HumanitarianRecord:
    """
    Canonical Humanitarian Record used by the Telegram client.

    A Humanitarian Record represents one humanitarian observation about
    a human or animal.

    It is not an identity record, does not confirm that multiple observations
    refer to the same subject and must not be treated as a personal history.
    """

    id: str
    schema_version: str
    source_client: str

    subject: HumanitarianSubject
    observation: HumanitarianObservation

    extensions: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Return the complete canonical Humanitarian Record as a dictionary.
        """
        record: dict[str, Any] = {
            "id": self.id,
            "schema_version": self.schema_version,
            "source_client": self.source_client,
            "subject": self.subject.to_dict(),
            "observation": self.observation.to_dict(),
        }

        if self.extensions:
            record.update(self.extensions)

        return record

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "HumanitarianRecord":
        """
        Create a HumanitarianRecord from canonical HCP data.

        Unknown top-level fields are preserved in extensions so compatible
        protocol additions are not silently discarded.
        """
        known_fields = {
            "id",
            "schema_version",
            "source_client",
            "subject",
            "observation",
        }

        extensions = {
            key: value
            for key, value in data.items()
            if key not in known_fields
        }

        subject_data = data.get("subject", {})
        observation_data = data.get("observation", {})

        if not isinstance(subject_data, dict):
            subject_data = {}

        if not isinstance(observation_data, dict):
            observation_data = {}

        return cls(
            id=str(data.get("id", "")).strip(),
            schema_version=str(
                data.get("schema_version", "")
            ).strip(),
            source_client=str(
                data.get("source_client", "")
            ).strip(),
            subject=HumanitarianSubject.from_dict(
                subject_data
            ),
            observation=HumanitarianObservation.from_dict(
                observation_data
            ),
            extensions=extensions,
        )


def _optional_text(value: object) -> str | None:
    """
    Normalize optional text values.
    """
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    return text


def _optional_integer(value: object) -> int | None:
    """
    Normalize optional integer values.
    """
    if value is None:
        return None

    try:
        integer = int(value)
    except (TypeError, ValueError):
        return None

    if integer < 0:
        return None

    return integer

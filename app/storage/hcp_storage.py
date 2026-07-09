import json
from pathlib import Path
from typing import Any


DATA_DIR = Path("data")
RECORDS_FILE = DATA_DIR / "hcp_records.json"


def ensure_storage_exists() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    if not RECORDS_FILE.exists():
        RECORDS_FILE.write_text("[]", encoding="utf-8")


def load_records() -> list[dict[str, Any]]:
    ensure_storage_exists()

    try:
        content = RECORDS_FILE.read_text(encoding="utf-8")
        records = json.loads(content)

        if isinstance(records, list):
            return records

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_records(records: list[dict[str, Any]]) -> None:
    ensure_storage_exists()

    RECORDS_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def add_record(record: dict[str, Any]) -> None:
    records = load_records()
    records.append(record)
    save_records(records)

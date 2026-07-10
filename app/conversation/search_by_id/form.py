from uuid import UUID

from telegram import Update
from telegram.ext import ContextTypes

from app.conversation import states
from app.storage.hcp_storage import load_record_by_id


def _normalize_uuid(value: str) -> str | None:
    """
    Validates and normalizes a UUID.

    Returns the canonical UUID string when valid.
    Returns None when the supplied value is not a valid UUID.
    """

    try:
        return str(UUID(value.strip()))
    except (ValueError, AttributeError, TypeError):
        return None


async def receive_report_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """
    Receives a report UUID and attempts to load the matching HCP record.
    """

    if not update.message:
        return states.SEARCH_BY_ID_TEXT

    raw_id = update.message.text.strip()
    normalized_id = _normalize_uuid(raw_id)

    if not normalized_id:
        await update.message.reply_text(
            text=(
                "⚠️ El ID no tiene un formato válido.\n\n"
                "Copia y pega el ID completo que recibiste al registrar "
                "el reporte.\n\n"
                "Ejemplo:\n"
                "9f73e54f-2c84-4cc4-9012-7a21b321abcd"
            )
        )
        return states.SEARCH_BY_ID_TEXT

    record = load_record_by_id(normalized_id)

    if record is None:
        await update.message.reply_text(
            text=(
                "🔎 No encontramos un reporte con ese ID.\n\n"
                "Verifica que lo hayas copiado completo y sin cambiar "
                "ningún carácter.\n\n"
                "El ID identifica una observación HCP, no a una persona "
                "o animal."
            )
        )
        return states.SEARCH_BY_ID_TEXT

    context.user_data["search_by_id_record"] = record
    context.user_data["search_by_id_state"] = None

    return states.SEARCH_RESULTS

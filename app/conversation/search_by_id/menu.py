from telegram import Update
from telegram.ext import ContextTypes

from app.conversation import states


async def search_by_id_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """
    Starts the Search by Report ID flow.

    The user is asked to provide the UUID generated when the report
    was registered.
    """

    query = update.callback_query

    if not query:
        return states.SEARCH_BY_ID_TEXT

    await query.answer()

    context.user_data.pop("search_by_id_record", None)
    context.user_data.pop("search_by_id_candidates", None)
    context.user_data["search_by_id_state"] = states.SEARCH_BY_ID_TEXT

    message = (
        "🆔 Buscar por ID de reporte\n\n"
        "Escribe el ID HCP del reporte que deseas buscar.\n\n"
        "Este ID fue generado cuando registraste el reporte.\n\n"
        "Ejemplo:\n"
        "9f73e54f-2c84-4cc4-9012-7a21b321abcd\n\n"
        "Al encontrarlo, podrás revisar la observación y buscar nuevas "
        "observaciones relacionadas."
    )

    await query.edit_message_text(text=message)

    return states.SEARCH_BY_ID_TEXT

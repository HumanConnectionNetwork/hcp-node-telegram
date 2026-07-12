from telegram import Update
from telegram.ext import ContextTypes

from app.conversation import states
from app.hcp.record_builder import build_hcp_record
from app.storage.hcp_storage import add_record


async def submit_record(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Build a canonical HCP record, store it locally and show
    the report ID in a mobile-friendly format.
    """

    query = update.callback_query

    if not query:
        return

    await query.answer()

    # ---------------------------------------------------------
    # Build canonical HCP record
    # ---------------------------------------------------------

    record = build_hcp_record(context.user_data)

    # ---------------------------------------------------------
    # Local persistence
    # ---------------------------------------------------------

    add_record(record)

    print("\n==============================")
    print("New HCP Record")
    print("==============================")
    print(record)
    print("==============================\n")

    context.user_data["record_step"] = states.SUBMIT

    # ---------------------------------------------------------
    # Confirmation messages
    # ---------------------------------------------------------

    await query.edit_message_text(
        text="✅ Reporte registrado correctamente."
    )

    await update.effective_chat.send_message(
        text=(
            "🆔 ID del reporte\n\n"
            f"<code>{record['id']}</code>"
        ),
        parse_mode="HTML",
    )

    await update.effective_chat.send_message(
        text=(
            "📌 Guarda este ID.\n\n"
            "Con él podrás consultar nuevamente esta observación "
            "y buscar reportes relacionados más recientes."
        )
    )

    # ---------------------------------------------------------
    # Clean temporary conversation data
    # ---------------------------------------------------------

    language = context.user_data.get("language")

    context.user_data.clear()

    if language:
        context.user_data["language"] = language

    context.user_data["last_record_id"] = record["id"]

from telegram import Update
from telegram.ext import ContextTypes

from app.conversation import states
from app.models.humanitarian_record import HumanitarianRecord


async def submit_record(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    await query.answer()

    record = HumanitarianRecord(
        subject_type=context.user_data.get("subject_type", "human"),
        event_type=context.user_data.get("event_type", "unknown"),
        reported_name=context.user_data.get("reported_name", "Desconocido"),
        estimated_age=int(context.user_data.get("estimated_age", 0)),
        reported_location=context.user_data.get("reported_location", "Desconocido"),
        source=context.user_data.get("source", "unknown"),
        description=context.user_data.get("description", ""),
        status="reported",
    )

    payload = record.to_dict()

    print("HCP Record payload:")
    print(payload)

    context.user_data["record_step"] = states.SUBMIT

    await query.edit_message_text(
        text=(
            "✅ Reporte preparado correctamente.\n\n"
            "Gracias por contribuir.\n\n"
            "Tu reporte ha sido registrado como una observación humanitaria.\n\n"
            "HCP no busca identificar personas.\n"
            "HCP relaciona observaciones humanitarias para facilitar búsquedas, "
            "verificación y posibles coincidencias durante una emergencia.\n\n"
            "📄 Registro HCP\n\n"
            "ID:\n"
            "Pendiente de Nodo HCP\n\n"
            "Estado:\n"
            "🟢 Preparado correctamente\n\n"
            "Puedes compartir este reporte cuando sea registrado en un Nodo HCP."
        )
    )

    context.user_data.clear()

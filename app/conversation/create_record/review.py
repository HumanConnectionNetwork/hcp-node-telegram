from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.conversation import states


EVENT_LABELS = {
    "missing": "🚨 Persona desaparecida",
    "hospitalized": "🏥 Persona hospitalizada",
    "sheltered": "🏠 Persona refugiada / en albergue",
    "safe": "✅ Persona localizada / segura",
    "public_emergency": "🚑 Emergencia pública",
}


SOURCE_LABELS = {
    "family": "👨‍👩‍👧 Familia",
    "hospital": "🏥 Hospital",
    "fire_department": "🚒 Bomberos",
    "volunteer": "🤝 Voluntario",
    "police": "👮 Policía",
    "friend": "👤 Amigo / Conocido",
    "unknown": "❓ Desconocido",
}


async def review_record(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    event_type = context.user_data.get("event_type", "unknown")
    source = context.user_data.get("source", "unknown")

    summary = (
        "📋 Revisa tu reporte antes de enviarlo\n\n"
        "Has completado la información disponible para este reporte.\n\n"
        "Este registro formará parte de un servicio humanitario abierto cuyo propósito "
        "es facilitar la búsqueda y relación de información durante situaciones de emergencia.\n\n"
        "Te pedimos enviar únicamente información que consideres verdadera o razonablemente confiable. "
        "Un reporte honesto puede ayudar a conectar información importante para otras personas.\n\n"
        "──────────────\n\n"
        f"Tipo de evento: {EVENT_LABELS.get(event_type, event_type)}\n"
        f"Edad estimada: {context.user_data.get('estimated_age', 'Desconocido')}\n"
        f"Nombre reportado: {context.user_data.get('reported_name', 'Desconocido')}\n"
        f"Localización: {context.user_data.get('reported_location', 'Desconocido')}\n"
        f"Reportado por: {SOURCE_LABELS.get(source, source)}\n"
        f"Descripción: {context.user_data.get('description', 'Sin descripción')}\n\n"
        "¿Deseas enviar este reporte?"
    )

    keyboard = [
        [InlineKeyboardButton("✅ Confirmar y enviar", callback_data="review_confirm")],
        [InlineKeyboardButton("✏️ Editar información", callback_data="review_edit")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="review_cancel")],
    ]

    context.user_data["record_step"] = states.REVIEW

    if update.message:
        await update.message.reply_text(
            summary,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    if update.callback_query:
        await update.callback_query.edit_message_text(
            summary,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

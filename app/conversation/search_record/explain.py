from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


MOCK_EXPLANATIONS = {
    "candidate_1": {
        "probability": 68,
        "matches": [
            "Ubicación compatible con la búsqueda.",
            "El contexto del reporte es similar.",
            "La fuente del reporte puede ser relevante.",
        ],
        "warnings": [
            "El nombre no coincide completamente.",
            "La edad estimada necesita verificación humana.",
        ],
    },
    "candidate_2": {
        "probability": 52,
        "matches": [
            "El nombre reportado es parecido.",
            "La edad estimada es compatible.",
        ],
        "warnings": [
            "La ubicación es diferente.",
            "La probabilidad es moderada.",
        ],
    },
    "candidate_3": {
        "probability": 35,
        "matches": [
            "Existen algunas similitudes generales.",
        ],
        "warnings": [
            "Hay pocos datos compatibles.",
            "Este caso no debe interpretarse como una coincidencia probable.",
        ],
    },
    "weak_candidate_1": {
        "probability": 28,
        "matches": [
            "Existen similitudes generales de contexto.",
        ],
        "warnings": [
            "El nombre no coincide.",
            "La probabilidad es baja.",
            "Debe verificarse cuidadosamente antes de compartirlo como posible coincidencia.",
        ],
    },
}


def _format_list(items: list[str], icon: str) -> str:
    return "\n".join(f"{icon} {item}" for item in items)


async def explain_search_result(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    await query.answer()

    candidate_id = query.data.replace("explain_", "")
    explanation = MOCK_EXPLANATIONS.get(candidate_id)

    if not explanation:
        await query.edit_message_text(
            text=(
                "ℹ️ Explicación no disponible\n\n"
                "No fue posible encontrar los detalles de correlación para este caso."
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔍 Nueva búsqueda",
                            callback_data="search_menu",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "⬅️ Volver al menú principal",
                            callback_data="back_to_start",
                        )
                    ],
                ]
            ),
        )
        return

    matches = _format_list(explanation["matches"], "✅")
    warnings = _format_list(explanation["warnings"], "⚠️")

    message = (
        "ℹ️ ¿Por qué este resultado?\n\n"
        f"Probabilidad estimada: {explanation['probability']}%\n\n"
        "Este porcentaje no identifica a una persona o animal.\n"
        "Solo indica que existen observaciones compatibles con la búsqueda realizada.\n\n"
        "Coincidencias observadas:\n"
        f"{matches}\n\n"
        "Puntos que requieren verificación:\n"
        f"{warnings}\n\n"
        "La decisión final siempre debe ser verificada por una persona, familiar, "
        "institución o validador humanitario."
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🔍 Nueva búsqueda",
                callback_data="search_menu",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Volver al menú principal",
                callback_data="back_to_start",
            )
        ],
    ]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

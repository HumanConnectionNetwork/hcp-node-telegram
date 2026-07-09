from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.search.correlation import correlate_records
from app.storage.hcp_storage import load_records


EVENT_TYPE_LABELS = {
    "missing_person": "🚨 Persona desaparecida",
    "hospitalized_person": "🏥 Persona hospitalizada",
    "sheltered_person": "🏠 Persona refugiada",
    "safe_person": "✅ Persona localizada",
    "missing_animal": "🐾 Animal perdido",
    "found_animal": "✅ Animal encontrado",
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


def _format_unknown(value: object) -> str:
    if value is None:
        return "No especificado"

    text = str(value).strip()

    if not text or text == "0":
        return "No especificado"

    return text


def _event_type_label(value: object) -> str:
    key = str(value or "").strip()
    return EVENT_TYPE_LABELS.get(key, _format_unknown(value))


def _source_label(value: object) -> str:
    key = str(value or "").strip()
    return SOURCE_LABELS.get(key, _format_unknown(value))


def _candidate_callback_id(candidate: dict) -> str:
    candidate_id = str(candidate.get("candidate_id", "unknown"))
    return candidate_id[:60]


def _store_candidate_explanations(
    context: ContextTypes.DEFAULT_TYPE,
    candidates: list[dict],
) -> None:
    explanations = {}

    for candidate in candidates:
        candidate_id = _candidate_callback_id(candidate)

        explanations[candidate_id] = {
            "probability": candidate.get("probability", 0),
            "matches": candidate.get("matches", []),
            "warnings": candidate.get("warnings", []),
            "record": candidate.get("record", {}),
        }

    context.user_data["search_explanations"] = explanations


def _format_search_summary(search_data: dict) -> str:
    category = search_data.get("category", "person")

    if category == "animal":
        return (
            f"🐾 Animal: {_format_unknown(search_data.get('species'))}\n"
            f"🏷️ Nombre: {_format_unknown(search_data.get('animal_name'))}\n"
            f"📏 Tamaño: {_format_unknown(search_data.get('size'))}\n"
            f"🧬 Raza / tipo: {_format_unknown(search_data.get('breed_or_type'))}\n"
            f"📍 Ubicación: {_format_unknown(search_data.get('location'))}\n"
            f"🧩 Características: {_format_unknown(search_data.get('recognition_features'))}\n\n"
        )

    return (
        f"👤 Nombre: {_format_unknown(search_data.get('reported_name'))}\n"
        f"🎂 Edad aproximada: {_format_unknown(search_data.get('estimated_age'))}\n"
        f"📍 Ubicación: {_format_unknown(search_data.get('location'))}\n"
        f"🧩 Características: {_format_unknown(search_data.get('recognition_features'))}\n\n"
    )


def _format_candidate(index: int, candidate: dict) -> str:
    record = candidate.get("record", {})
    category = record.get("subject_type", "human")

    base = (
        "──────────────\n"
        f"📄 Posible caso relacionado #{index}\n\n"
        f"Probabilidad: {candidate.get('probability', 0)}%\n"
        f"Tipo: {_event_type_label(record.get('event_type'))}\n"
        f"Estado: {_format_unknown(record.get('status'))}\n"
        f"Fuente: {_source_label(record.get('source'))}\n\n"
        f"Nombre reportado: {_format_unknown(record.get('reported_name'))}\n"
        f"Ubicación reportada: {_format_unknown(record.get('reported_location'))}\n"
    )

    if category == "animal":
        base += (
            f"Especie: {_format_unknown(record.get('animal_species'))}\n"
            f"Tamaño: {_format_unknown(record.get('animal_size'))}\n"
            f"Raza / tipo: {_format_unknown(record.get('animal_breed'))}\n"
        )
    else:
        base += (
            f"Edad estimada: {_format_unknown(record.get('estimated_age'))}\n"
        )

    base += (
        f"Características: {_format_unknown(record.get('recognition_features'))}\n"
        f"ID HCP: {_format_unknown(record.get('id'))}\n\n"
    )

    return base


def _build_results_keyboard(candidates: list[dict]) -> InlineKeyboardMarkup:
    keyboard = []

    for index, candidate in enumerate(candidates, start=1):
        candidate_id = _candidate_callback_id(candidate)

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"ℹ️ ¿Por qué este resultado? #{index}",
                    callback_data=f"explain_{candidate_id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔍 Nueva búsqueda",
                callback_data="search_menu",
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "⬅️ Volver al menú principal",
                callback_data="back_to_start",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def _build_empty_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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
    )


async def show_search_results(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Shows possible related cases using local HCP records.

    In development, records are loaded from data/hcp_records.json.
    In production, this can be replaced by a Node HCP search endpoint
    without changing the Telegram flow.
    """

    search_data = context.user_data.get("search_record", {})
    records = load_records()

    candidates = correlate_records(
        search_data=search_data,
        records=records,
        limit=3,
        min_probability=20,
    )

    _store_candidate_explanations(context, candidates)

    message = (
        "🔍 Posibles casos relacionados\n\n"
        "HCP no identifica personas ni animales por identidad.\n"
        "Relaciona observaciones humanitarias que podrían corresponder "
        "a un mismo caso.\n\n"
        "Datos consultados:\n"
        f"{_format_search_summary(search_data)}"
    )

    if not candidates:
        await update.message.reply_text(
            message
            + (
                "No se encontraron posibles casos relacionados con la "
                "información proporcionada.\n\n"
                "Puedes intentar nuevamente agregando o modificando datos como:\n\n"
                "• nombre\n"
                "• ubicación\n"
                "• edad aproximada\n"
                "• características para identificación\n\n"
                "Las correlaciones mejoran cuando existen más observaciones compatibles."
            ),
            reply_markup=_build_empty_keyboard(),
        )
        return

    strong_candidates = [
        candidate for candidate in candidates
        if candidate.get("probability", 0) >= 60
    ]

    if strong_candidates:
        message += "Se encontraron posibles casos relacionados:\n\n"
    else:
        message += (
            "No se encontraron coincidencias fuertes.\n\n"
            "Sin embargo, existen observaciones con características parcialmente "
            "similares. Pueden ser útiles para verificación humanitaria, pero no "
            "deben interpretarse como coincidencias probables.\n\n"
        )

    for index, candidate in enumerate(candidates, start=1):
        message += _format_candidate(index, candidate)

    await update.message.reply_text(
        text=message,
        reply_markup=_build_results_keyboard(candidates),
    )

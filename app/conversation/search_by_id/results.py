from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.search.correlation import correlate_records
from app.storage.hcp_storage import load_records


CONTACT_VISIBILITY_THRESHOLD = 60


EVENT_TYPE_LABELS = {
    "missing_person": "🚨 Persona desaparecida",
    "hospitalized_person": "🏥 Persona hospitalizada",
    "sheltered_person": "🏠 Persona refugiada",
    "safe_person": "✅ Persona localizada",
    "missing_animal": "🐾 Animal desaparecido",
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


ANIMAL_SPECIES_LABELS = {
    "dog": "Perro",
    "cat": "Gato",
    "horse": "Caballo",
    "bird": "Ave",
    "other": "Otro",
    "unknown": "Animal",
}


ANIMAL_SIZE_LABELS = {
    "small": "Pequeño",
    "medium": "Mediano",
    "large": "Grande",
    "unknown": "Desconocido",
}


def _format_value(
    value: object,
    fallback: str = "No especificado",
) -> str:
    """
    Returns a clean value for user-facing messages.
    """

    if value is None:
        return fallback

    text = str(value).strip()

    if not text or text == "0":
        return fallback

    return text


def _event_type_label(value: object) -> str:
    key = str(value or "").strip()

    return EVENT_TYPE_LABELS.get(
        key,
        _format_value(value),
    )


def _source_label(value: object) -> str:
    key = str(value or "").strip()

    return SOURCE_LABELS.get(
        key,
        _format_value(value),
    )


def _animal_species_label(value: object) -> str:
    key = str(value or "").strip()

    return ANIMAL_SPECIES_LABELS.get(
        key,
        _format_value(value),
    )


def _animal_size_label(value: object) -> str:
    key = str(value or "").strip()

    return ANIMAL_SIZE_LABELS.get(
        key,
        _format_value(value),
    )


def _record_to_search_data(record: dict) -> dict:
    """
    Converts a canonical HCP record into correlation search criteria.

    This allows the existing correlation engine to search for newer or
    independent observations related to the stored report.
    """

    subject_type = record.get("subject_type", "human")

    if subject_type == "animal":
        return {
            "category": "animal",
            "animal_name": record.get("reported_name", ""),
            "species": record.get("animal_species", ""),
            "size": record.get("animal_size", ""),
            "breed_or_type": record.get("animal_breed", ""),
            "location": record.get("reported_location", ""),
            "recognition_features": record.get(
                "recognition_features",
                "",
            ),
        }

    return {
        "category": "person",
        "reported_name": record.get("reported_name", ""),
        "estimated_age": record.get("estimated_age"),
        "location": record.get("reported_location", ""),
        "recognition_features": record.get(
            "recognition_features",
            "",
        ),
    }


def _format_record(record: dict) -> str:
    """
    Formats the original HCP report found by its UUID.
    """

    subject_type = record.get("subject_type", "human")

    message = (
        "🆔 Reporte encontrado\n\n"
        f"Tipo de reporte: "
        f"{_event_type_label(record.get('event_type'))}\n"
        f"Estado: {_format_value(record.get('status'))}\n"
        f"Nombre reportado: "
        f"{_format_value(record.get('reported_name'))}\n"
    )

    if subject_type == "animal":
        message += (
            f"Especie: "
            f"{_animal_species_label(record.get('animal_species'))}\n"
            f"Tamaño: "
            f"{_animal_size_label(record.get('animal_size'))}\n"
            f"Raza / tipo: "
            f"{_format_value(record.get('animal_breed'))}\n"
        )
    else:
        message += (
            f"Edad estimada: "
            f"{_format_value(record.get('estimated_age'))}\n"
        )

    message += (
        f"Ubicación: "
        f"{_format_value(record.get('reported_location'))}\n"
        f"Fuente: {_source_label(record.get('source'))}\n"
        f"Características para identificación: "
        f"{_format_value(record.get('recognition_features'))}\n"
    )

    public_contact = str(
        record.get("public_contact") or ""
    ).strip()

    if public_contact:
        message += (
            f"📞 Medio de contacto: {public_contact}\n"
        )

    message += (
        f"Fecha de creación: "
        f"{_format_value(record.get('created_at'))}\n\n"
        f"🆔 ID del reporte:\n"
        f"{_format_value(record.get('id'))}\n\n"
        "Este ID identifica únicamente esta observación HCP. "
        "No identifica a una persona ni a un animal."
    )

    return message


def _record_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 Buscar nuevas observaciones relacionadas",
                    callback_data="search_by_id_related",
                )
            ],
            [
                InlineKeyboardButton(
                    "🆔 Buscar otro ID de reporte",
                    callback_data="search_by_id",
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


def _candidate_callback_id(candidate: dict) -> str:
    candidate_id = str(
        candidate.get("candidate_id", "unknown")
    )

    return candidate_id[:60]


def _store_candidate_explanations(
    context: ContextTypes.DEFAULT_TYPE,
    candidates: list[dict],
) -> None:
    """
    Stores explanations in the same structure used by search_record/explain.py.
    """

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


def _should_show_public_contact(
    candidate: dict,
    record: dict,
) -> bool:
    probability = int(
        candidate.get("probability", 0)
    )

    public_contact = str(
        record.get("public_contact") or ""
    ).strip()

    return (
        probability >= CONTACT_VISIBILITY_THRESHOLD
        and bool(public_contact)
    )


def _format_candidate(
    index: int,
    candidate: dict,
) -> str:
    """
    Formats one related observation found from the original report.
    """

    record = candidate.get("record", {})
    subject_type = record.get("subject_type", "human")
    probability = int(
        candidate.get("probability", 0)
    )

    message = (
        "──────────────\n"
        f"📄 Nueva observación relacionada #{index}\n\n"
        f"Compatibilidad: {probability}%\n"
        f"Tipo: {_event_type_label(record.get('event_type'))}\n"
        f"Nombre reportado: "
        f"{_format_value(record.get('reported_name'))}\n"
        f"Ubicación: "
        f"{_format_value(record.get('reported_location'))}\n"
    )

    if subject_type == "animal":
        message += (
            f"Especie: "
            f"{_animal_species_label(record.get('animal_species'))}\n"
            f"Tamaño: "
            f"{_animal_size_label(record.get('animal_size'))}\n"
            f"Raza / tipo: "
            f"{_format_value(record.get('animal_breed'))}\n"
        )
    else:
        message += (
            f"Edad estimada: "
            f"{_format_value(record.get('estimated_age'))}\n"
        )

    message += (
        f"Características: "
        f"{_format_value(record.get('recognition_features'))}\n"
    )

    if _should_show_public_contact(candidate, record):
        message += (
            f"📞 Medio de contacto: "
            f"{_format_value(record.get('public_contact'))}\n"
        )
    elif record.get("public_contact"):
        message += (
            "📞 Medio de contacto: protegido por baja correlación\n"
        )

    message += (
        f"Referencia HCP: "
        f"{_format_value(record.get('id'))}\n\n"
    )

    return message


def _related_results_keyboard(
    candidates: list[dict],
) -> InlineKeyboardMarkup:
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

    keyboard.extend(
        [
            [
                InlineKeyboardButton(
                    "🔄 Buscar nuevamente",
                    callback_data="search_by_id_related",
                )
            ],
            [
                InlineKeyboardButton(
                    "🆔 Buscar otro ID de reporte",
                    callback_data="search_by_id",
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

    return InlineKeyboardMarkup(keyboard)


async def show_record_by_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Displays the HCP report previously loaded by receive_report_id().
    """

    record = context.user_data.get("search_by_id_record")

    if not record:
        message = (
            "⚠️ No fue posible recuperar el reporte.\n\n"
            "Vuelve a seleccionar «Buscar por ID de reporte» "
            "e introduce nuevamente el ID."
        )

        if update.message:
            await update.message.reply_text(message)
        elif update.callback_query:
            await update.callback_query.edit_message_text(message)

        return

    message = _format_record(record)
    reply_markup = _record_keyboard()

    if update.message:
        await update.message.reply_text(
            text=message,
            reply_markup=reply_markup,
        )
        return

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
        )


async def search_related_from_report(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Runs a fresh correlation using the stored HCP report as the query.

    The original record is excluded from the results so it does not correlate
    with itself.
    """

    query = update.callback_query

    if not query:
        return

    await query.answer()

    original_record = context.user_data.get(
        "search_by_id_record"
    )

    if not original_record:
        await query.edit_message_text(
            text=(
                "⚠️ No fue posible recuperar el reporte original.\n\n"
                "Busca nuevamente el reporte mediante su ID."
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🆔 Buscar por ID de reporte",
                            callback_data="search_by_id",
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

    original_id = str(
        original_record.get("id", "")
    ).strip().lower()

    records = [
        record
        for record in load_records()
        if str(record.get("id", "")).strip().lower() != original_id
    ]

    search_data = _record_to_search_data(
        original_record
    )

    candidates = correlate_records(
        search_data=search_data,
        records=records,
        limit=3,
        min_probability=20,
    )

    context.user_data["search_by_id_candidates"] = candidates

    _store_candidate_explanations(
        context,
        candidates,
    )

    if not candidates:
        await query.edit_message_text(
            text=(
                "🔄 Nuevas observaciones relacionadas\n\n"
                "Por ahora no se encontraron otras observaciones compatibles "
                "con este reporte.\n\n"
                "Puedes volver a buscar más adelante usando el mismo ID. "
                "Los resultados pueden cambiar cuando se agreguen nuevos "
                "reportes a la red."
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔄 Buscar nuevamente",
                            callback_data="search_by_id_related",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🆔 Ver reporte original",
                            callback_data="search_by_id_show_record",
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

    message = (
        "🔄 Nuevas observaciones relacionadas\n\n"
        "Estos resultados aparecieron al comparar nuevamente el reporte "
        "con las observaciones disponibles actualmente.\n\n"
        "Una compatibilidad alta no confirma una identidad. "
        "Siempre debe existir verificación humana.\n\n"
        f"📞 El medio de contacto solo se muestra a partir del "
        f"{CONTACT_VISIBILITY_THRESHOLD}% de compatibilidad y nunca "
        "participa en el cálculo.\n\n"
    )

    for index, candidate in enumerate(candidates, start=1):
        message += _format_candidate(
            index,
            candidate,
        )

    await query.edit_message_text(
        text=message,
        reply_markup=_related_results_keyboard(
            candidates
        ),
    )

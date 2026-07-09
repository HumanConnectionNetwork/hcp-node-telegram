from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


MOCK_RESULTS = [
    {
        "candidate_id": "candidate_1",
        "probability": 68,
        "event_type": "🚨 Persona desaparecida",
        "reported_name": "Luis Trapito",
        "estimated_age": "45",
        "reported_location": "La Guaira",
        "status": "Reportado",
        "source": "👤 Amigo / Conocido",
        "reason_summary": (
            "Coinciden parcialmente el lugar y el contexto, "
            "pero el nombre y la edad no coinciden completamente."
        ),
    },
    {
        "candidate_id": "candidate_2",
        "probability": 52,
        "event_type": "🏥 Persona hospitalizada",
        "reported_name": "Luis Trápito",
        "estimated_age": "45",
        "reported_location": "Hospital en Caracas",
        "status": "Reportado",
        "source": "🏥 Hospital",
        "reason_summary": (
            "El nombre es parecido y la edad es compatible, "
            "pero la localización es diferente."
        ),
    },
    {
        "candidate_id": "candidate_3",
        "probability": 35,
        "event_type": "🏠 Persona refugiada / en albergue",
        "reported_name": "Luis T.",
        "estimated_age": "Adulto",
        "reported_location": "Centro de refugio",
        "status": "Reportado",
        "source": "🤝 Voluntario",
        "reason_summary": (
            "Existen pocos datos compatibles. "
            "Este resultado tiene baja probabilidad."
        ),
    },
]


def get_mock_results_for_query(search_data: dict) -> list[dict]:
    """
    Temporary mock correlation function.

    Later this function should be replaced by a real call to an HCP node.
    """

    search_name = search_data.get("reported_name", "")
    normalized_name = search_name.strip().lower()

    if normalized_name in ["mario", "pedro", "jose", "josé", "carlos"]:
        return [
            {
                "candidate_id": "weak_candidate_1",
                "probability": 28,
                "event_type": "🚨 Persona desaparecida",
                "reported_name": "Luis Trapito",
                "estimated_age": "45",
                "reported_location": "La Guaira",
                "status": "Reportado",
                "source": "👤 Amigo / Conocido",
                "reason_summary": (
                    "El nombre no coincide. "
                    "Solo existen similitudes generales de contexto."
                ),
            }
        ]

    return MOCK_RESULTS[:3]


def _format_unknown(value: object) -> str:
    if value is None:
        return "No especificado"

    text = str(value).strip()

    if not text:
        return "No especificado"

    if text == "0":
        return "No especificado"

    return text


async def show_search_results(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Shows possible related humanitarian cases.

    HCP does not claim to identify a person or animal.
    It shows correlation candidates based on compatible observations.
    """

    search_data = context.user_data.get("search_record", {})

    search_name = _format_unknown(
        search_data.get("reported_name") or search_data.get("animal_name")
    )
    search_age = _format_unknown(search_data.get("estimated_age"))
    search_location = _format_unknown(search_data.get("location"))
    search_features = _format_unknown(search_data.get("recognition_features"))
    search_category = search_data.get("category", "person")

    results = get_mock_results_for_query(search_data)

    message = (
        "🔍 Posibles casos relacionados\n\n"
        "HCP no identifica personas ni animales por identidad.\n"
        "Relaciona observaciones humanitarias que podrían corresponder "
        "a un mismo caso.\n\n"
        "Datos consultados:\n"
    )

    if search_category == "animal":
        species = _format_unknown(search_data.get("species"))
        size = _format_unknown(search_data.get("size"))
        breed_or_type = _format_unknown(search_data.get("breed_or_type"))

        message += (
            f"🐾 Animal: {species}\n"
            f"🏷️ Nombre: {search_name}\n"
            f"📏 Tamaño: {size}\n"
            f"🧬 Raza / tipo: {breed_or_type}\n"
            f"📍 Ubicación: {search_location}\n"
            f"🧩 Características: {search_features}\n\n"
        )
    else:
        message += (
            f"👤 Nombre: {search_name}\n"
            f"🎂 Edad aproximada: {search_age}\n"
            f"📍 Ubicación: {search_location}\n"
            f"🧩 Características: {search_features}\n\n"
        )

    if not results:
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

        await update.message.reply_text(
            message
            + (
                "No se encontraron posibles casos relacionados con la "
                "información proporcionada.\n\n"
                "Puedes intentar nuevamente agregando o modificando datos como:\n\n"
                "• ubicación\n"
                "• edad aproximada\n"
                "• características para identificación\n\n"
                "Las correlaciones mejoran cuando existen más observaciones compatibles."
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    strong_results = [result for result in results if result["probability"] >= 60]

    if strong_results:
        message += "Se encontraron posibles casos relacionados:\n\n"
    else:
        message += (
            "No se encontraron coincidencias fuertes.\n\n"
            "Sin embargo, existen algunos reportes con características "
            "parcialmente similares. Pueden ser útiles para verificación "
            "humanitaria, pero no deben interpretarse como coincidencias probables.\n\n"
        )

    keyboard = []

    for index, result in enumerate(results, start=1):
        message += (
            "──────────────\n"
            f"📄 Posible caso #{index}\n\n"
            f"Probabilidad: {result['probability']}%\n"
            f"Tipo: {result['event_type']}\n"
            f"Nombre reportado: {result['reported_name']}\n"
            f"Edad estimada: {result['estimated_age']}\n"
            f"Ubicación: {result['reported_location']}\n"
            f"Estado: {result['status']}\n"
            f"Fuente: {result['source']}\n\n"
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"ℹ️ ¿Por qué este resultado? #{index}",
                    callback_data=f"explain_{result['candidate_id']}",
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

    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

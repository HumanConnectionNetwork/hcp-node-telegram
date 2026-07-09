from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.messages import t


async def search_record_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Displays the initial Search Record menu.
    """

    query = update.callback_query

    if not query:
        return

    await query.answer()

    user_language = "es"

    keyboard = [
        [
            InlineKeyboardButton(
                "👤 Buscar persona",
                callback_data="search_person",
            )
        ],
        [
            InlineKeyboardButton(
                "🐾 Buscar animal",
                callback_data="search_animal",
            )
        ],
        [
            InlineKeyboardButton(
                t("common.cancel", user_language),
                callback_data="cancel",
            )
        ],
    ]

    message = (
        "🔍 Buscar caso reportado\n\n"
        "HCP busca observaciones humanitarias, no identidades.\n\n"
        "Cuando varias observaciones describen un mismo caso, "
        "el sistema puede encontrar registros relacionados mediante "
        "un proceso de correlación.\n\n"
        "Puedes proporcionar solo el nombre, o agregar más información "
        "para obtener resultados más precisos.\n\n"
        "¿Qué deseas buscar?"
    )

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def search_person_type_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Displays the person search type menu.
    """

    query = update.callback_query

    if not query:
        return

    await query.answer()

    user_language = "es"

    keyboard = [
        [
            InlineKeyboardButton(
                "🔍 Buscar una persona desaparecida",
                callback_data="search_person_missing",
            )
        ],
        [
            InlineKeyboardButton(
                "🔍 Buscar una persona hospitalizada",
                callback_data="search_person_hospitalized",
            )
        ],
        [
            InlineKeyboardButton(
                "🔍 Buscar una persona refugiada",
                callback_data="search_person_sheltered",
            )
        ],
        [
            InlineKeyboardButton(
                "🔍 Buscar una persona localizada",
                callback_data="search_person_safe",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Atrás",
                callback_data="search_menu",
            )
        ],
        [
            InlineKeyboardButton(
                t("common.cancel", user_language),
                callback_data="cancel",
            )
        ],
    ]

    message = (
        "👤 Buscar persona\n\n"
        "Selecciona el tipo de observación que deseas encontrar."
    )

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def search_animal_type_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Displays the animal search type menu.
    """

    query = update.callback_query

    if not query:
        return

    await query.answer()

    user_language = "es"

    keyboard = [
        [
            InlineKeyboardButton(
                "🔍 Buscar un animal perdido",
                callback_data="search_animal_missing",
            )
        ],
        [
            InlineKeyboardButton(
                "🔍 Buscar un animal encontrado",
                callback_data="search_animal_found",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Atrás",
                callback_data="search_menu",
            )
        ],
        [
            InlineKeyboardButton(
                t("common.cancel", user_language),
                callback_data="cancel",
            )
        ],
    ]

    message = (
        "🐾 Buscar animal\n\n"
        "Selecciona el tipo de observación que deseas encontrar."
    )

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.messages import t


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Displays the main menu of the HCP Telegram client.
    """

    user_language = context.user_data.get("language", "es")

    keyboard = [
        [
            InlineKeyboardButton(
                t("menu.create_report", user_language),
                callback_data="create_report",
            )
        ],
        [
            InlineKeyboardButton(
                t("menu.search_report", user_language),
                callback_data="search_report",
            )
        ],
        [
            InlineKeyboardButton(
                "🆔 Buscar por ID de reporte",
                callback_data="search_by_id",
            )
        ],
        [
            InlineKeyboardButton(
                t("menu.language", user_language),
                callback_data="language",
            )
        ],
        [
            InlineKeyboardButton(
                t("menu.help", user_language),
                callback_data="help",
            )
        ],
    ]

    message = (
        f"{t('start.welcome_title', user_language)}\n\n"
        f"{t('start.welcome_message', user_language)}\n\n"
        f"{t('start.main_menu_question', user_language)}"
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    language = context.user_data.get("language")
    context.user_data.clear()

    if language:
        context.user_data["language"] = language

    if update.message:
        await update.message.reply_text(
            text=message,
            reply_markup=reply_markup,
        )
        return

    if update.callback_query:
        query = update.callback_query

        await query.answer()

        await query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
        )

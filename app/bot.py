from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from app.config import settings
from app.conversation.create_record import create_record_menu, ask_reported_name
from app.conversation.start import start


def main() -> None:
    application = Application.builder().token(
        settings.telegram_bot_token
    ).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(
        CallbackQueryHandler(create_record_menu, pattern="^create_report$")
    )

    application.add_handler(
        CallbackQueryHandler(ask_reported_name, pattern="^event_")
    )

    print("HCP Telegram Client is running...")

    application.run_polling()


if __name__ == "__main__":
    main()

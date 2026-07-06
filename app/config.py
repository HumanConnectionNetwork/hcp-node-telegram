import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    hcp_node_url: str
    default_language: str
    request_timeout: int
    environment: str


def get_settings() -> Settings:
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    hcp_node_url = os.getenv("HCP_NODE_URL", "http://localhost:8000")
    default_language = os.getenv("DEFAULT_LANGUAGE", "en")
    request_timeout = int(os.getenv("REQUEST_TIMEOUT", "10"))
    environment = os.getenv("ENVIRONMENT", "development")

    if not telegram_bot_token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is missing. Please define it in your .env file."
        )

    return Settings(
        telegram_bot_token=telegram_bot_token,
        hcp_node_url=hcp_node_url.rstrip("/"),
        default_language=default_language,
        request_timeout=request_timeout,
        environment=environment,
    )


settings = get_settings()

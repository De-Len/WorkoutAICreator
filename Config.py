import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    # OpenRouter (или OpenAI)
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

    # Database
    DATABASE_URL = "sqlite:///./fitness.db"

    # Web
    WEB_HOST = "0.0.0.0"
    WEB_PORT = 8000

    # Model settings
    MODEL_NAME = "openai/gpt-3.5-turbo"  # или другой модель
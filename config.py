# config.py - исправленная версия
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TelegramConfig:
    token: str = os.getenv("TELEGRAM_TOKEN")
    bot_username: str = os.getenv("BOT_USERNAME", "")

@dataclass
class LLMConfig:
    api_key: str = os.getenv("OPENROUTER_API_KEY")
    api_url: str = "https://api.proxyapi.ru/openrouter/v1"
    model_name: str = "deepseek/deepseek-chat-v3-0324"

@dataclass
class DatabaseConfig:
    url: str = os.getenv("DATABASE_URL", "sqlite:///./fitness.db")

@dataclass
class WebConfig:
    host: str = os.getenv("WEB_HOST", "0.0.0.0")  # Должно быть 0.0.0.0 для облака
    port: int = int(os.getenv("WEB_PORT", 8000))
    external_url: str = os.getenv("EXTERNAL_URL")
    # Добавь если нужно:
    # allowed_hosts: list = field(default_factory=lambda: [
    #     external_url[7:],
    #     "localhost",
    #     "127.0.0.1"
    # ])

@dataclass
class Config:
    telegram: TelegramConfig = field(default_factory=TelegramConfig)  # Используем field
    llm: LLMConfig = field(default_factory=LLMConfig)  # Используем field
    database: DatabaseConfig = field(default_factory=DatabaseConfig)  # Используем field
    web: WebConfig = field(default_factory=WebConfig)  # Используем field

config = Config()
import asyncio
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from src.infrastructure.unit_of_work import UnitOfWork
from src.presentation.telegram_bot.handlers import router as telegram_router
from src.presentation.web.middleware import setup_cors
from src.presentation.web.routes import router as web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan для FastAPI приложения"""
    UnitOfWork.init_database()
    print("Database initialized")

    yield

    print("Application shutting down")


# Создаем FastAPI приложение
web_app = FastAPI(title="Fitness Program Generator", lifespan=lifespan)
setup_cors(web_app)  # Добавь эту строку
web_app.include_router(web_router)

# Создаем Telegram бота
bot = Bot(token=config.telegram.token)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(telegram_router)


def run_web_server():
    """Запуск веб-сервера в отдельном потоке"""
    uvicorn.run(
        web_app,
        host="0.0.0.0",  # Обязательно 0.0.0.0 для облака
        port=8000,
        reload=False
    )


async def run_telegram_bot():
    """Запуск Telegram бота"""
    await dp.start_polling(bot)


async def main():
    """Основная функция запуска"""
    print("Starting Fitness Program Generator...")
    print(f"Web interface: https://{config.web.host}:{config.web.port}")
    print(f"Telegram bot: @{(await bot.get_me()).username}")

    # Запускаем веб-сервер в отдельном потоке
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    # Запускаем Telegram бота
    await run_telegram_bot()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Application stopped")
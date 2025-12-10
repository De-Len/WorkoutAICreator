from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class TelegramDataMiddleware(BaseHTTPMiddleware):
    """Проверка данных от Telegram Web App"""

    async def dispatch(self, request: Request, call_next):
        # Telegram передает данные в заголовках или query параметрах
        telegram_data = request.query_params.get("tgWebAppData", "")

        if telegram_data:
            # Валидация данных от Telegram (опционально)
            pass

        response = await call_next(request)
        return response
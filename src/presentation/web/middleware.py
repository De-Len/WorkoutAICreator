from fastapi.middleware.cors import CORSMiddleware

from config import config


def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            config.web.external_url,
            "http://localhost:8080",
            "http://127.0.0.1:8080"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
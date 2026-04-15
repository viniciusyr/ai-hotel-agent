import logging

import uvicorn
from fastapi import FastAPI

from config.settings import get_settings
from telephony.twilio_handler import create_twilio_router


def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    app = FastAPI(title=f"{settings.hotel_name} Voice Agent")
    app.include_router(create_twilio_router(settings))
    return app


if __name__ == "__main__":
    app_settings = get_settings()
    uvicorn.run(
        "main:create_app",
        factory=True,
        host=app_settings.app_host,
        port=app_settings.app_port,
        log_level=app_settings.log_level.lower(),
    )

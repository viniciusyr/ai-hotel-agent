import logging
from html import escape

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from pipecat.runner.utils import parse_telephony_websocket
from pipecat.serializers.twilio import TwilioFrameSerializer
from pipecat.transports.websocket.fastapi import (
    FastAPIWebsocketParams,
    FastAPIWebsocketTransport,
)
from starlette.websockets import WebSocketState

from agent.pipeline import run_voice_pipeline
from config.settings import Settings

logger = logging.getLogger(__name__)


def create_twilio_router(settings: Settings) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @router.post("/voice")
    async def voice(request: Request) -> Response:
        websocket_url = _websocket_url(request)
        twiml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            "<Response>"
            "<Connect>"
            f'<Stream url="{escape(websocket_url, quote=True)}" />'
            "</Connect>"
            "</Response>"
        )
        return Response(content=twiml, media_type="application/xml")

    @router.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket) -> None:
        await websocket.accept()

        try:
            transport_type, call_data = await parse_telephony_websocket(websocket)
            if transport_type != "twilio":
                await websocket.close(code=1003)
                return

            serializer = TwilioFrameSerializer(
                stream_sid=call_data["stream_id"],
                call_sid=call_data["call_id"],
                account_sid=settings.twilio_account_sid,
                auth_token=settings.twilio_auth_token,
            )
            transport = FastAPIWebsocketTransport(
                websocket=websocket,
                params=FastAPIWebsocketParams(
                    audio_in_enabled=True,
                    audio_out_enabled=True,
                    add_wav_header=False,
                    serializer=serializer,
                ),
            )
            await run_voice_pipeline(transport, settings)
        except WebSocketDisconnect:
            logger.info("Twilio WebSocket disconnected")
        except Exception:
            logger.exception("Twilio WebSocket session failed")
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await websocket.close(code=1011)

    return router


def _websocket_url(request: Request) -> str:
    forwarded_proto = request.headers.get("x-forwarded-proto", request.url.scheme)
    forwarded_host = request.headers.get("x-forwarded-host")
    host = forwarded_host or request.headers.get("host") or request.url.netloc
    scheme = "wss" if forwarded_proto == "https" else "ws"
    return f"{scheme}://{host}/ws"

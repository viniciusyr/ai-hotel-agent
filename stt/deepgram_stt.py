from pipecat.services.deepgram.stt import DeepgramSTTService

from config.settings import Settings


def create_deepgram_stt(settings: Settings) -> DeepgramSTTService:
    return DeepgramSTTService(
        api_key=settings.deepgram_api_key,
        settings=DeepgramSTTService.Settings(
            model="nova-3-general",
            language="en",
            smart_format=True,
        ),
    )

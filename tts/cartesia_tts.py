from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.tts_service import TextAggregationMode

from config.settings import Settings


def create_cartesia_tts(settings: Settings) -> CartesiaTTSService:
    return CartesiaTTSService(
        api_key=settings.cartesia_api_key,
        settings=CartesiaTTSService.Settings(
            model="sonic-3",
            voice=settings.cartesia_voice_id,
        ),
        text_aggregation_mode=TextAggregationMode.TOKEN,
    )

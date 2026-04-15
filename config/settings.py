from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    twilio_account_sid: str = Field(
        validation_alias="TWILIO_ACCOUNT_SID",
        min_length=1,
    )
    twilio_auth_token: str = Field(validation_alias="TWILIO_AUTH_TOKEN", min_length=1)
    twilio_phone_number: str = Field(
        validation_alias="TWILIO_PHONE_NUMBER",
        min_length=1,
    )
    deepgram_api_key: str = Field(validation_alias="DEEPGRAM_API_KEY", min_length=1)
    anthropic_api_key: str = Field(validation_alias="ANTHROPIC_API_KEY", min_length=1)
    claude_model: str = Field(validation_alias="CLAUDE_MODEL", min_length=1)
    cartesia_api_key: str = Field(validation_alias="CARTESIA_API_KEY", min_length=1)
    cartesia_voice_id: str = Field(validation_alias="CARTESIA_VOICE_ID", min_length=1)
    hotel_name: str = Field(validation_alias="HOTEL_NAME", min_length=1)
    hotel_city: str = Field(validation_alias="HOTEL_CITY", min_length=1)
    hotel_phone: str = Field(validation_alias="HOTEL_PHONE", min_length=1)
    hotel_checkin_time: str = Field(
        validation_alias="HOTEL_CHECKIN_TIME",
        min_length=1,
    )
    hotel_checkout_time: str = Field(
        validation_alias="HOTEL_CHECKOUT_TIME",
        min_length=1,
    )
    app_host: str = Field(validation_alias="APP_HOST", min_length=1)
    app_port: int = Field(validation_alias="APP_PORT", gt=0, le=65535)
    log_level: str = Field(validation_alias="LOG_LEVEL", min_length=1)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )


def get_settings() -> Settings:
    return Settings()

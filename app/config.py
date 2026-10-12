
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "REX"
    app_version: str = "0.1.0"
    debug: bool = Field(default=True, validation_alias="VOICE_AI_DEBUG")

    ollama_model: str = "qwen3"
    ollama_host: str = "http://localhost:11434"

    whisper_model: str = "base"
    max_audio_size_mb: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

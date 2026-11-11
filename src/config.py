"""Application configuration for the text-to-SQL generator."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class ModelConfig:
    """Configuration for LLM model."""

    model_name: str = "openai/gpt-oss-20b"
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    timeout_seconds: float = 120.0
    max_retries: int = 2


class Settings:
    """Central configuration manager for the application."""

    def __init__(self):
        """Initialize settings from environment variables."""
        # Load environment variables from .env file
        self.base_dir = Path(__file__).parent.parent
        load_dotenv(self.base_dir / ".env")

        # Initialize model configuration
        self.model_config = ModelConfig(
            model_name=os.getenv("MODEL_NAME", "openai/gpt-oss-20b"),
            base_url=os.getenv("MODEL_BASE_URL", "https://openrouter.ai/api/v1"),
            api_key=os.getenv("MODEL_API_KEY", None),
            temperature=float(os.getenv("MODEL_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MODEL_MAX_TOKENS", "2048")),
            timeout_seconds=float(os.getenv("MODEL_TIMEOUT_SECONDS", "120")),
            max_retries=int(os.getenv("MODEL_MAX_RETRIES", "2")),
        )

        # Logging configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")


# Global settings instance
settings = Settings()
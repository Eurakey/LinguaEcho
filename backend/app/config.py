"""
Application configuration using environment variables
"""
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""

    # LLM Provider Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openrouter")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    # CORS Configuration
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    ).split(",")

    # Rate Limiting
    RATE_LIMIT_PER_HOUR: int = int(os.getenv("RATE_LIMIT_PER_HOUR", "20"))

    @property
    def api_key(self) -> str:
        """Get the appropriate API key based on LLM provider"""
        if self.LLM_PROVIDER == "groq":
            return self.GROQ_API_KEY
        return self.OPENROUTER_API_KEY

    @property
    def model_name(self) -> str:
        """Get the appropriate model name based on LLM provider"""
        if self.LLM_PROVIDER == "groq":
            return self.GROQ_MODEL
        return self.OPENROUTER_MODEL


settings = Settings()

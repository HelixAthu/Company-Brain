import logging
import os
from typing import Optional
from backend.config import settings

logger = logging.getLogger("company_brain.ai")

class GeminiAgent:
    """Core Google Gemini AI Agent client wrapper."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = "gemini-2.5-flash"
        self._client = None

    def get_client(self):
        """Lazy initialization of the official Google GenAI SDK client."""
        if self._client is not None:
            return self._client
        try:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            logger.info("Initialized Google GenAI client successfully.")
            return self._client
        except Exception as e:
            logger.warning(f"Could not initialize Google GenAI SDK: {e}. Will rely on fallback/mock mode if needed.")
            return None

    def is_configured(self) -> bool:
        """Check if a non-placeholder Gemini API key is configured."""
        return (
            bool(self.api_key) and 
            self.api_key != "your_gemini_api_key_here" and
            not self.api_key.startswith("your_")
        )

# Global singleton
gemini_agent = GeminiAgent()

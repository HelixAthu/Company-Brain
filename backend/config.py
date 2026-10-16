import os
from typing import List
from dotenv import load_dotenv

# Preload environment variables from .env
load_dotenv()

try:
    from pydantic_settings import BaseSettings
    from pydantic import Field

    class Settings(BaseSettings):
        GEMINI_API_KEY: str = Field(default="your_gemini_api_key_here", env="GEMINI_API_KEY")
        FALKORDB_HOST: str = Field(default="localhost", env="FALKORDB_HOST")
        FALKORDB_PORT: int = Field(default=6379, env="FALKORDB_PORT")
        FALKORDB_GRAPH: str = Field(default="company_brain", env="FALKORDB_GRAPH")
        DEMO_MODE: bool = Field(default=False, env="DEMO_MODE")
        CORS_ORIGINS: str = Field(
            default="http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
            env="CORS_ORIGINS"
        )

        @property
        def cors_origins_list(self) -> List[str]:
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            extra = "ignore"

    settings = Settings()

except ImportError:
    # Fallback to standard os.environ loader
    class Settings:
        def __init__(self):
            self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")
            self.FALKORDB_HOST = os.getenv("FALKORDB_HOST", "localhost")
            self.FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", "6379"))
            self.FALKORDB_GRAPH = os.getenv("FALKORDB_GRAPH", "company_brain")
            self.DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() in ("true", "1", "t", "yes")
            self.CORS_ORIGINS = os.getenv(
                "CORS_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
            )

        @property
        def cors_origins_list(self) -> List[str]:
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    settings = Settings()

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "mergemindpassword123"
    GITHUB_WEBHOOK_SECRET: str = "mergemind-webhook-secret"
    GITHUB_TOKEN: Optional[str] = None
    JWT_SECRET: str = "mergemind-jwt-secret-key-please-change-in-prod"

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()


from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "mergemindpassword123"
    GITHUB_WEBHOOK_SECRET: str = "mergemind-webhook-secret"
    GITHUB_TOKEN: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()

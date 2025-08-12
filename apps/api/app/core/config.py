from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_name: str = "OEI API"
    # e.g. postgresql+psycopg://oei:oei@localhost:5432/oei
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://oei:oei@db:5432/oei")
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")

settings = Settings()

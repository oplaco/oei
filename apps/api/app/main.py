from fastapi import FastAPI
from app.core.config import settings
from app.routers.main import all_routers

app = FastAPI(title=settings.app_name)

app.include_router(all_routers)

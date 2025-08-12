from fastapi import APIRouter
from app.schemas.satellite import SatelliteCreate, SatelliteUpdate, SatelliteRead
from app.repositories.satellite import SatelliteRepo
from app.routers.factory import RouterFactory

satellite_router: APIRouter = RouterFactory(
    name="satellites",
    pk_type=int,
    pk_field="id",
    create_schema=SatelliteCreate,
    update_schema=SatelliteUpdate,
    read_schema=SatelliteRead,
    repo=SatelliteRepo,
)

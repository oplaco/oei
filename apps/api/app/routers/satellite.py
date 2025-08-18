from fastapi import APIRouter
from app.schemas.satellite import CreateSatellite, UpdateSatellite, ReadSatellite
from app.repositories.satellite import SatelliteRepo
from app.routers.factory import RouterFactory

satellite_router: APIRouter = RouterFactory(
    name="satellites",
    pk_type=int,
    pk_field="id",
    create_schema=CreateSatellite,
    update_schema=UpdateSatellite,
    read_schema=ReadSatellite,
    repo=SatelliteRepo,
)

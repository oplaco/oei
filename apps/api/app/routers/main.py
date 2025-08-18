from app.routers.aoi import aoi_router
from app.routers.satellite import satellite_router
from app.routers.tle import tle_router

all_routers = [satellite_router, tle_router, aoi_router]

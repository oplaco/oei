from app.routers.aoi import aoi_router
from app.routers.orbital_pass import orbital_pass_router
from app.routers.satellite import satellite_router
from app.routers.tle import tle_router

all_routers = [satellite_router, tle_router, aoi_router, orbital_pass_router]

from app.models.satellite import Satellite
from app.repositories.abstract import AbstractRepository

SatelliteRepo = AbstractRepository(Satellite)

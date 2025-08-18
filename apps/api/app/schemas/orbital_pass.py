from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from typing import Union


class TimeWindow(BaseModel):
    start: datetime
    end: datetime


class PassComputeRequest(BaseModel):
    satellite_id: int
    aoi_id: int
    window: TimeWindow
    min_elevation_deg: float = Field(default=10.0, ge=0, le=90)


class PassComputeResult(BaseModel):
    start_time: datetime
    end_time: datetime
    max_elevation_deg: float
    max_elevation_time: datetime
    track_geojson: dict  # Leaflet-ready LineString

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BaseTLE(BaseModel):
    name: Optional[str] = None
    line1: str
    line2: str
    epoch_utc: datetime
    satnum: int
    intl_desg: Optional[str] = None
    inclination_deg: float
    raan_deg: float
    eccentricity: float
    arg_perigee_deg: float
    mean_anomaly_deg: float
    mean_motion_rev_per_day: float
    bstar: Optional[float] = None
    rev_number: Optional[int] = None
    checksum_ok_l1: bool
    checksum_ok_l2: bool
    source: Optional[str] = None


class CreateTLE(BaseTLE):
    satellite_id: int


class UpdateTLE(BaseTLE):
    pass


class ReadTLE(BaseTLE):
    id: int
    satellite_id: int
    fetched_at: datetime

    class Config:
        orm_mode = True

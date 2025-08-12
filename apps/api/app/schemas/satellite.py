from pydantic import BaseModel, Field


class SatelliteCreate(BaseModel):
    norad_id: int = Field(ge=1, description="NORAD catalog number (positive integer)")
    name: str = Field(min_length=1, max_length=128)


class SatelliteUpdate(BaseModel):
    # Partial update: both fields optional
    norad_id: int | None = Field(default=None, ge=1)
    name: str | None = Field(default=None, min_length=1, max_length=128)


class SatelliteRead(BaseModel):
    id: int
    norad_id: int
    name: str

    class Config:
        from_attributes = True

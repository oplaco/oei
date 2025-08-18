from fastapi import APIRouter, Body, Depends, HTTPException
from geoalchemy2.shape import to_shape
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.tle import TLE
from app.models.aoi import AOI
from app.models.satellite import Satellite
from app.schemas.orbital_pass import PassComputeRequest, PassComputeResult
from app.utils.pass_engine import compute_passes_over_aoi

orbital_pass_router = APIRouter(prefix="/passes", tags=["orbital_passes"])


@orbital_pass_router.post("/compute", response_model=list[PassComputeResult])
def compute_passes(
    req: PassComputeRequest = Body(...),
    db: Session = Depends(get_db),
):
    # 1. Get satellite
    sat = db.execute(
        select(Satellite).where(Satellite.id == req.satellite_id)
    ).scalar_one_or_none()
    if not sat:
        raise HTTPException(status_code=404, detail="Satellite not found")

    # 2. Get latest TLE for this satellite
    tle = db.execute(
        select(TLE).where(TLE.satellite_id == sat.id).order_by(TLE.epoch_utc.desc())
    ).scalar_one_or_none()
    if not tle:
        raise HTTPException(
            status_code=404, detail="No TLEs available for this satellite"
        )

    # 3. Get AOI geometry
    aoi = db.execute(select(AOI).where(AOI.id == req.aoi_id)).scalar_one_or_none()
    if not aoi:
        raise HTTPException(status_code=404, detail="AOI not found")
    shapely_geom = to_shape(aoi.geometry)  # returns a Shapely Polygon/MultiPolygon

    # 4. Compute passes
    try:
        passes = compute_passes_over_aoi(
            tle=tle,
            aoi_geometry=shapely_geom,
            window=req.window,
            min_elevation_deg=req.min_elevation_deg,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pass computation failed: {e}")

    return passes

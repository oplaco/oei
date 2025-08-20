from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from app.db.session import get_db
from app.models.satellite import Satellite
from app.models.tle import TLE
from app.repositories.tle import TLERepo
from app.routers.factory import RouterFactory
from app.schemas.tle import CreateTLE, ReadTLE, UpdateTLE
from app.utils.tle_parser import parse_tle_block, validate_tle_checksum


def add_ingest_endpoint(router: APIRouter):
    @router.post("/ingest", status_code=201)
    def ingest_tles_from_raw_text(
        raw_text: str = Body(..., media_type="text/plain"),
        db: Session = Depends(get_db),
    ):
        lines = [l for l in raw_text.strip().splitlines() if l.strip()]
        if len(lines) % 3 != 0:
            raise HTTPException(
                status_code=400,
                detail="TLE input must be groups of 3 lines (name, line1, line2)",
            )

        parsed_tles = []
        for i in range(0, len(lines), 3):
            name, line1, line2 = lines[i : i + 3]
            try:
                tle_data = parse_tle_block(name, line1, line2)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error parsing TLE: {e}")

            sat = (
                db.query(Satellite)
                .filter(Satellite.norad_id == tle_data["satnum"])
                .first()
            )
            if not sat:
                sat = Satellite(norad_id=tle_data["satnum"], name=tle_data["name"])
                db.add(sat)
                db.flush()

            tle_data["satellite_id"] = sat.id
            tle_data["checksum_ok_l1"] = validate_tle_checksum(line1)
            tle_data["checksum_ok_l2"] = validate_tle_checksum(line2)
            # tle_data["source"] Source of the data
            parsed_tles.append(TLE(**tle_data))

        try:
            db.add_all(parsed_tles)
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="One or multiple TLEs message already exist in the database.",
            )

        return {
            "message": f"{len(parsed_tles)} TLEs ingested successfully.",
            "satellites": [t.satnum for t in parsed_tles],
        }


tle_router: APIRouter = RouterFactory(
    name="tles",
    pk_type=int,
    create_schema=CreateTLE,
    update_schema=UpdateTLE,
    read_schema=ReadTLE,
    repo=TLERepo(),
    extra_routes=add_ingest_endpoint,
)

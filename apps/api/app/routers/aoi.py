from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from shapely.geometry import shape, MultiPolygon, Polygon
from geoalchemy2.shape import from_shape
import json

from app.db.session import get_db
from app.models.aoi import AOI

aoi_router = APIRouter(prefix="/aois", tags=["AOIs"])


@aoi_router.post("/upload", response_model=dict)
async def upload_geojson_aoi(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        contents = await file.read()
        geojson_data = json.loads(contents)

        # Extract geometry depending on the wrapper
        if geojson_data.get("type") == "FeatureCollection":
            features = geojson_data.get("features", [])
            if len(features) != 1:
                raise ValueError("Only one Feature is allowed.")
            geometry_data = features[0]["geometry"]

        elif geojson_data.get("type") == "Feature":
            geometry_data = geojson_data["geometry"]

        elif geojson_data.get("type") == "Polygon":
            geometry_data = geojson_data

        else:
            raise ValueError("Unsupported GeoJSON type.")

        geom = shape(geometry_data)

        if not isinstance(geom, Polygon):
            raise ValueError("Only GeoJSON Polygons are supported.")

    except Exception as e:
        raise HTTPException(400, detail=f"Invalid GeoJSON file: {e}")

    db_aoi = AOI(name=name, geometry=from_shape(geom, srid=4326))
    db.add(db_aoi)
    db.commit()
    db.refresh(db_aoi)

    return {"id": db_aoi.id, "name": db_aoi.name}

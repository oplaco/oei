from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from geoalchemy2 import Geometry
from app.db.base import Base


class AOI(Base):
    __tablename__ = "aois"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    geometry: Mapped[str] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=4326), nullable=False
    )

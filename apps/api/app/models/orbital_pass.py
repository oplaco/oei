import datetime as dt
from sqlalchemy import Integer, Float, DateTime, func, CheckConstraint, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry


class OrbitalPass(Base):
    __tablename__ = "orbital_passes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    satellite_id: Mapped[int] = mapped_column(
        ForeignKey("satellites.id", ondelete="CASCADE"), nullable=False
    )
    aoi_id: Mapped[int] = mapped_column(
        ForeignKey("aois.id", ondelete="CASCADE"), nullable=False
    )
    tle_id: Mapped[int] = mapped_column(
        ForeignKey("tles.id", ondelete="RESTRICT"), nullable=False
    )

    start_time: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        doc="UTC start of visibility window for the pass.",
    )
    end_time: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        doc="UTC end of visibility window for the pass.",
    )

    max_elevation_deg: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        doc="Maximum elevation (degrees) reached during the pass (0–90).",
    )
    max_elevation_time: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        doc="UTC timestamp when max_elevation_deg occurs (within [start,end]).",
    )

    track_geom: Mapped[str] = mapped_column(
        Geometry(geometry_type="LINESTRING", srid=4326, spatial_index=True),
        nullable=False,
        doc="Sub-satellite ground track as a LINESTRING in EPSG:4326.",
    )

    min_elevation_deg: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=10.0,
        doc="Elevation threshold (deg) used to detect the pass.",
    )

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Row creation time (UTC).",
    )
    __table_args__ = (
        # Temporal sanity checks
        CheckConstraint("end_time > start_time", name="ck_pass_time_order"),
        CheckConstraint(
            "max_elevation_deg >= 0 AND max_elevation_deg <= 90",
            name="ck_pass_max_el_range",
        ),
        CheckConstraint(
            "max_elevation_time >= start_time AND max_elevation_time <= end_time",
            name="ck_pass_peak_within_window",
        ),
    )

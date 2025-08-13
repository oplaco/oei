from datetime import datetime
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Numeric,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Index,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class TLE(Base):
    __tablename__ = "tles"

    # ---- Identity / relations ----
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    satellite_id: Mapped[int] = mapped_column(
        ForeignKey("satellites.id", ondelete="CASCADE"), nullable=False
    )

    # ---- Raw ----
    name: Mapped[str | None] = mapped_column(String(128))
    line1: Mapped[str] = mapped_column(
        String(80), nullable=False
    )  # usually 69 chars, allow up to ~80
    line2: Mapped[str] = mapped_column(String(80), nullable=False)

    # ---- Parsed (normalized) ----
    epoch_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    satnum: Mapped[int] = mapped_column(Integer, nullable=False)
    intl_desg: Mapped[str | None] = mapped_column(String(11))  # e.g., YYNNNAAA
    inclination_deg: Mapped[float] = mapped_column(Numeric(7, 4), nullable=False)  # i
    raan_deg: Mapped[float] = mapped_column(Numeric(7, 4), nullable=False)  # Ω
    eccentricity: Mapped[float] = mapped_column(
        Numeric(9, 7), nullable=False
    )  # e (decimal, not 7-digit integer)
    arg_perigee_deg: Mapped[float] = mapped_column(Numeric(7, 4), nullable=False)  # ω
    mean_anomaly_deg: Mapped[float] = mapped_column(Numeric(7, 4), nullable=False)  # M
    mean_motion_rev_per_day: Mapped[float] = mapped_column(
        Numeric(12, 8), nullable=False
    )  # n
    bstar: Mapped[float | None] = mapped_column(Numeric(12, 8))  # drag term (can be 0)

    # From line 2 tail
    rev_number: Mapped[int | None] = mapped_column(Integer)

    # ---- Validation / provenance ----
    checksum_ok_l1: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    checksum_ok_l2: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    source: Mapped[str | None] = mapped_column(String(64))
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    satellite = relationship("Satellite", back_populates="tles")

    __table_args__ = (
        # prevent duplicates for the same sat & epoch
        UniqueConstraint("satellite_id", "epoch_utc", name="uq_tle_sat_epoch"),
    )

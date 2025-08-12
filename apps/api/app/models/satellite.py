from sqlalchemy import Integer, String, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Satellite(Base):
    __tablename__ = "satellites"
    __table_args__ = (UniqueConstraint("norad_id", name="uq_sat_norad"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    norad_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)

    tles = relationship("TLE", back_populates="satellite", cascade="all, delete-orphan")

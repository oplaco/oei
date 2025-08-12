from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import models so Alembic sees them
from app.models import satellite, tle, aoi, pass_prediction  # noqa: E402,F401
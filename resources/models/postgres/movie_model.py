from ...services.postgresql_service import Base
from sqlalchemy import (
    Column, Integer, String, JSON, Float, DateTime
)
from datetime import datetime, timezone

class Movie(Base):
    __tablename__ = "movies"
    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=True)
    genres = Column(JSON, nullable=True)
    overview = Column(String(500), nullable=True)
    release_date = Column(String(10), nullable=True)
    vote_average = Column(Float, nullable=True)
    vote_count = Column(Integer, nullable=True)
    runtime = Column(Integer, nullable=True)
    tagline = Column(String(100), nullable=True)
    keywords = Column(JSON, nullable=True)

    poster_path = Column(String(100), nullable=True)
    backdrop_path = Column(String(100), nullable=True)
    images_path = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
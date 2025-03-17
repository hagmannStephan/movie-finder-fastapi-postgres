from ...services.postgresql_service import Base
from sqlalchemy import (
    Column, Integer, String
)

class Movie(Base):
    __tablename__ = "movies"
    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=True)
    poster_path = Column(String(100), nullable=True)
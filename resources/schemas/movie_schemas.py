from pydantic import BaseModel
from typing import List
from datetime import datetime

class MovieBase(BaseModel):
    movie_id: int
    title: str
    liked_on: datetime

class Movie(MovieBase):
    pass

    class Config:
        from_attributes = True

class Genre(BaseModel):
    id: int
    name: str

class GenreList(BaseModel):
    movie_genres: List[Genre]
    tv_genres: List[Genre]

# Incomplete
class MovieProfile(BaseModel):
    genres: List[str]
    overview: str
    backdrop_path: str  # https://image.tmdb.org/t/p/original/{backdrop_path}
    original_language: str
    release_date: str
    vote_average: float
    vote_count: int
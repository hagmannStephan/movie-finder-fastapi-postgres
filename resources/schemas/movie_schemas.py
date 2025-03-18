from pydantic import BaseModel
from typing import List
from datetime import datetime, date

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

class MovieProfile(BaseModel):
    id: int
    title: str
    genres: List[Genre]
    overview: str
    release_date: date
    vote_average: float
    vote_count: int
    runtime: int
    tagline: str
    keywords: List[str]

    # https://image.tmdb.org/t/p/original/{path}
    poster_path: str
    backdrop_path: str
    images_path: List[str]
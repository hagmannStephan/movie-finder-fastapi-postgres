from pydantic import BaseModel, Field
from typing import List
from datetime import date

class Genre(BaseModel):
    id: int
    name: str

class GenreList(BaseModel):
    movie_genres: List[Genre]
    tv_genres: List[Genre]

    class Config:
        from_attributes = True

class BaseMovie(BaseModel):
    title: str
    overview: str
    genres: List[Genre]
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
    watch_providers: dict

    class Config:
        from_attributes = True
        from_orm = True

class MovieFavourites(BaseMovie):
    id: int = Field(..., alias='movie_id')  # Alias to map movie_id to id


class MovieProfile(BaseMovie):
    id: int
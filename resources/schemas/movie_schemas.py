from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Genre(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class GenreList(BaseModel):
    movie_genres: Optional[List[Genre]] = None
    tv_genres: Optional[List[Genre]] = None

    class Config:
        from_attributes = True

class BaseMovie(BaseModel):
    title: Optional[str] = None
    overview: Optional[str] = None
    genres: Optional[List[Genre]] = None
    release_date: Optional[date] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    runtime: Optional[int] = None
    tagline: Optional[str] = None
    keywords: Optional[List[str]] = None

    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    images_path: Optional[List[str]] = None
    watch_providers: Optional[dict] = None

    class Config:
        from_attributes = True
        from_orm = True

class MovieFavourites(BaseMovie):
    id: Optional[int] = Field(None, alias='movie_id')

class MovieProfile(BaseMovie):
    id: Optional[int] = None

class WatchProvider(BaseModel):
    provider_id: int
    provider_name: str
    logo_path: Optional[str] = None
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8)]


class UserCreated(UserBase):
    user_id: int
    friend_code: str

    class Config:
        from_attributes = True

class User(UserCreated):
    created_on: str
    last_login: str
    movie_session: dict
    page: int
    latest_movie_date: str
    show_movies: bool
    show_tv: bool
    include_adult: bool
    language: str
    release_date_gte: str
    release_date_lte: str
    watch_region: str
    watch_providers: list
    with_genres: list
    without_genres: list
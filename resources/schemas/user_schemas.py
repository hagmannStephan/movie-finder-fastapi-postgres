from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime, date
from typing import Annotated, Optional, List

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
    created_on: Optional[datetime] = None
    last_login: Optional[datetime] = None

    movie_session: Optional[dict] = None
    page: int = 1
    latest_movie_date: Optional[date] = None

    show_movies: bool = True
    show_tv: bool = True
    include_adult: bool = False
    language: str = 'en-US'
    release_date_gte: Optional[date] = None
    release_date_lte: Optional[date] = None
    watch_region: str = 'CH'

    watch_providers: List[str] = []
    with_genres: List[str] = []
    without_genres: List[str] = []

    @field_validator("watch_providers", "with_genres", "without_genres", mode="before")
    @classmethod
    def parse_json_fields(cls, value):
        """Ensure JSON-encoded lists are properly converted."""
        if isinstance(value, str):
            import json
            return json.loads(value)
        return value

    class Config:
        orm_mode = True
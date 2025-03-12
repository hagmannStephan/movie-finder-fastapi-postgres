from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

class User(UserCreated):
    show_movies: bool = True
    show_tv: bool = True
    include_adult: bool = False
    language: str = 'en-US'
    release_date_gte: Optional[date] = None
    release_date_lte: Optional[date] = None
    watch_region: str = 'CH'

    watch_providers: List[str] = Field(default_factory=list)
    with_genres: List[str] = Field(default_factory=list)
    without_genres: List[str] = Field(default_factory=list)

    created_on: Optional[datetime] = None
    last_login: Optional[datetime] = None

    movie_session: Optional[dict] = None
    page: int = 1
    latest_movie_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("watch_providers", "with_genres", "without_genres", mode="before")
    @classmethod
    def parse_json_fields(cls, value):
        """Ensure JSON-encoded lists are properly converted."""
        if isinstance(value, str):
            import json
            return json.loads(value)
        if isinstance(value, list):
            return [str(item) for item in value]
        return value
    
    @field_validator("show_movies", "show_tv")
    @classmethod
    def validate_show_preference(cls, value, info):
        """Ensure at least one of show_movies or show_tv is True."""
        
        if info.data.get('show_movies') is False and info.data.get('show_tv') is False:
            raise ValueError("At least one of show_movies or show_tv must be True")
        
        return value
        
    model_config = ConfigDict(from_attributes=True)


class UserPatchSettings(BaseModel):
    show_movies: bool = True
    show_tv: bool = True
    include_adult: bool = False
    language: str = 'en-US'
    release_date_gte: date = None
    release_date_lte: date = None
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
    
    @field_validator("show_movies", "show_tv")
    @classmethod
    def validate_show_preference(cls, value, info):
        """Ensure at least one of show_movies or show_tv is True."""
        
        if info.data.get('show_movies') is False and info.data.get('show_tv') is False:
            raise ValueError("At least one of show_movies or show_tv must be True")
        
        return value
        
    model_config = ConfigDict(from_attributes=True)

class GroupMember(BaseModel):
    friend_code: str
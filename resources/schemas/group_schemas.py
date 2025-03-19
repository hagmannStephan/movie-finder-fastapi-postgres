from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from .movie_schemas import MovieProfile as Movie
import json

class GroupCreate(BaseModel):
    name: str = Field(..., max_length=25)

class GroupUpdate(GroupCreate):
    admin_id: int

    show_movies: bool = True
    show_tv: bool = True

    settings_movies: Optional[Dict[str, Any]] = None
    settings_tv: Optional[Dict[str, Any]] = None

    @field_validator("settings_movies", "settings_tv", mode="before")
    @classmethod
    def parse_json_fields(cls, value):
        """Ensure JSON-encoded fields are properly converted."""
        if isinstance(value, str):
            return json.loads(value)
        return value

    @field_validator("settings_movies")
    @classmethod
    def validate_settings_movies(cls, value):
        """Validate settings_movies against default structure."""
        default_settings = {
            "include_adult": False,
            "language": "en-US",
            "release_date": {"gte": "1900-01-01", "lte": None},
            "vote_avrage": {"gte": 0, "lte": 10},
            "watch_region": None,
            "genres": {"include": [], "exclude": []},
            "with_runtime": {"gte": 0, "lte": 300},
            "watch_providers": [],
        }
        return cls._validate_settings(value, default_settings)

    @field_validator("settings_tv")
    @classmethod
    def validate_settings_tv(cls, value):
        """Validate settings_tv against default structure."""
        default_settings = {
            "include_adult": False,
            "language": "en-US",
            "first_air_date": {"gte": "1900-01-01", "lte": None},
            "vote_avrage": {"gte": 0, "lte": 10},
            "watch_region": None,
            "genres": {"include": [], "exclude": []},
            "watch_providers": [],
        }
        return cls._validate_settings(value, default_settings)

    @staticmethod
    def _validate_settings(value, default_settings):
        """Helper method to validate settings against a default structure."""
        if value is None:
            return default_settings
        if not isinstance(value, dict):
            raise ValueError("Settings must be a dictionary.")
        for key, default_value in default_settings.items():
            if key not in value:
                value[key] = default_value
            elif isinstance(default_value, dict) and isinstance(value[key], dict):
                value[key] = Group._validate_settings(value[key], default_value)
        return value

    @field_validator("show_movies", "show_tv")
    @classmethod
    def validate_show_preference(cls, value, info):
        """Ensure at least one of show_movies or show_tv is True."""
        show_movies = info.data.get("show_movies", True)
        show_tv = info.data.get("show_tv", True)
        if show_movies is False and show_tv is False:
            raise ValueError("At least one of show_movies or show_tv must be True")
        return value


class Group(GroupUpdate):
    group_id: int
    created_on: date = Field(default='now()')
    
    model_config = ConfigDict(from_attributes=True)

class GroupQuery(Group):
    members: List[int]

class GroupMatch(BaseModel):
    group_id: int
    count_likes: int
    last_update: datetime
    movie: Movie

class GroupMatchQuery(BaseModel):
    group_members: int
    matches: List[GroupMatch]

class GroupMember(BaseModel):
    friend_code: str
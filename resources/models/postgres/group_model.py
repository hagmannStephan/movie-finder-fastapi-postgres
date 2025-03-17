from ...services.postgresql_service import Base
from sqlalchemy import (
    Column, Integer, String, Date, JSON, Boolean, CheckConstraint, ForeignKey
)
import json

class Group(Base):
    __tablename__ = "groups"
    group_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False, index=True)
    admin_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_on = Column(Date, nullable=False, default='now()')

    # Metadata about movie preferences
    show_movies = Column(Boolean, nullable=False, default=True)
    show_tv = Column(Boolean, nullable=False, default=True)

    settings_movies = Column(JSON, nullable=False, default=lambda: json.dumps({
        "include_adult": False,
        "language": "en-US",
        "release_date": {
            "gte": "1900-01-01",
            "lte": None
        },
        "vote_avrage": {
            "gte": 0,
            "lte": 10
        },
        "watch_region": None,
        "genres": {
            "include": [],
            "exclude": []
        },
        "with_runtime": {
            "gte": 0,
            "lte": 300
        },
        "watch_providers": []
    }))

    settings_tv = Column(JSON, nullable=False, default=lambda: json.dumps({
        "include_adult": False,
        "language": "en-US",
        "first_air_date": {
            "gte": "1900-01-01",
            "lte": None
        },
        "vote_avrage": {
            "gte": 0,
            "lte": 10
        },
        "watch_region": None,
        "genres": {
            "include": [],
            "exclude": []
        },
        "watch_providers": [],
    }))


    __table_args__ = (
        CheckConstraint('groups.show_movies = true OR groups.show_tv = true', name='check_at_least_one_true'),
    )
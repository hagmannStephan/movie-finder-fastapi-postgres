from ...services.postgresql_service import Base
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import (
    Column, Integer, String, DateTime, JSON, Boolean, CheckConstraint, Date
)


def default_session():
    return {
        "next_movies": [],
        "metadata_query": {
            "discover": {
                "movies": {
                    "popularity_desc": {
                        "page": 1,
                        "vote_count_gte": 1000,
                        "vote_avrage_gte": 6,
                        "vote_count_lte": None,
                        "vote_avrage_lte": None
                    },
                    "primary_release_date_desc": {
                        "release_date_gte": (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
                        "vote_count_gte": 50,
                        "vote_avrage_gte": 5
                    }
                },
                "tv": {
                    "popularity_desc": {
                        "page": 1,
                        "vote_count_gte": 1000,
                        "vote_avrage_gte": 6,
                        "vote_count_lte": None,
                        "vote_avrage_lte": None
                    },
                    "first_air_date_desc": {
                        "first_air_date_gte": (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
                        "vote_count_gte": 50,
                        "vote_avrage_gte": 5
                    }
                }
            },
            "group_matches": {
                "last_query": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            "similar": {
                "last_query": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
    }

def default_settings_movies():
    return {
        "include_adult": False,
        "language": "en-US",
        "release_date": {
            "gte": "1900-01-01",
            "lte": None
        },
        "vote_average": {
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
    }

def default_settings_tv():
    return {
        "include_adult": False,
        "language": "en-US",
        "first_air_date": {
            "gte": "1900-01-01",
            "lte": None
        },
        "vote_average": {
            "gte": 0,
            "lte": 10
        },
        "watch_region": None,
        "genres": {
            "include": [],
            "exclude": []
        },
        "watch_providers": [],
    }


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False)
    email = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    friend_code = Column(String(5), nullable=False, unique=True)
    created_on = Column(DateTime, nullable=False, server_default=func.now())
    last_login = Column(DateTime, nullable=True)

    # Metadata for algorithm
    session = Column(MutableDict.as_mutable(JSONB), nullable=False, default=default_session)

    # Metadata about movie preferences
    show_movies = Column(Boolean, nullable=False, default=True)
    show_tv = Column(Boolean, nullable=False, default=True)

    settings_movies = Column(JSON, nullable=False, default=default_settings_movies)
    settings_tv = Column(JSON, nullable=False, default=default_settings_tv)

    __table_args__ = (
        CheckConstraint('users.show_movies = true OR users.show_tv = true', name='check_at_least_one_true'),
    )

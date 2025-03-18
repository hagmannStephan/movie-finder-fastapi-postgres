from ...services.postgresql_service import Base
from sqlalchemy.sql import func
import json
from datetime import datetime, timedelta
from sqlalchemy import (
    Column, Integer, String, DateTime, JSON, Boolean, CheckConstraint, Date
)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False)
    email = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    friend_code = Column(String(5), nullable=False, unique=True)
    created_on = Column(DateTime, nullable=False, server_default=func.now())
    last_login = Column(DateTime, nullable=True)

    # Metadata for alogrithm
    # ----------------------------------------------------------------------------------------
    # Mix from the following
    # 1. Movies according to settings (if enabled)
    #   1.1 Discover via popularity_desc (page, vote_count_gte, vote_avrage_gte)
    #   1.2 Discover via primary_release_date.desc (release_date, vote_avrage, vote_count)
    # 2. TV Shows according to settings (if enabled)
    #   2.1 Discover via popularity_desc (page, vote_count desc., vote_avrage desc.)
    #   2.2 Discover via first_air_date.desc (release_date, vote_avrage, vote_count)
    # 3. Movies and TVs from friends
    #   3.1 Discover via group_matches that user hasn't liked / disliked yet but is part of
    # 4. Similar movies and TV show to already liked ones
    # ----------------------------------------------------------------------------------------
    session = Column(JSON, nullable=False, default=lambda: json.dumps({
        "next_movies": [],
        "metadata_query": {
            "discover": {
                "movies": {
                    "popularity_desc": {
                        # Increase by one with each query
                        # Set to 1 if last page reached
                        "page": 1,
                        # Lower if last page reached
                        # If not possible to go any lower, set to inital value
                        "vote_count_gte": 1000,
                        "vote_avrage_gte": 6,
                        # Set to previous _gte if last page reached
                        "vote_count_lte": None,
                        "vote_avrage_lte": None
                    },
                    "primary_release_date_desc": {
                        # Each time queried, set to current date
                        "release_date_gte": (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
                        "vote_count_gte": 50,
                        "vote_avrage_gte": 5
                    }
                },
                "tv": {
                    "popularity_desc": {
                        # Same as in movies
                        "page": 1,
                        "vote_count_gte": 1000,
                        "vote_avrage_gte": 6,
                        "vote_count_lte": None,
                        "vote_avrage_lte": None
                    },
                    "first_air_date_desc": {
                        # Same as in movies
                        "first_air_date_gte": (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
                        "vote_count_gte": 50,
                        "vote_avrage_gte": 5
                    }

                }
            },
            "group_matches": {
                # Update with each query to current date
                # Show users movies that got updated (liked/disliked) since the last time a query was made
                "last_query": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            "similar": {
                # Checkout movies that got liked since the last query
                "last_query": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
    }))

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
        CheckConstraint('users.show_movies = true OR users.show_tv = true', name='check_at_least_one_true'),
    )
from ...services.postgresql_service import Base
from sqlalchemy.sql import func
import json
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
    movie_session = Column(JSON, nullable=True)
    page = Column(Integer, nullable=False, default=1)
    latest_movie_date = Column(Date, nullable=True)

    # Metadata about movie preferences
    show_movies = Column(Boolean, nullable=False, default=True)
    show_tv = Column(Boolean, nullable=False, default=True)
    include_adult = Column(Boolean, nullable=False, default=False)
    language = Column(String(10), nullable=False, default='en-US')
    release_date_gte = Column(Date, nullable=True, default='1900-01-01')
    release_date_lte = Column(Date, nullable=True, server_default=func.now())
    watch_region = Column(String(10), nullable=True, default='CH')

    watch_providers = Column(JSON, nullable=True, default=lambda: json.dumps([]))        # TODO: Sync with watch providers from groups
    with_genres = Column(JSON, nullable=True, default=lambda: json.dumps([]))
    without_genres = Column(JSON, nullable=True, default=lambda: json.dumps([]))
    

    __table_args__ = (
        CheckConstraint('users.show_movies = true OR users.show_tv = true', name='check_at_least_one_true'),
    )
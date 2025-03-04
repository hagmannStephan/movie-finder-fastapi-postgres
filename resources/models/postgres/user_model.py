from ...services.postgresql_service import Base
from sqlalchemy import (
    Column, Integer, String, Date, JSON, Boolean, CheckConstraint
)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False)
    email = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(50), nullable=False)
    friend_code = Column(String(5), nullable=False, unique=True, fixed=True)
    created_on = Column(Date, nullable=False, default='now()')
    last_login = Column(Date, nullable=True)

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
    release_date_lte = Column(Date, nullable=True, default='now()')
    watch_region = Column(String(10), nullable=True, default='CH')
    watch_providers = Column(JSON, nullable=True, default=list)        # TODO: Sync with watch providers from groups
    with_genres = Column(JSON, nullable=True, default=list)
    without_genres = Column(JSON, nullable=True, default=list)
    

    __table_args__ = (
        CheckConstraint('users.show_movies = true OR users.show_tv = true', name='check_at_least_one_true'),
    )
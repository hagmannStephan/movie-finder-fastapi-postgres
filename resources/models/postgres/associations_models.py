from ...services.postgresql_service import Base
from sqlalchemy import (
    Table, Column, ForeignKey, Integer, DateTime
)

user_movies = Table(
    'user_likes', Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('movie_id', ForeignKey('movies.movie_id'), primary_key=True),
    Column('liked_on', DateTime, nullable=False)
)

group_matches = Table(
    'group_matches', Base.metadata,
    Column('group_id', ForeignKey('groups.group_id'), primary_key=True),
    Column('movie_id', ForeignKey('movies.movie_id'), primary_key=True),
    Column('count_likes', Integer, nullable=False),
    Column('last_update', DateTime, nullable=False)
)

group_users = Table(
    'group_members', Base.metadata,
    Column('group_id', ForeignKey('groups.group_id'), primary_key=True),
    Column('user_id', ForeignKey('users.user_id'), primary_key=True)
)
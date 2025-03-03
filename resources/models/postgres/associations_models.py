from ...services.postgresql_service import Base
from sqlalchemy import (
    Table, Column, ForeignKey
)

user_movie_association = Table(
    'user_likes', Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('movie_id', ForeignKey('movies.movie_id'), primary_key=True)
)

group_movie_association = Table(
    'group_matches', Base.metadata,
    Column('group_id', ForeignKey('groups.group_id'), primary_key=True),
    Column('movie_id', ForeignKey('movies.movie_id'), primary_key=True)
)

group_user_association = Table(
    'group_members', Base.metadata,
    Column('group_id', ForeignKey('groups.group_id'), primary_key=True),
    Column('user_id', ForeignKey('users.user_id'), primary_key=True)
)
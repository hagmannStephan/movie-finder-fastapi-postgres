from sqlalchemy.orm import Session
from fastapi import Depends
from resources.services.postgresql_service import get_db
import resources.models.postgres as postgers_models
import resources.schemas as schemas

def get_user_favourites(
        id: int,
        db: Session = Depends(get_db),
) -> list[schemas.Movie]:
    favourite_movies = (
        db.query(postgers_models.Movie)
        .join(postgers_models.user_movies)
        .filter(postgers_models.user_movies.c.user_id == id)
        .all()
    )
    return favourite_movies
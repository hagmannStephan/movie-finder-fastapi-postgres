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

def remove_user_favourite(
        id: int,
        movie_id: int,
        db: Session = Depends(get_db)
) -> schemas.Movie:
    user_favourites = get_user_favourites(id, db)
    for movie in user_favourites:
        if movie.movie_id == movie_id:
            db.query(postgers_models.user_movies).filter(
                postgers_models.user_movies.c.user_id == id,
                postgers_models.user_movies.c.movie_id == movie_id
            ).delete()
            db.commit()
            return movie
        
    raise Exception("Movie not found in user's favourites")
    
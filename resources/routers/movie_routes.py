from fastapi import APIRouter, HTTPException, Depends
from resources.services.auth_service import get_current_user
import resources.services.movie_service as movie_service
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from resources.services.postgresql_service import get_db
import os
import resources.schemas as schemas

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

headers = {
    "accept": "application/json",
    "Authorization": f'Bearer {TMDB_API_KEY}'
}

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
        responses={
        400: {"description": "Bad Request"},
        200: {"description": "Success"}
    }
)

@router.get(
        "/random",
        response_model=schemas.MovieProfile,
        description="Get a random movie",
        responses={
            "200": {"description": "Random movie found"},
            "429": {"description": "Rate limit exceeded after maximum retries"},
            "500": {"description": "Internal server error"}
        }
)
async def get_random_movie(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return await movie_service.get_random_movie(current_user, db)
    except Exception as e:
        if str(e) == "Rate limit exceeded after maximum retries":
            raise HTTPException(status_code=429, detail="Rate limit exceeded after maximum retries")
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/genres",
    response_model=schemas.GenreList,
    description="Get a list of movie genres",
    responses={
        "200": {"description": "Movie genres found"},
        "429": {"description": "Rate limit exceeded after maximum retries"},
        "500": {"description": "Internal server error"}
        }
)
async def get_movie_genres(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return await movie_service.get_movie_genres(db)
    except Exception as e:
        if str(e) == "Rate limit exceeded after maximum retries":
            raise HTTPException(status_code=429, detail="Rate limit exceeded after maximum retries")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post(
    "/{id}/right-swipe",
    response_model=schemas.MovieProfile,
    description="Like a movie",
    responses={
        "200": {"description": "Movie liked successfully"},
        "404": {"description": "Movie not found"},
        "500": {"description": "Internal server error"}
    }
)
async def like_movie(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db), id: int = None):
    try:
        return await movie_service.like_movie(current_user, db, id)
    except HTTPException as e:
        if str(e) == "Rate limit exceeded after maximum retries":
            raise HTTPException(status_code=429, detail="Rate limit exceeded after maximum retries")
        if str(e) == "Movie not found":
            raise HTTPException(status_code=404, detail="Movie not found")            
        raise HTTPException(status_code=500, detail="Internal server error")

# --------------------------------------------------------------------------------------------
# TODO: Implement these endpoints
# --------------------------------------------------------------------------------------------
# POST     /movies/{id}/right-swipe             Right swipe a movie
# POST     /movies/{id}/left-swipe              Left swipe a movie
# GET      /movies/search?query={keywords}      Search for movie by keywords
# GET      /movies/watch-providers/popular      Get a list of watch providers
# GET      /movies/watch-providers              Get all watch providers from region
# --------------------------------------------------------------------------------------------

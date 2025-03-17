from fastapi import APIRouter, HTTPException, Depends
from resources.services.auth_service import get_current_user
import resources.services.movie_service as movie_service
from dotenv import load_dotenv
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
    "/genres",
    response_model=schemas.GenreList,
    description="Get a list of movie genres",
    responses={
        "200": {"description": "Movie genres found"},    }
)
async def get_movie_genres(current_user: schemas.User = Depends(get_current_user)):
    try:
        return await movie_service.get_movie_genres()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    

# --------------------------------------------------------------------------------------------
# TODO: Implement these endpoints
# --------------------------------------------------------------------------------------------
# GET      /movies/random                       Get a random array of movies
# POST     /movies/{id}/right-swipe             Right swipe a movie
# POST     /movies/{id}/left-swipe              Left swipe a movie
# GET      /movies/search?query={keywords}      Search for movie by keywords
# GET      /movies/watch-providers              Get a list of watch providers
# --------------------------------------------------------------------------------------------

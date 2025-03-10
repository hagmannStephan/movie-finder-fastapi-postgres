from fastapi import APIRouter
from dotenv import load_dotenv
import os
import requests

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

# --------------------------------------------------------------------------------------------
# TODO: Implement these endpoints
# --------------------------------------------------------------------------------------------
# GET      /movies/random                       Get a random array of movies
# POST     /movies/{id}/right-swipe             Right swipe a movie
# POST     /movies/{id}/left-swipe              Left swipe a movie
# GET      /movies/search?query={keywords}      Search for movie by keywords
# --------------------------------------------------------------------------------------------

@router.get("/")
async def get_movies():
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    response = requests.get(url, headers=headers)
    
    return response.json()
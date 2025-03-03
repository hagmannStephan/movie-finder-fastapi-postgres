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

@router.get("/")
async def get_movies():
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    response = requests.get(url, headers=headers)
    
    return response.json()
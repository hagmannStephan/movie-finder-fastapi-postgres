from dotenv import load_dotenv
from fastapi import Depends
from resources.services.auth_service import get_current_user
from resources.services.postgresql_service import get_db
import os
import requests as req
import httpx
import asyncio
import resources.schemas as schemas
from sqlalchemy.orm import Session



load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_KEY}"
}


async def get_movie_genres():
    async with httpx.AsyncClient() as client:
        movie_task = client.get(f"{BASE_URL}/genre/movie/list?language=en", headers=headers)
        tv_task = client.get(f"{BASE_URL}/genre/tv/list?language=en", headers=headers)
        movie_response, tv_response = await asyncio.gather(movie_task, tv_task)
        return {
            "movie_genres": movie_response.json().get("genres"),
            "tv_genres": tv_response.json().get("genres")
        }
    
def get_random_movie(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pass
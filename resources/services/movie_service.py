from dotenv import load_dotenv
from fastapi import Depends
from resources.services.auth_service import get_current_user
from resources.services.postgresql_service import get_db
import resources.services.cache_service as cache_service
import os
import requests as req
import httpx
import asyncio
import resources.schemas as schemas
from sqlalchemy.orm import Session
from datetime import datetime, timedelta



load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_KEY}"
}

# TODO: Set timeout if return code is 429
async def get_movie_genres(
        db: Session = Depends(get_db)
):
    cache = cache_service.get_cache("movie_genres", db)

    # Only return the cache if it was updated within the last week
    if cache:
        updated_at = cache.updated_at
        if updated_at > datetime.now() - timedelta(weeks=1):
            return {"movie_genres": cache.value.get("movie_genres"), "tv_genres": cache.value.get("tv_genres")}
        
    async with httpx.AsyncClient() as client:
        movie_task = client.get(f"{BASE_URL}/genre/movie/list?language=en", headers=headers)
        tv_task = client.get(f"{BASE_URL}/genre/tv/list?language=en", headers=headers)
        movie_response, tv_response = await asyncio.gather(movie_task, tv_task)

        print ("Made a request to the API, got this: ", movie_response.json().get("genres"), tv_response.json().get("genres"))
        
        cache_service.update_cache("movie_genres", {
            "movie_genres": movie_response.json().get("genres"),
            "tv_genres": tv_response.json().get("genres")
        }, db)

        return cache_service.get_cache("movie_genres", db)

    
def get_random_movie(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pass
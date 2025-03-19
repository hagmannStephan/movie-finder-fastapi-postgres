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
import random


load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_KEY}"
}

MAX_RETRIES = 5
BASE_DELAY = 2  # seconds

async def get_with_retry(client, url, headers, retries=0):
    try:
        response = await client.get(url, headers=headers)
        
        # 429 means that to many requests were made
        if response.status_code == 429:
            if retries >= MAX_RETRIES:
                raise Exception(status_code=429, detail="Rate limit exceeded after maximum retries")
                
            # Calculate backoff with jitter to avoid synchronized retries
            delay = (BASE_DELAY ** retries) + (random.random() * 0.5)
            print(f"Rate limited. Retrying in {delay:.2f} seconds...")
            
            await asyncio.sleep(delay)
            return await get_with_retry(client, url, headers, retries + 1)
        
        # Raise an exception if there is an HTTP error
        response.raise_for_status()
        return response
        
    except httpx.HTTPStatusError as e:
        raise Exception(status_code=e.response.status_code, detail=str(e))


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
        movie_task = get_with_retry(client, f"{BASE_URL}/genre/movie/list?language=en", headers)
        tv_task = get_with_retry(client, f"{BASE_URL}/genre/tv/list?language=en", headers)
        movie_response, tv_response = await asyncio.gather(movie_task, tv_task)
        
        cache_service.update_cache("movie_genres", {
            "movie_genres": movie_response.json().get("genres"),
            "tv_genres": tv_response.json().get("genres")
        }, db)

        cache = cache_service.get_cache("movie_genres", db)

        return {"movie_genres": cache.value.get("movie_genres"), "tv_genres": cache.value.get("tv_genres")}

async def get_movies_by_popularity(
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    async with httpx.AsyncClient() as client:
        movies_by_popularity = await get_with_retry(
            client,
            f"{BASE_URL}/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc",
            headers
        )
        return movies_by_popularity
    
async def parse_movie_to_movieProfile(
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db),
        movie_id: int = None
):
    async with httpx.AsyncClient() as client:
        movie_detailed = get_with_retry(
            client,
            f"{BASE_URL}/movie/{movie_id}?language=en-US",
            headers
        )
        movie_keywords = get_with_retry(
            client,
            f"{BASE_URL}/movie/{movie_id}/keywords",
            headers
        )
        movie_additional_images = get_with_retry(
            client,
            f"{BASE_URL}/movie/{movie_id}/images?include_image_language=en",
            headers
        )
        movie_detailed, movie_keywords, movie_additional_images = await asyncio.gather(movie_detailed, movie_keywords, movie_additional_images)

        return {
            "id": movie_detailed.json().get("id"),
            "title": movie_detailed.json().get("title"),
            "genres": [schemas.Genre(**genre) for genre in movie_detailed.json().get("genres", [])],
            "overview": movie_detailed.json().get("overview") or "",
            "release_date": datetime.strptime(movie_detailed.json().get("release_date"), "%Y-%m-%d").date() if movie_detailed.json().get("release_date") else None,
            "vote_average": movie_detailed.json().get("vote_average"),
            "vote_count": movie_detailed.json().get("vote_count"),
            "runtime": movie_detailed.json().get("runtime"),
            "tagline": movie_detailed.json().get("tagline") or "",
            "keywords": [kw["name"] for kw in movie_keywords.json().get("keywords", [])] or "",
            "poster_path": movie_detailed.json().get("poster_path"),
            "backdrop_path": movie_detailed.json().get("backdrop_path") or "",
            "images_path": [img["file_path"] for img in movie_additional_images.json().get("backdrops", [])]
        }

    
async def get_random_movie(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # TODO: Discover should always return a new movie according to use settings
    # TODO: Save relevant movies in db
    # TODO: Implement other datasources
    movies_by_popularity = await get_movies_by_popularity(current_user, db)
    movie_profile = await parse_movie_to_movieProfile(current_user, db, movies_by_popularity.json().get("results")[0].get("id"))

    return movie_profile
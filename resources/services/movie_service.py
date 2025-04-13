from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from resources.services.auth_service import get_current_user
from resources.services.postgresql_service import get_db
import resources.services.cache_service as cache_service
import os
import httpx
import asyncio
import resources.schemas as schemas
from sqlalchemy.orm import Session, attributes
from datetime import datetime, timedelta
import random
from typing import Dict, Any, Optional
import resources.models.postgres as postgers_models

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
                raise HTTPException(status_code=429, detail="Rate limit exceeded after maximum retries")
                
            # Calculate backoff with jitter to avoid synchronized retries
            delay = (BASE_DELAY ** retries) + (random.random() * 0.5)
            print(f"Rate limited. Retrying in {delay:.2f} seconds...")
            
            await asyncio.sleep(delay)
            return await get_with_retry(client, url, headers, retries + 1)
        
        # Raise an exception if there is an HTTP error
        response.raise_for_status()
        return response
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))



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
        movie_watch_providers = get_with_retry(
            client,
            f"{BASE_URL}/movie/{movie_id}/watch/providers",
            headers
        )
        movie_detailed, movie_keywords, movie_additional_images, movie_watch_providers = await asyncio.gather(movie_detailed, movie_keywords, movie_additional_images, movie_watch_providers)

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
            "keywords": [kw["name"] for kw in movie_keywords.json().get("keywords", [])],
            "poster_path": movie_detailed.json().get("poster_path"),
            "backdrop_path": movie_detailed.json().get("backdrop_path") or "",
            "images_path": [img["file_path"] for img in movie_additional_images.json().get("backdrops", [])],
            "watch_providers": movie_watch_providers.json().get("results", {}).get("CH", {})
        }
    
def save_movie_to_db():
    # TODO: Implement this function to make code for like and dislike less redundant
    pass

def get_user_session(
    current_user: schemas.User,
    db: Session
) -> Optional[Dict[str, Any]]:
    user = db.query(postgers_models.User).filter(postgers_models.User.user_id == current_user.user_id).first()
    if user:
        return user.session
    return None


def update_user_session(
    session: Dict[str, Any],
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from sqlalchemy.orm import attributes
    
    user = db.query(postgers_models.User).filter(postgers_models.User.user_id == current_user.user_id).first()
    if user:
        user.session = session
        attributes.flag_modified(user, "session")
        db.commit()
        return {"message": "Session updated successfully"}
    return {"message": "User not found"}
    
async def get_random_movie(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = get_user_session(current_user, db)

    # TODO: Pay attention to use settings and movie session methods
    # TODO: Implement other datasources (likes from other users, latest releases, similar to already liked movies, etc.)

    if len(session["next_movies"]) < 15:
        movies_by_popularity = await get_movies_by_popularity(current_user, db)

        for movie in movies_by_popularity.json().get("results", []):
            session["next_movies"].append(movie.get("id"))
            update_user_session(session, current_user, db)
            id = movies_by_popularity.json().get("results")[0].get("id")
              
    else:
        id = session["next_movies"][0]
    
    # TODO: Save relevant movies in db
    # TODO: Get likes of the movies in db from user

    # If movie doesn't exsist - load it
    movie_profile = await parse_movie_to_movieProfile(current_user, db, id)
    
    return movie_profile

async def like_movie(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    id: int = None
):
    # Check if movie is in session, if yes - remove it from session
    user = db.query(postgers_models.User).filter(postgers_models.User.user_id == current_user.user_id).first()
    
    if user and id in user.session["next_movies"]:
        user.session["next_movies"].remove(id)
        
        # Explicitly mark the session column as modified
        attributes.flag_modified(user, "session")
        
        # Commit the changes
        db.commit()

    # Like movie by updating the user_movies table
    user = db.query(postgers_models.User).filter(postgers_models.User.user_id == current_user.user_id).first()

    # Ensure movie exists
    movie = db.query(postgers_models.Movie).filter(postgers_models.Movie.movie_id == id).first()
    if not movie:
        movie_profile = await parse_movie_to_movieProfile(current_user, db, id)
        
        movie = postgers_models.Movie(
            movie_id=movie_profile["id"],
            title=movie_profile["title"],
            genres=[genre.dict() for genre in movie_profile["genres"]],
            overview=movie_profile["overview"],
            release_date=movie_profile["release_date"].strftime("%Y-%m-%d") if movie_profile["release_date"] else None,
            vote_average=movie_profile["vote_average"],
            vote_count=movie_profile["vote_count"],
            runtime=movie_profile["runtime"],
            tagline=movie_profile["tagline"],
            keywords=movie_profile["keywords"],
            poster_path=movie_profile["poster_path"],
            backdrop_path=movie_profile["backdrop_path"],
            images_path=movie_profile["images_path"],
            watch_providers=movie_profile["watch_providers"],
        )
        db.add(movie)
        db.commit()
        db.refresh(movie)

    # Check if already liked
    already_liked = db.execute(
        postgers_models.user_movies.select().where(
            (postgers_models.user_movies.c.user_id == user.user_id) &
            (postgers_models.user_movies.c.movie_id == id)
        )
    ).first()

    if not already_liked:
        db.execute(
            postgers_models.user_movies.insert().values(
                user_id=user.user_id,
                movie_id=id,
                liked_on=datetime.now()
            )
        )
        
        # Update or create entry in the group_matches table
        # 1. Get all groups the user is part of
        group_users = db.query(postgers_models.Group).join(
            postgers_models.group_users,
            postgers_models.group_users.c.group_id == postgers_models.Group.group_id
        ).filter(
            postgers_models.group_users.c.user_id == user.user_id
        ).all()
        
        current_time = datetime.now()
        
        # 2. For each group, update or create a group_matches entry
        for group in group_users:
            # Check if there's an existing match for this group and movie
            existing_match = db.execute(
                postgers_models.group_matches.select().where(
                    (postgers_models.group_matches.c.group_id == group.group_id) &
                    (postgers_models.group_matches.c.movie_id == id)
                )
            ).first()
            
            if existing_match:
                # 3. If yes: Increment count_likes and update last_update
                db.execute(
                    postgers_models.group_matches.update().where(
                        (postgers_models.group_matches.c.group_id == group.group_id) &
                        (postgers_models.group_matches.c.movie_id == id)
                    ).values(
                        count_likes=existing_match.count_likes + 1,
                        last_update=current_time
                    )
                )
            else:
                # 4. If no: Add a new entry with count_likes=1
                db.execute(
                    postgers_models.group_matches.insert().values(
                        group_id=group.group_id,
                        movie_id=id,
                        count_likes=1,
                        last_update=current_time
                    )
                )
        
        # Commit the changes for all group matches
        db.commit()
        
    return movie

async def dislike_movie(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    id: int = None
):
    # Get user directly from the database
    user = db.query(postgers_models.User).filter(postgers_models.User.user_id == current_user.user_id).first()
    
    # Check if movie is in session, if yes - remove it
    if user and id in user.session["next_movies"]:
        user.session["next_movies"].remove(id)
        
        # Explicitly mark the session column as modified
        from sqlalchemy.orm import attributes
        attributes.flag_modified(user, "session")
        
        # Commit the changes
        db.commit()
    
    # Ensure movie exists in database
    movie = db.query(postgers_models.Movie).filter(postgers_models.Movie.movie_id == id).first()
    
    # If movie doesn't exist in our database, fetch it from external API
    if not movie:
        movie_profile = await parse_movie_to_movieProfile(current_user, db, id)
        
        movie = postgers_models.Movie(
            movie_id=movie_profile["id"],
            title=movie_profile["title"],
            genres=[genre.dict() for genre in movie_profile["genres"]],
            overview=movie_profile["overview"],
            release_date=movie_profile["release_date"].strftime("%Y-%m-%d") if movie_profile["release_date"] else None,
            vote_average=movie_profile["vote_average"],
            vote_count=movie_profile["vote_count"],
            runtime=movie_profile["runtime"],
            tagline=movie_profile["tagline"],
            keywords=movie_profile["keywords"],
            poster_path=movie_profile["poster_path"],
            backdrop_path=movie_profile["backdrop_path"],
            images_path=movie_profile["images_path"],
            watch_providers=movie_profile["watch_providers"],
        )
        db.add(movie)
        db.commit()
        db.refresh(movie)
    
    return movie

async def search_movies(
    keywords: str,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    url = f"{BASE_URL}/search/multi?query={keywords}&include_adult=false&language=en-US&page=1"

    async with httpx.AsyncClient() as client:
        response = await get_with_retry(client, url, headers)

        # Filter for only movie types
        results = response.json().get("results", [])
        # filtered = [item for item in results if item.get("media_type") == {"movie", "tv"}]
        filtered = [item for item in results if item.get("media_type") == "movie"]

        # Parse each movie to MovieProfile
        profiles = []
        for item in filtered:
            movie_id = item.get("id")
            profile = await parse_movie_to_movieProfile(
                current_user=current_user,
                db=db,
                movie_id=movie_id
            )
            profiles.append(profile)

        return profiles

async def get_watch_providers(
        db: Session = Depends(get_db)
):
    cache = cache_service.get_cache("watch_providers", db)

    # Only return the cache if it was updated within the last week
    if cache:
        updated_at = cache.updated_at
        if updated_at > datetime.now() - timedelta(weeks=1):
            return cache.value.get("watch_providers")
        
    async with httpx.AsyncClient() as client:
        watch_providers = await get_with_retry(
            client,
            f"{BASE_URL}/watch/providers/movie?language=en-US&watch_region=CH",
            headers
        )
        
        parsed_providers = [
            {
            "provider_id": provider.get("provider_id"),
            "provider_name": provider.get("provider_name"),
            "logo_path": provider.get("logo_path")
            }
            for provider in watch_providers.json().get("results", [])
        ]

        cache_service.update_cache("watch_providers", {
            "watch_providers": parsed_providers
        }, db)

        cache = cache_service.get_cache("watch_providers", db)

        return cache.value.get("watch_providers")
    
async def get_popular_watch_providers(
        db: Session = Depends(get_db)
):
    all_providers = await get_watch_providers(db)

    # Netflix (id: 8)
    # Amazon Prime Video (id: 119)
    # Disney Plus (id: 337)
    # blue TV (id: 150)
    # Apple TV (id: 2)
    # Play Suisse (id: 691)
    popular_provider_ids = {8, 119, 337, 150, 2, 691}

    filtered_providers = [
        provider for provider in all_providers
        if provider.get("provider_id") in popular_provider_ids
    ]

    return filtered_providers
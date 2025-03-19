from fastapi import APIRouter, Depends, HTTPException, status
import resources.schemas as schemas
from resources.services.postgresql_service import get_db
from sqlalchemy.orm import Session
import resources.models.postgres as postgers_models
from resources.services.auth_service import get_current_user
import resources.services.user_service as user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
        "/",
        response_model=schemas.UserCreated,
        description="Create a new user",
        responses={
            "200": {"description": "User created"},
            "400": {"description": "User with Email already exists"},
            "500": {"description": "Internal server error"}
        }
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(user, db)
    except ValueError as e:
        if str(e) == "Email already registered":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get(
        "/me", 
        response_model=schemas.User,
        description="Get current user",
        responses={
            "200": {"description": "User found"},
            "401": {"description": "User not authenticated"}
        }
)
def read_current_user(current_user: postgers_models.User = Depends(get_current_user)):
    return current_user


@router.get(
        "/{id}/favourites",
        response_model=list[schemas.MovieProfile],
        description="Get liked movies of a user",
        responses={
            "200": {"description": "User found"},
            "401": {"description": "User not authorized"},
            "500": {"description": "Internal server error"}
        }
)
def get_user_favourites(id: int, current_user: postgers_models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_id != id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized"
        )
    try:
        return user_service.get_user_favourites(id, db)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete(
        "/{id}/favourites/{movieId}",
        response_model=schemas.MovieProfile,
        description="Remove a movie from the user's favourites",
        responses={
            "200": {"description": "Movie removed"},
            "401": {"description": "User not authorized"},
            "404": {"description": "Movie not found"},
            "500": {"description": "Internal server error"}
        }
)
def remove_user_favourite(id: int, movieId: int, current_user: postgers_models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_id != id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized"
        )
    try:
        return user_service.remove_user_favourite(id, movieId, db)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    

@router.patch(
        "/{id}/settings",
        response_model=schemas.UserPatchSettings,
        description="Update user settings",
        responses={
            "200": {"description": "Settings updated"},
            "401": {"description": "User not authorized"},
            "500": {"description": "Internal server error"}
        }
)
def update_user_settings(id: int, settings: schemas.UserPatchSettings, current_user: postgers_models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_id != id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized"
        )
    try:
        return user_service.update_user_settings(id, settings, db)
    except Exception as e:
        print(e)
        raise


@router.delete(
        "/{id}",
        response_model=schemas.User,
        description="Delete a user",
        responses={
            "200": {"description": "User deleted"},
            "401": {"description": "User not authorized"},
            "500": {"description": "Internal server error"}
        }
)
def delete_user(id: int, current_user: postgers_models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_id != id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized"
        )
    try:
        return user_service.delete_user(id, db)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get(
        "/{id}/groups",
        response_model=list[schemas.Group],
        description="Get groups of a user",
        responses={
            "200": {"description": "Groups found"},
            "401": {"description": "User not authorized"},
            "500": {"description": "Internal server error"}
        }
)
def get_user_groups(id: int, current_user: postgers_models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_id != id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized"
        )
    try:
        return user_service.get_user_groups(id, db)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

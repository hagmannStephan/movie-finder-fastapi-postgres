from fastapi import APIRouter, Depends, HTTPException, status
import resources.schemas as schemas
from resources.services.postgresql_service import get_db
from sqlalchemy.orm import Session
import resources.models.postgres as postgers_models
import secrets
from resources.services.auth_service import get_password_hash, get_current_user
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
            200: {"description": "User created"},
            400: {"description": "User with Email already exists"}
        }
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(postgers_models.User).filter(postgers_models.User.email == user.email).first()

    # Check if user already exists
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    while True:
        friend_code = secrets.token_hex(5)[:5].upper()
        
        if not db.query(postgers_models.User).filter(postgers_models.User.friend_code == friend_code).first():
            break
    
    # Create a new user
    hashed_password = get_password_hash(user.password)
    db_user = postgers_models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        friend_code=friend_code
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get(
        "/me", 
        response_model=schemas.User,
        description="Get current user",
        responses={
            200: {"description": "User found"},
            401: {"description": "User not authenticated"}
        }
)
def read_current_user(current_user: postgers_models.User = Depends(get_current_user)):
    return current_user


@router.get(
        "/{id}/favourites",
        response_model=list[schemas.Movie],
        description="Get liked movies of a user",
        responses={
            200: {"description": "User found"},
            401: {"description": "User not authorized"}
        }
)
def get_user_favourites(id: int, current_user: postgers_models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_id != id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized"
        )
    return user_service.get_user_favourites(id, db)
    

# --------------------------------------------------------------------------------------------
# - DELETE  /users/{id}/favourites/{movieId}
# - PATCH   /users/{id}/settings
# - DELETE  /users/{id}
# - GET     /users/{id}/groups
# --------------------------------------------------------------------------------------------
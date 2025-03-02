from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from resources.postgres.database import engine, SessionLocal, get_db
from resources.auth.auth import get_password_hash, verify_password
import resources.postgres.models as models
import resources.postgres.schemas as schemas

app = FastAPI(
    title="Movie Finder - Backend",
    description="FastAPI backend with PostgreSQL and Redis",
    version="0.1.0"
)

models.Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}


@app.post("/users", response_model=schemas.User, tags=["Auth"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.name == user.name).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Create new user with hashed password
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
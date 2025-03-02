from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from resources.postgres.database import engine, SessionLocal
import resources.postgres.models as models
import resources.postgres.schemas as schemas

app = FastAPI(
    title="Movie Finder - Backend",
    description="FastAPI backend with PostgreSQL and Redis",
    version="0.1.0"
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}


@app.post("/items", response_model=schemas.Item, tags=["Items"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(
        **item.model_dump()
	)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

@app.get("/items", response_model=List[schemas.Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    
    return items
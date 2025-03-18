from sqlalchemy.orm import Session
import resources.models.postgres as postgers_models

def get_cache(
        key: str,
        db: Session
):
    cache = db.query(postgers_models.Cache).filter(postgers_models.Cache.key == key).first()
    
    if not cache:
        return None
    
    return cache

def create_cache(
        key: str,
        value: dict,
        db: Session
):
    cache = postgers_models.Cache(
        key=key,
        value=value
    )
    
    db.add(cache)
    db.commit()
    db.refresh(cache)
    
    return cache

def update_cache(
        key: str,
        value: dict,
        db: Session
):
    cache = db.query(postgers_models.Cache).filter(postgers_models.Cache.key == key).first()

    if not cache:
        cache = create_cache(key, value, db)
    
    cache.value = value
    db.commit()
    db.refresh(cache)
    
    return cache
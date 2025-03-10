from sqlalchemy.orm import Session
from fastapi import Depends
from resources.services.postgresql_service import get_db
import resources.models.postgres as postgers_models
import resources.schemas as schemas

def delete_group(
        id: int,
        db: Session = Depends(get_db)
) -> schemas.Group:
    group = db.query(postgers_models.Group).filter(postgers_models.Group.group_id == id).first()

    # Delete group references from related tables
    db.query(postgers_models.group_users).filter(postgers_models.group_users.c.group_id == id).delete()
    db.query(postgers_models.group_matches).filter(postgers_models.group_matches.c.group_id == id).delete()

    db.delete(group)
    db.commit()
    return group
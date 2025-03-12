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

def create_group(
        group: schemas.GroupCreate,
        current_user: schemas.User,
        db: Session = Depends(get_db)
) -> schemas.Group:
    db_group = postgers_models.Group(
        name=group.name,
        admin_id=current_user.user_id
    )

    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    return db_group

def get_group(
        id: int,
        current_user: schemas.User,
        db: Session = Depends(get_db)
) -> schemas.GroupQuery:
    group = db.query(postgers_models.Group).filter(postgers_models.Group.group_id == id).first()

    members = db.query(postgers_models.group_users.c.user_id).filter(postgers_models.group_users.c.group_id == id).all()
    member_ids = [member.user_id for member in members]

    if not group:
        raise Exception("Group not found")

    if group.admin_id != current_user.user_id or current_user.user_id not in member_ids:
        raise Exception("User not authorized")

    return schemas.GroupQuery(
        **group.__dict__,
        members=member_ids
    )
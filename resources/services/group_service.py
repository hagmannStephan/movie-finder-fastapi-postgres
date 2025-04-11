from sqlalchemy.orm import Session
from fastapi import Depends
from resources.services.postgresql_service import get_db
import json
import resources.models.postgres as postgers_models
import resources.schemas as schemas

def delete_group_helper(
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

    if (group.admin_id != current_user.user_id 
        and current_user.user_id not in member_ids):
        raise Exception("User not authorized")

    return schemas.GroupQuery(
        **group.__dict__,
        members=member_ids
    )

def update_group(
        id: int,
        original_group: schemas.Group,
        current_user: schemas.User,
        db: Session = Depends(get_db)
) -> schemas.Group:
    group = db.query(postgers_models.Group).filter(postgers_models.Group.group_id == id).first()

    if not group:
        raise Exception("Group not found")
    
    if (group.admin_id != original_group.admin_id and current_user.user_id != original_group.admin_id):
        raise Exception("User not authorized")
    
    for key, value in original_group.dict().items():
        setattr(group, key, value)
    db.commit()
    return group

def add_group_member(
        id: int,
        member: schemas.GroupMember,
        current_user: schemas.User,
        db: Session = Depends(get_db)
) -> schemas.GroupQuery:
    group = db.query(postgers_models.Group).filter(postgers_models.Group.group_id == id).first()
    user = db.query(postgers_models.User).filter(postgers_models.User.friend_code == member.friend_code).first()

    if not group:
        raise Exception("Group not found")

    if (group.admin_id != current_user.user_id
        or not user):
        raise Exception("User not authorized")

    db_group_user = postgers_models.group_users.insert().values(
        group_id=id,
        user_id=user.user_id
    )

    db.execute(db_group_user)
    db.commit()

    return get_group(id, current_user, db)

def remove_group_member(
        id: int,
        member_id: int,
        current_user: schemas.User,
        db: Session = Depends(get_db)
) -> schemas.GroupQuery:
        group = db.query(postgers_models.Group).filter(postgers_models.Group.group_id == id).first()

        members = db.query(postgers_models.group_users.c.user_id).filter(postgers_models.group_users.c.group_id == id).all()
        member_ids = [member.user_id for member in members]

        if not group:
            raise Exception("Group not found")
        
        if member_id not in member_ids:
            raise Exception("Member not found")
        
        if (group.admin_id != current_user.user_id 
            or member_id == current_user.user_id):
            raise Exception("User not authorized")
        
        db.query(postgers_models.group_users).filter(
            postgers_models.group_users.c.group_id == id,
            postgers_models.group_users.c.user_id == member_id
        ).delete()
        db.commit()

        return get_group(id, current_user, db)

def delete_group(
        id: int,
        current_user: schemas.User,
        db: Session = Depends(get_db)
) -> schemas.Group:
    group = db.query(postgers_models.Group).filter(postgers_models.Group.group_id == id).first()

    if not group:
        raise Exception("Group not found")

    if group.admin_id != current_user.user_id:
        raise Exception("User not authorized")

    return delete_group_helper(id, db)

def get_group_matches(
        id: int,
        current_user: schemas.User,
        db: Session = Depends(get_db)
) -> schemas.GroupMatchQuery:
    group = db.query(postgers_models.Group).filter(postgers_models.Group.group_id == id).first()

    members = db.query(postgers_models.group_users.c.user_id).filter(postgers_models.group_users.c.group_id == id).all()
    member_ids = [member.user_id for member in members]

    if not group:
        raise Exception("Group not found")

    if group.admin_id != current_user.user_id and current_user.user_id not in member_ids:
        raise Exception("User not authorized")

    matches = db.query(postgers_models.group_matches).filter(postgers_models.group_matches.c.group_id == id).all()
    match_dicts = []

    for match in matches:
        movie = db.query(postgers_models.Movie).filter(postgers_models.Movie.movie_id == match.movie_id).first()
        
        if not movie:
            continue

        movie_profile = schemas.MovieProfile(
            id=movie.movie_id,
            title=movie.title or "",
            genres = [
                schemas.Genre(name=g) if isinstance(g, str) else schemas.Genre(name=g.get('name', ''), id=g.get('id', 0))
                for g in movie.genres
            ] if movie.genres else [],
            overview=movie.overview or "",
            release_date=movie.release_date or "",
            vote_average=movie.vote_average or 0.0,
            vote_count=movie.vote_count or 0,
            runtime=movie.runtime or 0,
            tagline=movie.tagline or "",
            keywords=movie.keywords or [],
            poster_path=movie.poster_path or "",
            backdrop_path=movie.backdrop_path or "",
            images_path=movie.images_path or []
        )

        # Create the match dictionary
        match_dict = schemas.GroupMatch(
            **match._asdict(),
            movie=movie_profile
        )
        match_dicts.append(match_dict)

    return schemas.GroupMatchQuery(
        group_id=id,
        group_members=len(member_ids),
        matches=match_dicts,
    )
from fastapi import APIRouter, Depends, HTTPException
import resources.schemas as schemas
import resources.services.group_service  as group_service
from resources.services.auth_service import get_current_user
from resources.services.postgresql_service import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)


@router.post(
    "/",
    response_model=schemas.Group,
    description="Create a new group",
    responses={
        "200": {"description": "Group created"},
        "500": {"description": "Internal server error"}
    }
)
def create_group(group: schemas.GroupCreate, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return group_service.create_group(group, current_user, db)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/{id}",
    response_model=schemas.GroupQuery,
    description="Get a group with its members, settings, etc.",
    responses={
        "200": {"description": "Group found"},
        "404": {"description": "Group not found"},
        "401": {"description": "User not authorized"},
        "500": {"description": "Internal server error"}
    }
)
def get_group(id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return group_service.get_group(id, current_user, db)
    except Exception as e:
        if str(e) == "Group not found":
            raise HTTPException(status_code=404, detail="Group not found")
        elif str(e) == "User not authorized":
            raise HTTPException(status_code=401, detail="User not authorized")
        else:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error")
        
@router.patch(
    "/{id}",
    response_model=schemas.Group,
    description="Update a group (settings, admin or name)",
    responses={
        "200": {"description": "Group updated"},
        "404": {"description": "Group not found"},
        "401": {"description": "User not authorized"},
        "500": {"description": "Internal server error"}
    }
)
def update_group(id: int, group: schemas.Group, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return group_service.update_group(id, group, current_user, db)
    except Exception as e:
        if str(e) == "Group not found":
            raise HTTPException(status_code=404, detail="Group not found")
        elif str(e) == "User not authorized":
            raise HTTPException(status_code=401, detail="User not authorized")
        else:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error")
        
@router.post(
    "/{id}/members",
    response_model=schemas.GroupQuery,
    description="Add a member with friendship code to a group",
    responses={
        "200": {"description": "Member added"},
        "404": {"description": "Group not found"},
        "401": {"description": "User not authorized"},
        "500": {"description": "Internal server error"}
    }
)
def add_group_member(id: int, member: schemas.GroupMember, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return group_service.add_group_member(id, member, current_user, db)
    except Exception as e:
        if str(e) == "Group not found":
            raise HTTPException(status_code=404, detail="Group not found")
        elif str(e) == "User not authorized":
            raise HTTPException(status_code=401, detail="User not authorized")
        else:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error")

@router.delete(
    '/{id}/members/{member_id}',
    response_model=schemas.GroupQuery,
    description="Remove a member from a group (or leave the group)",
    responses={
        "200": {"description": "Member removed"},
        "404": {"description": "Group not found"},
        "404": {"description": "Member not found"},
        "401": {"description": "User not authorized"},
        "500": {"description": "Internal server error"}
    }
)
def remove_group_member(id: int, member_id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return group_service.remove_group_member(id, member_id, current_user, db)
    except Exception as e:
        if str(e) == "Group not found":
            raise HTTPException(status_code=404, detail="Group not found")
        elif str(e) == "Member not found":
            raise HTTPException(status_code=404, detail="Member not found")
        elif str(e) == "User not authorized":
            raise HTTPException(status_code=401, detail="User not authorized")
        else:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error")
        
@router.delete(
    '/{id}',
    response_model=schemas.Group,
    description="Delete a group",
    responses={
        "200": {"description": "Group deleted"},
        "404": {"description": "Group not found"},
        "401": {"description": "User not authorized"},
        "500": {"description": "Internal server error"}
    }
)
def delete_group(id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return group_service.delete_group(id, current_user, db)
    except Exception as e:
        if str(e) == "Group not found":
            raise HTTPException(status_code=404, detail="Group not found")
        elif str(e) == "User not authorized":
            raise HTTPException(status_code=401, detail="User not authorized")
        else:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error")
        
@router.get(
    '/{id}/matches',
    response_model=schemas.GroupMatchQuery,
    description="Get matches of a group (and close matches)",
    responses={
        "200": {"description": "Matches found"},
        "404": {"description": "Group not found"},
        "401": {"description": "User not authorized"},
        "500": {"description": "Internal server error"}
    }
)
def get_group_matches(id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return group_service.get_group_matches(id, current_user, db)
    except Exception as e:
        if str(e) == "Group not found":
            raise HTTPException(status_code=404, detail="Group not found")
        elif str(e) == "User not authorized":
            raise HTTPException(status_code=401, detail="User not authorized")
        else:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error")
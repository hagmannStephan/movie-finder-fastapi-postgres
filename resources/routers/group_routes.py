from fastapi import APIRouter, Depends
import resources.schemas as schemas
import resources.services.group_service  as group_service
from resources.services.auth_service import get_current_user


router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)


@router.post(
    "/",
    description="Create a new group",
    responses={
        "200": {"description": "Group created"},
    }
)
def create_group(group: schemas.GroupCreate, current_user: schemas.User = Depends(get_current_user)):
    return group_service.create_group(group, current_user)

# --------------------------------------------------------------------------------------------
# TODO: Implement these endpoints
# --------------------------------------------------------------------------------------------
# GET       /groups/{id}                Get a group with its members, settings, etc.
# PATCH     /groups/{id}                Update a group (settings, admin or name)
# POST      /groups/{id}/members        Add a member with friendship code to a group
# DELETE    /groups/{id}/members/{id}   Remove a member from a group (or leave the group)
# DELETE    /groups/{id}                Delete a group
# GET       /groups/{id}/matches        Get matches of a group
# --------------------------------------------------------------------------------------------
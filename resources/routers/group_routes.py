from fastapi import APIRouter

router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)

# --------------------------------------------------------------------------------------------
# TODO: Implement these endpoints
# --------------------------------------------------------------------------------------------
# POST      /groups                     Create a new group
# GET       /groups/{id}                Get a group with its members, settings, etc.
# PATCH     /groups/{id}                Update a group (settings, admin or name)
# POST      /groups/{id}/members        Add a member with friendship code to a group
# DELETE    /groups/{id}/members/{id}   Remove a member from a group (or leave the group)
# DELETE    /groups/{id}                Delete a group
# GET       /groups/{id}/matches        Get matches of a group
# --------------------------------------------------------------------------------------------
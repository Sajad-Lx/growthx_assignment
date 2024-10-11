from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.assignment_schema import AssignmentListResponse, AssignmentUpdate, AssignmentUpdateResponse
from app.services.admin_service import register_admin, login_admin, get_assignments_for_admin, update_assignment_status
from app.schemas.user_schema import UserCreate, UserCreateResponse, UserLogin, UserLoginResponse

router = APIRouter()


@router.post("/register", response_model=UserCreateResponse, summary="Register admin")
async def register_admin_endpoint(admin: UserCreate):
    """
    Registers a new admin.

    Args:
        admin (UserCreate): The admin data for registration.

    Returns:
        UserCreateResponse: The result of the registration.
    """
    result = await register_admin(admin)
    return result


@router.post("/login", response_model=UserLoginResponse, summary="Login Admin")
async def login_admin_endpoint(admin: Annotated[UserLogin, Depends()]):
    """
    Authenticates an admin and returns admin data with a JWT token.

    Args:
        admin (UserLogin): The admin login data.

    Returns:
        UserLoginResponse: The authenticated admin details and token.
    """
    admin_data = await login_admin(admin)
    return admin_data


@router.get("/assignments", response_model=AssignmentListResponse, summary="Get all assignments")
async def get_assignments_endpoint(current_user: Annotated[User, Depends(get_current_active_user)], admin: str | None = None):
    """
    Retrieves all assignments for the logged-in admin. If optional admin name is provided then will retrieve that Admin's assignments.

    Args:
        current_user (User): The current authenticated admin.
        Optional admin (str): The name of Admin.

    Returns:
        AssignmentListResponse: A list of assignments for the admin.
    """
    assignments = await get_assignments_for_admin(current_user, admin)
    return assignments


@router.post("/assignments/{id}/accept", response_model=AssignmentUpdateResponse, summary="Update assignment status as accepted")
async def accept_assignment_endpoint(id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    Updates the status of an assignment to accepted.

    Args:
        id (str): The assignment ID.
        current_user (User): The current authenticated admin.

    Returns:
        AssignmentUpdateResponse: The result of the update.
    """
    result = await update_assignment_status(AssignmentUpdate(assignment_id=id, status="accepted"), current_user)
    return result


@router.post("/assignments/{id}/reject", response_model=AssignmentUpdateResponse, summary="Update assignment status as rejected")
async def reject_assignment_endpoint(id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    Updates the status of an assignment to rejected.

    Args:
        id (str): The assignment ID.
        current_user (User): The current authenticated admin.

    Returns:
        AssignmentUpdateResponse: The result of the update.
    """
    result = await update_assignment_status(AssignmentUpdate(assignment_id=id, status="rejected"), current_user)
    return result

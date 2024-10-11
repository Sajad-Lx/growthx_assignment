from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.assignment_schema import AssignmentCreate
from app.services.user_service import register_user, login_user, upload_assignment, get_admins
from app.schemas.user_schema import AdminListResponse, UserAssignmentUploadResponse, UserCreate, UserCreateResponse, UserLogin, UserLoginResponse

router = APIRouter()


@router.post("/register", response_model=UserCreateResponse, summary="Register user")
async def register_user_endpoint(user: UserCreate):
    """
    Registers a new user.

    Args:
        user (UserCreate): The user data for registration.

    Returns:
        UserCreateResponse: The result of the registration.
    """
    result = await register_user(user)
    return result


@router.post("/login", response_model=UserLoginResponse, summary="Login user")
async def login_user_endpoint(user: Annotated[UserLogin, Depends()]):
    """
    Authenticates a user and returns user data with a JWT token.

    Args:
        user (UserLogin): The user login data.

    Returns:
        UserLoginResponse: The authenticated user details and token.
    """
    user_data = await login_user(user)
    return user_data


@router.post("/upload", response_model=UserAssignmentUploadResponse, summary="Upload assignment")
async def upload_assignment_endpoint(assignment: AssignmentCreate, current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    Uploads an assignment for the logged-in user.

    Args:
        assignment (AssignmentCreate): The assignment details.

    Returns:
        UserAssignmentUploadResponse: The result of the upload.
    """
    result = await upload_assignment(assignment, current_user)
    return result


@router.get("/admins", response_model=AdminListResponse, summary="Get all admins")
async def get_admins_endpoint(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Retrieves a list of all admins.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        AdminListResponse: A list of all admins.
    """
    result = await get_admins()
    return result

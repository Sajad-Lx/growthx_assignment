from datetime import timedelta
from app.auth import create_access_token, get_password_hash, verify_password
from app.database import users_collection, assignments_collection
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserCreateResponse, UserLogin, UserLoginResponse, UserAssignmentUploadResponse, AdminListResponse
from app.schemas.assignment_schema import AssignmentUpdate, AssignmentListResponse
from fastapi import HTTPException, status
from bson import ObjectId, errors
from fastapi import HTTPException
from pymongo.errors import PyMongoError


async def register_admin(admin: UserCreate) -> UserCreateResponse:
    """
    Registers a new admin user.

    Args:
        admin (UserCreate): The admin data for registration.

    Returns:
        UserCreateResponse: A response containing the admin ID and a success message.

    Raises:
        HTTPException: If the username is already taken or a database error occurs.
    """
    try:
        # Check if the username already exists
        existing_admin = await users_collection.find_one({"username": admin.username})
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        # Create a new admin document
        new_admin = {
            "username": admin.username,
            "password": get_password_hash(admin.password),
            "role": "admin"
        }
        result = await users_collection.insert_one(new_admin)
        return {"id": str(result.inserted_id), "message": "Admin registered successfully"}

    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred while registering admin") from e


async def login_admin(admin: UserLogin) -> UserLoginResponse:
    """
    Authenticates an admin and returns a JWT access token.

    Args:
        admin (UserLogin): The admin credentials for login.

    Returns:
        UserLoginResponse: A response containing the admin ID, username, and access token.

    Raises:
        HTTPException: If the credentials are invalid or a database error occurs.
    """
    try:
        # Find the admin by username
        found_admin = await users_collection.find_one({"username": admin.username, "role": "admin"})
        # Hashed password check
        if not found_admin or not verify_password(admin.password, found_admin["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        access_token = create_access_token(
            data={"sub": found_admin["username"]}, expires_delta=timedelta(minutes=30))

        return {"id": str(found_admin["_id"]), "username": found_admin["username"], "access_token": access_token, "token_type": "bearer"}

    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred while logging in") from e


async def get_assignments_for_admin(current_user: User, admin: str = None) -> AssignmentListResponse:
    """
    Retrieves assignments tagged to a specific admin.

    Args:
        admin_id (str): The ID of the admin.

    Returns:
        AssignmentListResponse: A list of assignments for the admin.

    Raises:
        HTTPException: If the admin ID is invalid or a database error occurs.
    """
    try:
        # Find assignments tagged to this admin
        if not current_user["role"] == "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to admin")
        if admin:
            assignments = await assignments_collection.find({"admin": admin}).to_list(length=100)
        else:
            assignments = await assignments_collection.find({"admin_id": current_user["_id"]}).to_list(length=100)
        return {"assignments": [{"id": str(a["_id"]), "userId": a["userId"], "task": a["task"], "admin": a["admin"], "status": a["status"], "timestamp": a["timestamp"]} for a in assignments]}

    except errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Admin ID.")

    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred while getting assignments") from e


async def update_assignment_status(assignment: AssignmentUpdate, current_user: User) -> dict:
    """
    Updates the status of an assignment (accept/reject).

    Args:
        assignment (AssignmentUpdate): The assignment data including the new status.

    Returns:
        dict: A success message indicating the assignment status was updated.

    Raises:
        HTTPException: If the user is not an admin, assignment ID is invalid, assignment is not found, or a database error occurs.
    """
    try:
        # Update the assignment status (accept/reject)
        if not current_user["role"] == "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to accept assignments.")
        object_id = ObjectId(assignment.assignment_id)

        result = await assignments_collection.update_one(
            {"_id": ObjectId(object_id)},
            {"$set": {"status": assignment.status}}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found.")

        return {"message": "Assignment status updated successfully"}

    except errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid assignment ID.")

    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred while updating assignment status") from e

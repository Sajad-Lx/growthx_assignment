from pydantic import BaseModel
from app.models.assignment import Assignment
from app.models.user import User


class AssignmentCreate(BaseModel):
    userId: str
    task: str
    admin: str


class AssignmentUpdate(BaseModel):
    assignment_id: str
    status: str


class AssignmentUpdateResponse(BaseModel):
    message: str


class AssignmentListResponse(BaseModel):
    assignments: list[Assignment] | None

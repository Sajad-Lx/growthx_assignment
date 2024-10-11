from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserCreateResponse(BaseModel):
    id: str
    message: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    id: str
    username: str
    access_token: str
    token_type: str


class UserAssignmentUploadResponse(BaseModel):
    id: str
    message: str


class AdminResponse(BaseModel):
    id: str
    username: str


class AdminListResponse(BaseModel):
    admins: list[AdminResponse] | None

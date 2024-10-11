from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    id: Optional[str]
    username: str
    password: str
    is_active: bool = True
    role: str = Field(..., pattern="^(user|admin)$")

from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.token import Token
from app.routes import user_routes, admin_routes
from app.schemas.user_schema import UserLogin
from app.services.user_service import login_user

app = FastAPI(
    title="Assignment Submission Portal API",
    description="""
    This API allows users and admins to manage and submit assignments.
    
    **Users** can:
    - Register and log in
    - Upload assignments
    - View available admins
    
    **Admins** can:
    - Register and log in
    - View and manage assignments tagged to them
    - Accept or reject assignments
    """,
    version="1.0.0",
    contact={
        "name": "Abdus Salam",
        "email": "sajad.laskar1@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def root():
    return {"message": "Assignment Submission Portal API"}

# Endpoint for getting access_token using OAuth2
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    found_user = await login_user(UserLogin(username=form_data.username, password=form_data.password))
    return Token(access_token=found_user["access_token"], token_type=found_user["token_type"])


# Register routers
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])

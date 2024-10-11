from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_username: str
    mongo_password: str
    mongo_host: str = "mongodb"
    mongo_port: int = 27017
    mongo_db: str = "assignment_db"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_password: str
    database_username: str
    database_host: str
    database_name: str
    database_port: int

    class Config:
        env_file = ".env"


settings = Settings()

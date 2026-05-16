from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    db_url: str
    admin_id: int

    class Config:
        env_file = ".env"

settings = Settings()
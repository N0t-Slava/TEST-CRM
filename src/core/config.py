from pydantic.env_settings import BaseSettings

class Settings(BaseSettings):
    smtp_host: str
    smtp_user: str
    smtp_pass: str

    class Config:
        env_file = ".env"

settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_KEY: str
    APP_SECRET: str
    BASE_URL: str

    class Config:
        env_file='.env'
        env_file_encoding='utf-8'
        extra='ignore'
from pydantic import BaseSettings

class Settings(BaseSettings):
    DB.CONNECTION: str
    DB.HOST: str
    DB.PORT: int
    DB.USERNAME: str
    DB.PASSWORD: str
    DB.DATABASE: str

    class Config:
        env_file = 'api/.env'
        env_file_encoding = 'utf-8'
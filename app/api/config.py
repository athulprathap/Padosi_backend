from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_CONNECTION: str
    DB_HOST: str
    DB_PORT: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_DATABASE: str
    twilio_account_sid:str
    twilio_auth_token:str
    twilio_number:str
    aws_access_key_id: str
    aws_secret_key: str
    aws_s3_bucket_name: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
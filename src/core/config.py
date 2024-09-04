from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Image Augmentation API'
    app_description: str = 'Image Augmentation Backend Server'
    SECRET_KEY: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: str
    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str
    USER_TOKEN_LIFE_TIME: str
    API_PREFIX: str
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASSWORD: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_BUCKET: str

    class Config:
        env_file = '.env'


settings = Settings()

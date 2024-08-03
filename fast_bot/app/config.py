import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_DB: str
    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".env")
    )


settings = Settings()


def get_mongo_url():
    return f"mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}/{settings.MONGO_DB}"


def get_redis_url():
    return f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"

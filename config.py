from pydantic import BaseSettings


class Settings(BaseSettings):
    slack_app_token: str
    slack_bot_token: str

    class Config:
        env_file = '.env'


settings = Settings()

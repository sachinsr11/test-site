from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "test-site"
    debug: bool = True
    secret_key: str = ""  # loaded from env via BaseSettings if provided


settings = Settings()

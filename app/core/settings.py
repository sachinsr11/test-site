from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "test-site"
    debug: bool = True


settings = Settings()

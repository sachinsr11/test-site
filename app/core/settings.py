from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "test-site"
    debug: bool = True
    secret_key: str = "hardcoded-secret-please-change"


settings = Settings()

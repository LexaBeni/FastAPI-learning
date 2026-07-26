from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_path: str = ''
    database_url: str = ''
    api_key: str = ''
    secret_key: str = ""
    algorithm: str = ''
    access_token_expire_minutes: int = 1
    refresh_token_expire_days: int = 1
    admin_username: str = ''
    admin_email: str = ''
    admin_password: str = ''
    test_database_url: str = ''
    test_model_path: str = ''
    

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

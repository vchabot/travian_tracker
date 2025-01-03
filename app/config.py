from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Travian Tracker"
    database_url: str = ""
    travian_server_url: str = ""
    map_size: int = 200

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
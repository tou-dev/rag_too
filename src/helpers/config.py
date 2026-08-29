from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_TYPES:list
    FILE_DEFAULT_CHUNK_SIZE:int

    # Supabase Settings
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_BUCKET_NAME: str = "uploads"


    class config:
        env_file=".env"
def get_settings():
    return Settings()
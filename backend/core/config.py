from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str | None = None
    tavily_api_key: str | None = None
    pinecone_api_key: str | None = None
    pinecone_index: str | None = None
    pinecone_env: str | None = None
    database_url: str | None = None
    redis_url: str | None = None


settings = Settings()

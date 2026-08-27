from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    hf_token: str
    groq_api_key: str
    groq_model: str = 'openai/gpt-oss-120b'
    embedding_model: str = 'BAAI/bge-base-en-v1.5'

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
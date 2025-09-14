from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Banco de dados
    database_url: str = "sqlite:///./data/app.db"

    # Configuração de embeddings
    embedding_backend: str = "LOCAL"  # LOCAL ou OPENAI
    local_embedding_model: str = "BAAI/bge-base-en-v1.5"
    openai_api_key: str | None = None
    openai_embedding_model: str = "text-embedding-3-small"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"  # aceita variáveis extras no .env sem quebrar


settings = Settings()

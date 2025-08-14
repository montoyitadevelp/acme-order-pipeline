from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Postgres
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_PORT: int | None = None
    
    # Mongo
    MONGO_URI: str | None = None
    MONGO_INITDB_DATABASE: str = "ecommerce_orders"
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    # General
    APP_NAME: str | None = None
    FRONTEND_BASE_URL: str | None = None

    # Security
    BACKEND_CORS_ORIGIN: str | None = None



settings = Settings()

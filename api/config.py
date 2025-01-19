from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Albert AI settings
    ALBERT_AI_BASE_URL: str = "https://api.albert.ai"
    ALBERT_AI_API_KEY: str = ""
    
    # Application settings
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings() 
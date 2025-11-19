from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API
    API_TITLE: str = "AI Creative Studio"
    API_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Stable Diffusion
    SD_MODEL_ID: str = "runwayml/stable-diffusion-v1-5"
    SD_DEVICE: str = "cuda"  # ou "cpu"
    SD_DTYPE: str = "float16"  # ou "float32"
    
    # RL Agent
    RL_AGENT_PATH: str = "models/rl_agent.zip"
    RL_USE_AGENT: bool = True
    
    # Generation
    DEFAULT_GUIDANCE_SCALE: float = 7.5
    DEFAULT_NUM_STEPS: int = 50
    DEFAULT_WIDTH: int = 512
    DEFAULT_HEIGHT: int = 512
    
    # Paths
    OUTPUT_DIR: str = "outputs"
    MODELS_DIR: str = "models"
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/ai_creative_studio.db"
    
    class Config:
        env_file = ".env"

settings = Settings()


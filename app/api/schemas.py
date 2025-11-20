from pydantic import BaseModel
from typing import Optional, Dict
from app.utils.prompt_templates import UseCase

class GenerateRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    guidance_scale: Optional[float] = None  # None = auto selon use_case
    num_inference_steps: Optional[int] = None  # None = auto selon use_case
    width: Optional[int] = None  # None = auto selon use_case
    height: Optional[int] = None  # None = auto selon use_case
    seed: Optional[int] = None
    use_rl_optimization: bool = False
    use_case: Optional[str] = None  # "logo", "marketing", "game_assets", "artistic"
    style: Optional[str] = "general"  # Style spécifique du cas d'usage

class GenerateResponse(BaseModel):
    message: str
    prompt: str
    optimized_prompt: Optional[str] = None
    parameters: Dict
    score: Optional[float] = None
    image_path: Optional[str] = None

class OptimizationRequest(BaseModel):
    base_prompt: str
    n_iterations: int = 10

class OptimizationResponse(BaseModel):
    original_prompt: str
    optimized_prompt: str
    original_score: float
    optimized_score: float
    improvement: float
    best_params: Dict


class FeedbackRequest(BaseModel):
    """Schéma pour soumettre un feedback utilisateur"""
    generation_id: int
    score: float  # 0-1 (ou 0-10)
    comment: Optional[str] = None
    user_id: Optional[str] = None


class FeedbackResponse(BaseModel):
    """Réponse après soumission d'un feedback"""
    status: str
    feedback_id: int
    message: str


class StatsResponse(BaseModel):
    """Réponse pour les statistiques globales"""
    total_generations: int
    average_score: Optional[float]
    rl_agent_trained_steps: Optional[int] = None


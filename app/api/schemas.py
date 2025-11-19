from pydantic import BaseModel
from typing import Optional, Dict

class GenerateRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    guidance_scale: float = 7.5
    num_inference_steps: int = 50
    width: int = 512
    height: int = 512
    seed: Optional[int] = None
    use_rl_optimization: bool = False

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


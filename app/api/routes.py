from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
import time
from pathlib import Path
from sqlalchemy.orm import Session
from app.api.schemas import (
    GenerateRequest, GenerateResponse,
    OptimizationRequest, OptimizationResponse
)
from app.models.stable_diffusion import sd_generator
from app.models.aesthetic_scorer import aesthetic_scorer
from app.models.rl_agent import get_rl_optimizer
from app.utils.config import settings
from app.utils.helpers import get_output_path
from app.utils.prompt_templates import apply_prompt_template, get_available_use_cases, get_available_styles
from app.database.database import get_db
from app.database.repository import ImageRepository

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
async def generate_image(request: GenerateRequest, db: Session = Depends(get_db)):
    """
    Génère une image avec Stable Diffusion.
    
    Si use_case et style sont fournis, applique le template approprié.
    Si use_rl_optimization=True, l'agent RL optimise d'abord le prompt.
    """
    try:
        # Appliquer le template selon use_case et style
        template_prompt, template_negative_prompt, template_params = apply_prompt_template(
            base_prompt=request.prompt,
            use_case=request.use_case,
            style=request.style or "general"
        )
        
        # Utiliser les valeurs du template si non spécifiées dans la requête
        final_prompt = template_prompt
        final_negative_prompt = request.negative_prompt or template_negative_prompt
        final_guidance_scale = request.guidance_scale or template_params.get("guidance_scale", 7.5)
        final_num_steps = request.num_inference_steps or template_params.get("num_inference_steps", 50)
        final_width = request.width or template_params.get("width", 512)
        final_height = request.height or template_params.get("height", 512)
        
        optimized_prompt = None
        score = None
        
        # Optimisation RL du prompt (optionnel) - mettre de côté pour le moment
        # if request.use_rl_optimization:
        #     try:
        #         rl_optimizer = get_rl_optimizer()
        #         optimization_result = rl_optimizer.optimize_prompt(
        #             base_prompt=final_prompt,
        #             n_iterations=10
        #         )
        #         optimized_prompt = optimization_result['optimized_prompt']
        #         final_prompt = optimized_prompt
        #     except Exception as e:
        #         # Si l'optimisation RL échoue, continuer sans optimisation
        #         print(f"WARNING: Erreur lors de l'optimisation RL: {e}")
        #         optimized_prompt = None
        
        # Génération de l'image
        start_time = time.time()
        image = sd_generator.generate(
            prompt=final_prompt,
            negative_prompt=final_negative_prompt,
            guidance_scale=final_guidance_scale,
            num_inference_steps=final_num_steps,
            width=final_width,
            height=final_height,
            seed=request.seed
        )
        
        # Sauvegarder l'image
        output_dir = get_output_path("portfolio")
        timestamp = int(time.time())
        filename = f"generated_{timestamp}.png"
        filepath = output_dir / filename
        image.save(str(filepath))
        
        # Calculer score
        score = aesthetic_scorer.score(image)
        
        # Sauvegarder dans la base de données
        generation_time = time.time() - start_time
        try:
            ImageRepository.create(
                db=db,
                prompt=request.prompt,  # Prompt original de l'utilisateur
                image_path=str(filepath),
                negative_prompt=final_negative_prompt,
                optimized_prompt=final_prompt,  # Prompt final utilisé (template ou optimisé)
                guidance_scale=final_guidance_scale,
                num_inference_steps=final_num_steps,
                width=final_width,
                height=final_height,
                seed=request.seed,
                score=score,
                generation_time=generation_time,
                use_rl_optimization=request.use_rl_optimization,
            )
        except Exception as e:
            print(f"WARNING: Erreur lors de la sauvegarde en base de donnees: {e}")
        
        return GenerateResponse(
            message="Image generated successfully",
            prompt=request.prompt,
            optimized_prompt=final_prompt,  # Prompt final utilisé
            parameters={
                "guidance_scale": final_guidance_scale,
                "num_steps": final_num_steps,
                "width": final_width,
                "height": final_height,
                "seed": request.seed
            },
            score=score,
            image_path=str(filepath)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize", response_model=OptimizationResponse)
async def optimize_prompt(request: OptimizationRequest):
    """
    Optimise un prompt via l'agent RL.
    """
    try:
        rl_optimizer = get_rl_optimizer()
        result = rl_optimizer.optimize_prompt(
            base_prompt=request.base_prompt,
            n_iterations=request.n_iterations
        )
        
        return OptimizationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AI Creative Studio"}

@router.get("/history")
async def get_history(
    skip: int = 0,
    limit: int = 50,
    order_by: str = "created_at",
    order_desc: bool = True,
    db: Session = Depends(get_db)
):
    """Récupère l'historique des images générées"""
    try:
        images = ImageRepository.get_all(
            db=db,
            skip=skip,
            limit=limit,
            order_by=order_by,
            order_desc=order_desc
        )
        return {
            "total": len(images),
            "skip": skip,
            "limit": limit,
            "images": [img.to_dict() for img in images]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images/{image_id}")
async def get_image(image_id: int, db: Session = Depends(get_db)):
    """Récupère les métadonnées d'une image par son ID"""
    try:
        image = ImageRepository.get_by_id(db=db, image_id=image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_images(
    query: str,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Recherche des images par mot-clé dans le prompt"""
    try:
        images = ImageRepository.search_by_prompt(
            db=db,
            prompt_search=query,
            skip=skip,
            limit=limit
        )
        return {
            "query": query,
            "total": len(images),
            "skip": skip,
            "limit": limit,
            "images": [img.to_dict() for img in images]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/best")
async def get_best_images(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Récupère les meilleures images par score"""
    try:
        images = ImageRepository.get_best_scored(db=db, limit=limit)
        return {
            "limit": limit,
            "images": [img.to_dict() for img in images]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics")
async def get_statistics(db: Session = Depends(get_db)):
    """Récupère les statistiques globales"""
    try:
        stats = ImageRepository.get_statistics(db=db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/images/{image_id}")
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    """Supprime une image de la base de données (et son fichier)"""
    try:
        image = ImageRepository.get_by_id(db=db, image_id=image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Supprimer le fichier
        image_path = Path(image.image_path)
        if image_path.exists():
            image_path.unlink()
        
        # Supprimer de la base de données
        ImageRepository.delete(db=db, image_id=image_id)
        
        return {"message": "Image deleted successfully", "image_id": image_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/use-cases")
async def get_use_cases():
    """Retourne la liste des cas d'usage disponibles et leurs styles."""
    use_cases = get_available_use_cases()
    result = {}
    for uc in use_cases:
        if uc != "general":
            result[uc] = {
                "styles": get_available_styles(uc),
                "description": {
                    "logo": "Design de logos automatique : Génère des variations de logos et apprend quels styles fonctionnent le mieux",
                    "marketing": "Créateur de visuels marketing : Produit des bannières/posts et optimise selon l'engagement",
                    "game_assets": "Générateur de game assets : Crée des textures/sprites et apprend des choix du game designer",
                    "artistic": "Assistant artistique : Génère des concepts visuels et s'adapte au style préféré de l'artiste"
                }.get(uc, "")
            }
    return {
        "use_cases": result,
        "general": {
            "styles": ["general"],
            "description": "Génération générale sans template spécifique"
        }
    }

@router.get("/")
async def root():
    """Root endpoint avec instructions."""
    return {
        "message": "Welcome to AI Creative Studio API",
        "docs": "/docs",
        "endpoints": {
            "/generate": "Generate images with Stable Diffusion",
            "/optimize": "Optimize prompts using RL agent (disabled for now)",
            "/use-cases": "Get available use cases and styles",
            "/history": "Get generation history",
            "/images/{id}": "Get image metadata by ID",
            "/search": "Search images by prompt",
            "/best": "Get best scored images",
            "/statistics": "Get global statistics",
            "/health": "Health check"
        }
    }


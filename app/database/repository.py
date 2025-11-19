"""
Repository pour les opérations CRUD sur la base de données
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import datetime
from app.database.models import GeneratedImage

class ImageRepository:
    """Repository pour gérer les images générées"""
    
    @staticmethod
    def create(
        db: Session,
        prompt: str,
        image_path: str,
        negative_prompt: Optional[str] = None,
        optimized_prompt: Optional[str] = None,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 50,
        width: int = 512,
        height: int = 512,
        seed: Optional[int] = None,
        score: Optional[float] = None,
        generation_time: Optional[float] = None,
        use_rl_optimization: bool = False,
    ) -> GeneratedImage:
        """Crée une nouvelle entrée d'image générée"""
        db_image = GeneratedImage(
            prompt=prompt,
            negative_prompt=negative_prompt,
            optimized_prompt=optimized_prompt,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            width=width,
            height=height,
            seed=seed,
            score=score,
            image_path=image_path,
            generation_time=generation_time,
            use_rl_optimization=use_rl_optimization,
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image
    
    @staticmethod
    def get_by_id(db: Session, image_id: int) -> Optional[GeneratedImage]:
        """Récupère une image par son ID"""
        return db.query(GeneratedImage).filter(GeneratedImage.id == image_id).first()
    
    @staticmethod
    def get_by_path(db: Session, image_path: str) -> Optional[GeneratedImage]:
        """Récupère une image par son chemin"""
        return db.query(GeneratedImage).filter(GeneratedImage.image_path == image_path).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "created_at",
        order_desc: bool = True
    ) -> List[GeneratedImage]:
        """Récupère toutes les images avec pagination"""
        query = db.query(GeneratedImage)
        
        # Trier
        if order_by == "created_at":
            order_column = GeneratedImage.created_at
        elif order_by == "score":
            order_column = GeneratedImage.score
        else:
            order_column = GeneratedImage.created_at
        
        if order_desc:
            query = query.order_by(desc(order_column))
        else:
            query = query.order_by(order_column)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def search_by_prompt(
        db: Session,
        prompt_search: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[GeneratedImage]:
        """Recherche les images par mot-clé dans le prompt"""
        return db.query(GeneratedImage).filter(
            GeneratedImage.prompt.contains(prompt_search)
        ).order_by(desc(GeneratedImage.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_best_scored(
        db: Session,
        limit: int = 10
    ) -> List[GeneratedImage]:
        """Récupère les meilleures images par score"""
        return db.query(GeneratedImage).filter(
            GeneratedImage.score.isnot(None)
        ).order_by(desc(GeneratedImage.score)).limit(limit).all()
    
    @staticmethod
    def get_statistics(db: Session) -> dict:
        """Récupère les statistiques globales"""
        total = db.query(func.count(GeneratedImage.id)).scalar()
        avg_score = db.query(func.avg(GeneratedImage.score)).scalar()
        max_score = db.query(func.max(GeneratedImage.score)).scalar()
        min_score = db.query(func.min(GeneratedImage.score)).scalar()
        
        # Nombre avec RL
        with_rl = db.query(func.count(GeneratedImage.id)).filter(
            GeneratedImage.use_rl_optimization == True
        ).scalar()
        
        return {
            "total_images": total or 0,
            "average_score": round(avg_score, 2) if avg_score else None,
            "max_score": max_score,
            "min_score": min_score,
            "with_rl_optimization": with_rl or 0,
            "without_rl_optimization": (total or 0) - (with_rl or 0),
        }
    
    @staticmethod
    def delete(db: Session, image_id: int) -> bool:
        """Supprime une image de la base de données"""
        db_image = db.query(GeneratedImage).filter(GeneratedImage.id == image_id).first()
        if db_image:
            db.delete(db_image)
            db.commit()
            return True
        return False


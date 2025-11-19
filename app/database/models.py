"""
Modèles SQLAlchemy pour la base de données SQLite
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class GeneratedImage(Base):
    """
    Modèle pour stocker les métadonnées des images générées
    """
    __tablename__ = "generated_images"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Prompts
    prompt = Column(Text, nullable=False, index=True)
    negative_prompt = Column(Text, nullable=True)
    optimized_prompt = Column(Text, nullable=True)
    
    # Paramètres de génération
    guidance_scale = Column(Float, nullable=False, default=7.5)
    num_inference_steps = Column(Integer, nullable=False, default=50)
    width = Column(Integer, nullable=False, default=512)
    height = Column(Integer, nullable=False, default=512)
    seed = Column(Integer, nullable=True)
    
    # Résultats
    score = Column(Float, nullable=True, index=True)
    image_path = Column(String(500), nullable=False, unique=True, index=True)
    
    # Métadonnées
    generation_time = Column(Float, nullable=True)  # Temps de génération en secondes
    use_rl_optimization = Column(Boolean, default=False, nullable=False)
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "optimized_prompt": self.optimized_prompt,
            "guidance_scale": self.guidance_scale,
            "num_inference_steps": self.num_inference_steps,
            "width": self.width,
            "height": self.height,
            "seed": self.seed,
            "score": self.score,
            "image_path": self.image_path,
            "generation_time": self.generation_time,
            "use_rl_optimization": self.use_rl_optimization,
        }


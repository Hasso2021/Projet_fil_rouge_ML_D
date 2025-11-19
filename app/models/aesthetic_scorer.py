import torch
from PIL import Image
import numpy as np

class AestheticScorer:
    """
    Score la qualité esthétique d'une image.
    Utilise un modèle simplifié pour le starter (à améliorer avec CLIP).
    """
    
    def score(self, image: Image.Image) -> float:
        """
        Retourne un score esthétique entre 0 et 10.
        
        Args:
            image: Image PIL à scorer
        
        Returns:
            float: Score esthétique
        """
        # TODO: Implémenter un vrai aesthetic predictor
        # Pour le starter, score basique sur la variance des couleurs
        
        img_array = np.array(image)
        
        # Métriques simples
        color_variance = np.var(img_array)
        brightness = np.mean(img_array)
        
        # Score combiné (très simplifié)
        score = (color_variance / 10000) + (brightness / 100)
        score = np.clip(score, 0, 10)
        
        return float(score)

# Instance globale
aesthetic_scorer = AestheticScorer()


import torch
from PIL import Image
import numpy as np
from typing import Tuple

class AestheticScorer:
    """
    Score la qualité esthétique d'une image.
    Utilise plusieurs métriques visuelles pour évaluer la qualité.
    """
    
    def _calculate_metrics(self, img_array: np.ndarray) -> Tuple[float, float, float, float]:
        """Calcule plusieurs métriques visuelles."""
        # Variance des couleurs (diversité)
        color_variance = np.var(img_array)
        
        # Luminosité moyenne
        brightness = np.mean(img_array)
        
        # Contraste (différence entre max et min)
        contrast = np.std(img_array)
        
        # Saturation (différence entre canaux RGB)
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
            saturation = np.mean([np.std(r), np.std(g), np.std(b)])
        else:
            saturation = 0
        
        return color_variance, brightness, contrast, saturation
    
    def score(self, image: Image.Image) -> float:
        """
        Retourne un score esthétique entre 0 et 10.
        
        Args:
            image: Image PIL à scorer
        
        Returns:
            float: Score esthétique (0-10)
        """
        img_array = np.array(image, dtype=np.float32)
        
        # Calculer les métriques
        color_variance, brightness, contrast, saturation = self._calculate_metrics(img_array)
        
        # Normaliser les métriques
        # Variance de couleurs: score max si variance entre 1000-5000
        variance_score = min(color_variance / 3000.0, 1.0) * 2.5
        
        # Luminosité: score max si brightness entre 100-180 (éviter trop sombre ou trop clair)
        brightness_normalized = abs(brightness - 140) / 140.0
        brightness_score = (1.0 - min(brightness_normalized, 1.0)) * 2.5
        
        # Contraste: score max si contraste élevé (> 50)
        contrast_score = min(contrast / 80.0, 1.0) * 2.5
        
        # Saturation: score max si saturation élevée (> 30)
        saturation_score = min(saturation / 60.0, 1.0) * 2.5
        
        # Score final (moyenne pondérée)
        final_score = variance_score + brightness_score + contrast_score + saturation_score
        
        # Clipper entre 0 et 10, avec un bias vers le milieu (4-8)
        final_score = np.clip(final_score + 2.0, 0, 10)  # Ajouter un bias de +2 pour éviter les scores trop bas
        
        return float(final_score)

# Instance globale
aesthetic_scorer = AestheticScorer()


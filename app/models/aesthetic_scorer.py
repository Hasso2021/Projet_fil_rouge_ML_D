"""
Évaluateur de qualité esthétique des images générées.

Ce module implémente un système de scoring basé sur 4 métriques visuelles:
- Variance de couleurs (diversité)
- Luminosité (équilibre clair/sombre)
- Contraste (netteté)
- Saturation (richesse des couleurs)

Score final: 0-10 (4-8 = bon, 8-10 = excellent)
"""
import torch
from PIL import Image
import numpy as np
from typing import Tuple

class AestheticScorer:
    """
    Évalue la qualité esthétique d'une image sur une échelle de 0 à 10.
    
    Approche:
    - Analyse de 4 métriques visuelles quantitatives
    - Normalisation et pondération de chaque métrique
    - Agrégation en un score unique
    
    Avantages:
    - Rapide: ~10ms par image
    - Pas de modèle ML externe requis
    - Corrélation raisonnable avec perception humaine
    
    Limitations:
    - Ne capture pas la composition artistique
    - Favorise les images saturées et contrastées
    - À terme: remplacer par CLIP-based aesthetic predictor
    """
    
    def _calculate_metrics(self, img_array: np.ndarray) -> Tuple[float, float, float, float]:
        """
        Calcule les 4 métriques visuelles de base.
        
        Args:
            img_array: Image sous forme de numpy array (H, W, 3) en RGB
        
        Returns:
            Tuple de 4 floats: (variance_couleurs, luminosité, contraste, saturation)
        """
        # ========================================
        # MÉTRIQUE 1: VARIANCE DES COULEURS
        # ========================================
        # Mesure la diversité des couleurs dans l'image
        # - Faible variance: Image plate, monotone (ex: ciel uni)
        # - Forte variance: Image riche, détaillée (ex: paysage complexe)
        color_variance = np.var(img_array)
        
        # ========================================
        # MÉTRIQUE 2: LUMINOSITÉ MOYENNE
        # ========================================
        # Mesure si l'image est trop sombre ou trop claire
        # - Valeurs: 0-255 (0=noir, 255=blanc)
        # - Optimal: 100-180 (ni trop sombre ni trop clair)
        brightness = np.mean(img_array)
        
        # ========================================
        # MÉTRIQUE 3: CONTRASTE
        # ========================================
        # Mesure la différence entre zones claires et sombres
        # - Écart-type: Plus élevé = Plus de contraste
        # - Fort contraste = Image nette et dynamique
        # - Faible contraste = Image terne et plate
        contrast = np.std(img_array)
        
        # ========================================
        # MÉTRIQUE 4: SATURATION DES COULEURS
        # ========================================
        # Mesure la richesse/vivacité des couleurs
        # - Analyse la variation dans chaque canal RGB
        # - Haute saturation = Couleurs vives et riches
        # - Faible saturation = Image grisâtre/délavée
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
            # Moyenne de l'écart-type de chaque canal RGB
            saturation = np.mean([np.std(r), np.std(g), np.std(b)])
        else:
            # Image en niveaux de gris: saturation nulle
            saturation = 0
        
        return color_variance, brightness, contrast, saturation
    
    def score(self, image: Image.Image) -> float:
        """
        Calcule et retourne un score esthétique entre 0 et 10.
        
        Processus:
        1. Conversion de l'image en array numpy
        2. Calcul des 4 métriques visuelles
        3. Normalisation de chaque métrique sur une échelle 0-2.5
        4. Agrégation des scores (max = 10 points)
        5. Application d'un bias pour éviter scores trop bas
        
        Distribution des scores attendus:
        - 0-3: Très mauvaise qualité (rare)
        - 4-5: Qualité acceptable
        - 6-7: Bonne qualité (majorité des images)
        - 8-9: Excellente qualité
        - 9-10: Qualité exceptionnelle (rare)
        
        Args:
            image: Image PIL à scorer (format RGB)
        
        Returns:
            float: Score esthétique entre 0 et 10
        
        Exemple:
            >>> scorer = AestheticScorer()
            >>> image = Image.open("photo.jpg")
            >>> score = scorer.score(image)
            >>> print(f"Score: {score:.2f}/10")  # Ex: "Score: 7.35/10"
        """
        # Conversion en array numpy pour calculs vectorisés
        img_array = np.array(image, dtype=np.float32)
        
        # ========================================
        # ÉTAPE 1: CALCUL DES MÉTRIQUES BRUTES
        # ========================================
        color_variance, brightness, contrast, saturation = self._calculate_metrics(img_array)
        
        # ========================================
        # ÉTAPE 2: NORMALISATION DES MÉTRIQUES
        # ========================================
        # Chaque métrique contribue pour max 2.5 points (total = 10 points)
        
        # Score de variance: Optimal entre 1000-5000
        # Plus la variance est proche de 3000, meilleur est le score
        variance_score = min(color_variance / 3000.0, 1.0) * 2.5
        
        # Score de luminosité: Optimal autour de 140
        # Pénalise les images trop sombres (<100) ou trop claires (>180)
        brightness_normalized = abs(brightness - 140) / 140.0
        brightness_score = (1.0 - min(brightness_normalized, 1.0)) * 2.5
        
        # Score de contraste: Plus c'est élevé, mieux c'est
        # Optimal > 80 (contraste fort = image nette)
        contrast_score = min(contrast / 80.0, 1.0) * 2.5
        
        # Score de saturation: Plus c'est élevé, mieux c'est
        # Optimal > 60 (couleurs vives et riches)
        saturation_score = min(saturation / 60.0, 1.0) * 2.5
        
        # ========================================
        # ÉTAPE 3: AGRÉGATION ET FINALISATION
        # ========================================
        # Somme des 4 scores (max théorique = 10.0)
        final_score = variance_score + brightness_score + contrast_score + saturation_score
        
        # Bias de +2.0 pour éviter les scores trop bas
        # Raison: Les images générées par SD sont rarement "mauvaises"
        # Cela centre la distribution sur 4-8 plutôt que 2-6
        final_score = np.clip(final_score + 2.0, 0, 10)
        
        return float(final_score)

# Instance globale
aesthetic_scorer = AestheticScorer()


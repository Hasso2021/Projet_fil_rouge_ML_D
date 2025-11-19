"""
Tests pour les modèles.
"""
import pytest
import numpy as np
from PIL import Image
from app.models.aesthetic_scorer import aesthetic_scorer

def test_aesthetic_scorer():
    """Test du scorer esthétique."""
    # Créer une image de test
    test_image = Image.new('RGB', (512, 512), color=(100, 150, 200))
    
    # Tester le scoring
    score = aesthetic_scorer.score(test_image)
    
    assert isinstance(score, float)
    assert 0 <= score <= 10


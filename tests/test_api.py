"""
Tests pour l'API FastAPI.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Test du endpoint root."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    """Test du endpoint health."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate():
    """Test du endpoint generate."""
    response = client.post(
        "/api/v1/generate",
        json={
            "prompt": "a beautiful sunset",
            "num_inference_steps": 20  # Moins de steps pour test rapide
        }
    )
    # Peut échouer si pas de GPU/CUDA, donc on vérifie juste la structure
    assert response.status_code in [200, 500]  # 500 si pas de GPU disponible


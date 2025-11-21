"""
Configuration centralisée de l'application AI Creative Studio.
Utilise Pydantic Settings pour gérer les variables d'environnement.
"""
import os
import torch
from pydantic_settings import BaseSettings

# ============================================
# AUTO-DÉTECTION DE L'ENVIRONNEMENT
# ============================================
# Détecter si on est sur Hugging Face Spaces
IS_HUGGINGFACE_SPACE = os.getenv("SPACE_ID") is not None

# Détecter si GPU disponible
HAS_GPU = torch.cuda.is_available()

# Choix automatique du device et dtype optimal
AUTO_DEVICE = "cuda" if HAS_GPU else "cpu"
AUTO_DTYPE = "float16" if HAS_GPU else "float32"

# Adapter les steps par défaut selon le device
# CPU : Steps réduits pour génération plus rapide
# GPU : Steps plus élevés pour meilleure qualité
AUTO_DEFAULT_STEPS = 25 if not HAS_GPU else 50

print(f"[Config] Environnement detecte: {'Hugging Face Spaces' if IS_HUGGINGFACE_SPACE else 'Local'}")
print(f"[Config] Device: {AUTO_DEVICE} (GPU disponible: {HAS_GPU})")
print(f"[Config] Dtype: {AUTO_DTYPE}")
print(f"[Config] Steps par defaut: {AUTO_DEFAULT_STEPS}")

class Settings(BaseSettings):
    """
    Classe de configuration principale de l'application.
    
    Permet de configurer tous les paramètres via:
    - Variables d'environnement
    - Fichier .env
    - Valeurs par défaut
    """
    
    # ============================================
    # CONFIGURATION API (FastAPI)
    # ============================================
    API_TITLE: str = "AI Creative Studio"
    API_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"  # Accessible depuis toutes les interfaces réseau
    API_PORT: int = 8000       # Port par défaut de l'API REST
    
    # ============================================
    # STABLE DIFFUSION - Modèle de génération d'images
    # ============================================
    # DreamShaper-8: Modèle spécialisé pour l'art créatif
    # Avantages: Plus rapide et meilleure qualité que SD 1.5
    SD_MODEL_ID: str = "Lykon/dreamshaper-8"
    
    # Device: "cuda" pour GPU, "cpu" pour CPU
    # GPU recommandé pour performance (10-20x plus rapide)
    # AUTO-DÉTECTÉ: Utilise GPU si disponible, sinon CPU
    SD_DEVICE: str = AUTO_DEVICE
    
    # Précision: "float16" pour GPU (plus rapide), "float32" pour CPU (plus stable)
    # AUTO-DÉTECTÉ: float16 sur GPU, float32 sur CPU
    SD_DTYPE: str = AUTO_DTYPE
    
    # ============================================
    # RL AGENT - Optimisation des prompts (optionnel)
    # ============================================
    # Chemin vers le modèle PPO entraîné
    RL_AGENT_PATH: str = "models/rl_agent.zip"
    
    # Activer/désactiver l'agent RL
    # Note: Peut être désactivé si le modèle n'est pas disponible
    RL_USE_AGENT: bool = True
    
    # ============================================
    # PARAMÈTRES DE GÉNÉRATION PAR DÉFAUT
    # ============================================
    # Guidance Scale: Force d'adhésion au prompt (7-9 optimal pour DreamShaper)
    DEFAULT_GUIDANCE_SCALE: float = 7.5
    
    # Nombre de steps: 20-50 steps suffisent avec DreamShaper-8
    # AUTO-ADAPTÉ: 25 steps sur CPU (plus rapide), 50 sur GPU (meilleure qualité)
    DEFAULT_NUM_STEPS: int = AUTO_DEFAULT_STEPS
    
    # Dimensions des images générées (512x512 = standard SD 1.5)
    DEFAULT_WIDTH: int = 512
    DEFAULT_HEIGHT: int = 512
    
    # ============================================
    # CHEMINS DE FICHIERS
    # ============================================
    OUTPUT_DIR: str = "outputs"      # Dossier pour les images générées
    MODELS_DIR: str = "models"       # Dossier pour les modèles RL
    
    # ============================================
    # BASE DE DONNÉES
    # ============================================
    # SQLite pour stocker:
    # - Métadonnées des images générées
    # - Historique des générations
    # - Feedbacks utilisateurs
    DATABASE_URL: str = "sqlite:///./data/ai_creative_studio.db"
    
    # Configuration Pydantic pour charger depuis .env
    model_config = {
        "env_file": ".env"  # Fichier .env optionnel pour override
    }

# Instance globale de configuration accessible dans toute l'application
settings = Settings()


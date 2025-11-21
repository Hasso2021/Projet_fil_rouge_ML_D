"""
AI Creative Studio - Application Gradio pour Hugging Face Spaces
Point d'entrée principal pour le déploiement sur HF Spaces
"""
import os
import torch
from app.gradio_ui import demo
from app.database.database import init_db

# Afficher les informations de l'environnement
print("="*60)
print("AI CREATIVE STUDIO - Démarrage")
print("="*60)
print(f"Environnement: {'Hugging Face Spaces' if os.getenv('SPACE_ID') else 'Local'}")
print(f"Device disponible: {'GPU (CUDA)' if torch.cuda.is_available() else 'CPU'}")
print(f"PyTorch version: {torch.__version__}")

if os.getenv('SPACE_ID'):
    print(f"Space ID: {os.getenv('SPACE_ID')}")
    print(f"Space Author: {os.getenv('SPACE_AUTHOR_NAME', 'N/A')}")

print("="*60)

# Initialiser la base de données
print("\nInitialisation de la base de donnees...")
init_db()

# Lancer l'application Gradio
print("\nLancement de l'interface Gradio...")
if __name__ == "__main__":
    # Hugging Face Spaces configure automatiquement server_name et port
    # Pas besoin de les spécifier explicitement
    demo.launch(
        share=False,  # Pas besoin de share sur HF Spaces (déjà public)
        show_error=True,  # Afficher les erreurs dans l'interface
    )



"""
Script pour lancer l'interface Gradio
Usage: python run_gradio.py
"""
from app.gradio_ui import demo
from app.database.database import init_db

if __name__ == "__main__":
    # Initialiser la base de données
    init_db()
    
    print("🚀 Lancement de l'interface Gradio...")
    print("📡 L'interface sera accessible sur: http://localhost:7860")
    print("📊 Base de données SQLite initialisée")
    print("📚 Fermez avec Ctrl+C")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False  # Mettre à True pour créer un lien public (gradio.app)
    )


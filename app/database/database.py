"""
Configuration et gestion des sessions de la base de données SQLite.

RÔLE DE CE MODULE:
------------------
1. Initialisation de la connexion à SQLite
2. Création des tables au démarrage
3. Gestion des sessions DB (ouverture/fermeture)
4. Dependency injection pour FastAPI

ARCHITECTURE:
-------------
- Engine: Point d'entrée principal vers la base de données
- SessionLocal: Factory pour créer des sessions DB
- Session: Connexion active à la DB pour exécuter des requêtes

POURQUOI SQLITE ?
-----------------
✅ Simple: 1 seul fichier (data/ai_creative_studio.db)
✅ Sans serveur: Pas de PostgreSQL/MySQL à installer
✅ Portable: Facile à sauvegarder/partager
✅ Performant: Suffisant pour des milliers d'images
⚠️ Limite: Pas adapté pour production multi-utilisateurs intense
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.utils.config import settings
from app.database.models import Base
from pathlib import Path

# ============================================
# CRÉATION DU RÉPERTOIRE DATA
# ============================================
# S'assure que le dossier data/ existe avant de créer la DB
# Exemple: si DATABASE_URL = "sqlite:///./data/ai_creative_studio.db"
#          alors on crée le dossier "data/" s'il n'existe pas
db_path = Path(settings.DATABASE_URL.replace("sqlite:///./", ""))
db_path.parent.mkdir(parents=True, exist_ok=True)

# ============================================
# CRÉATION DE L'ENGINE SQLALCHEMY
# ============================================
# L'engine est le point d'entrée principal vers la base de données
# Il gère:
# - La connexion à SQLite
# - Le pool de connexions
# - La traduction SQL via l'ORM
engine = create_engine(
    settings.DATABASE_URL,  # Ex: "sqlite:///./data/ai_creative_studio.db"
    
    # check_same_thread=False: CRITIQUE pour SQLite avec FastAPI
    # Par défaut, SQLite n'autorise qu'un thread par connexion
    # FastAPI est multi-threadé, donc on désactive cette vérification
    connect_args={"check_same_thread": False},
    
    # echo=False: Ne pas afficher les requêtes SQL dans la console
    # Mettre True pour debugging (voir toutes les requêtes exécutées)
    echo=False
)

# ============================================
# CRÉATION DE LA SESSION FACTORY
# ============================================
# SessionLocal est une "factory" (pas une instance de session)
# Chaque appel à SessionLocal() crée une NOUVELLE session DB
# 
# Paramètres:
# - autocommit=False: Les transactions doivent être committées manuellement
# - autoflush=False: Ne pas flush automatiquement avant chaque query
# - bind=engine: Lier cette factory à notre engine SQLite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialise la base de données en créant toutes les tables.
    
    Processus:
    1. Lit les modèles définis dans models.py (GeneratedImage, UserFeedback)
    2. Génère automatiquement le SQL CREATE TABLE pour chaque modèle
    3. Exécute ces requêtes SQL sur la base de données
    4. Si les tables existent déjà, ne fait rien (idempotent)
    
    Cette fonction est appelée au démarrage de l'application:
    - Dans run_gradio.py (pour l'interface Gradio)
    - Dans app/main.py (pour l'API FastAPI)
    
    Exemple de SQL généré automatiquement:
        CREATE TABLE generated_images (
            id INTEGER PRIMARY KEY,
            created_at DATETIME NOT NULL,
            prompt TEXT NOT NULL,
            ...
        )
    """
    # create_all() génère et exécute les CREATE TABLE
    # C'est la "magie" de l'ORM SQLAlchemy
    Base.metadata.create_all(bind=engine)
    print(f"OK: Base de donnees initialisee : {settings.DATABASE_URL}")

def get_db() -> Session:
    """
    Generator qui fournit une session DB et garantit sa fermeture.
    
    PATTERN: Dependency Injection pour FastAPI
    
    Utilisation dans FastAPI:
        @app.get("/images/{image_id}")
        def get_image(image_id: int, db: Session = Depends(get_db)):
            image = ImageRepository.get_by_id(db, image_id)
            return image
    
    Fonctionnement:
    1. Crée une nouvelle session DB
    2. Yield (donne) la session à la fonction appelante
    3. Attend que la fonction se termine
    4. Ferme automatiquement la session (même en cas d'erreur)
    
    Avantages:
    - ✅ Gestion automatique des ressources
    - ✅ Pas de fuite de connexions (memory leak)
    - ✅ Gestion des erreurs (finally garantit la fermeture)
    - ✅ Une session par requête HTTP (isolation)
    
    Exemple de flux:
        Request → FastAPI → get_db() → Ouvre session
                                     → Exécute fonction
                                     → Ferme session automatiquement
    """
    # Créer une nouvelle session DB
    db = SessionLocal()
    
    try:
        # Yield la session à la fonction appelante
        # La fonction s'exécute ici (entre yield et finally)
        yield db
    finally:
        # Garantit la fermeture même si exception levée
        # Libère les ressources et connexions
        db.close()


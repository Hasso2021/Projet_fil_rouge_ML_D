"""
Configuration et session de la base de données SQLite
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.utils.config import settings
from app.database.models import Base
from pathlib import Path

# Créer le répertoire data s'il n'existe pas
db_path = Path(settings.DATABASE_URL.replace("sqlite:///./", ""))
db_path.parent.mkdir(parents=True, exist_ok=True)

# Créer l'engine SQLite
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Nécessaire pour SQLite avec FastAPI
    echo=False  # Mettre à True pour voir les requêtes SQL (debug)
)

# Créer la session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialise la base de données (crée les tables)"""
    Base.metadata.create_all(bind=engine)
    print(f"OK: Base de donnees initialisee : {settings.DATABASE_URL}")

def get_db() -> Session:
    """
    Dependency pour FastAPI qui retourne une session de base de données
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


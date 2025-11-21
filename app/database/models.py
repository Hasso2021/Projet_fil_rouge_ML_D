"""
Définition des modèles de données (tables) avec SQLAlchemy ORM.

QU'EST-CE QU'UN ORM ?
---------------------
ORM = Object-Relational Mapping
Permet de manipuler la base de données comme des objets Python au lieu de SQL brut.

Au lieu de:
    cursor.execute("SELECT * FROM generated_images WHERE id = ?", (1,))
    
On fait:
    image = db.query(GeneratedImage).filter(GeneratedImage.id == 1).first()

TABLES DÉFINIES:
----------------
1. GeneratedImage: Métadonnées de chaque image générée
2. UserFeedback: Retours utilisateurs sur les images

WORKFLOW:
---------
Python Class → SQLAlchemy → SQL → SQLite → Fichier .db

Exemple:
    class GeneratedImage(Base):      # Python
        id = Column(Integer)
        
    → CREATE TABLE generated_images  # SQL
      (id INTEGER PRIMARY KEY)
      
    → Enregistré dans ai_creative_studio.db  # SQLite
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

# Base class pour tous les modèles SQLAlchemy
# Tous nos modèles héritent de Base
Base = declarative_base()

class GeneratedImage(Base):
    """
    Table principale: Stocke toutes les métadonnées des images générées.
    
    OBJECTIFS:
    ----------
    1. Traçabilité: Retrouver comment chaque image a été créée
    2. Historique: Consulter toutes les générations passées
    3. Statistiques: Analyser performances (temps, scores, etc.)
    4. Reproductibilité: Régénérer une image identique (via seed)
    5. Apprentissage: Données pour améliorer le RL
    
    STRUCTURE:
    ----------
    - Informations de génération (prompt, paramètres)
    - Résultats (score, chemin fichier, temps)
    - Métadonnées (date, RL utilisé ou non)
    
    RELATION AVEC FICHIERS:
    -----------------------
    Cette table stocke les MÉTADONNÉES.
    Les images réelles (.png) sont dans outputs/portfolio/
    Le lien se fait via la colonne image_path.
    
    Exemple d'entrée:
        id: 42
        prompt: "a cat"
        image_path: "outputs/portfolio/generated_1732190561.png"
        score: 7.2
        generation_time: 58.3
        → L'image physique est stockée séparément
    """
    __tablename__ = "generated_images"  # Nom de la table SQL
    
    # ========================================
    # COLONNES D'IDENTIFICATION
    # ========================================
    
    # ID unique auto-incrémenté (1, 2, 3, ...)
    # primary_key=True: Clé primaire de la table
    # index=True: Index B-Tree pour recherches rapides par ID
    id = Column(Integer, primary_key=True, index=True)
    
    # Date/heure de création de l'entrée
    # default=lambda: datetime.now(timezone.utc): Timestamp UTC automatique à l'insertion
    # nullable=False: Obligatoire (pas de NULL)
    # index=True: Permet tri rapide par date (ex: images récentes)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    
    # ========================================
    # PROMPTS - Ce que l'utilisateur a demandé
    # ========================================
    
    # Prompt original de l'utilisateur (ex: "a cat")
    # Text: Peut contenir du texte long (vs String limité à 255 chars)
    # nullable=False: Obligatoire (on ne peut pas générer sans prompt)
    # index=True: Permet recherches par mot-clé dans les prompts
    prompt = Column(Text, nullable=False, index=True)
    
    # Prompt négatif: Ce qu'on veut éviter dans l'image
    # (ex: "ugly, blurry, low quality")
    # nullable=True: Optionnel (peut être NULL)
    negative_prompt = Column(Text, nullable=True)
    
    # Prompt optimisé par le RL (si l'optimisation RL a été utilisée)
    # Ex: "a cat" → "a cat, professional photography, detailed fur..."
    # nullable=True: NULL si RL non utilisé
    optimized_prompt = Column(Text, nullable=True)
    
    # ========================================
    # PARAMÈTRES DE GÉNÉRATION STABLE DIFFUSION
    # ========================================
    # Ces paramètres permettent de reproduire exactement la même image
    
    # Guidance Scale (CFG): Force d'adhésion au prompt
    # Valeurs typiques: 7-9 (optimal pour DreamShaper-8)
    # Plus élevé = plus fidèle au prompt, moins créatif
    guidance_scale = Column(Float, nullable=False, default=7.5)
    
    # Nombre d'étapes de débruitage (steps)
    # Plus de steps = meilleure qualité mais plus lent
    # DreamShaper-8: 20-50 steps suffisent
    num_inference_steps = Column(Integer, nullable=False, default=50)
    
    # Dimensions de l'image en pixels
    # 512x512: Standard SD 1.5
    # Doivent être multiples de 64 pour Stable Diffusion
    width = Column(Integer, nullable=False, default=512)
    height = Column(Integer, nullable=False, default=512)
    
    # Seed aléatoire pour reproductibilité
    # Même seed + même prompt = même image
    # NULL = seed aléatoire différent à chaque fois
    seed = Column(Integer, nullable=True)
    
    # ========================================
    # RÉSULTATS DE LA GÉNÉRATION
    # ========================================
    
    # Score esthétique automatique (0-10)
    # Calculé par AestheticScorer
    # index=True: Permet tri par score (meilleures images)
    # nullable=True: Peut être NULL si erreur de calcul
    score = Column(Float, nullable=True, index=True)
    
    # Chemin vers le fichier image physique
    # Ex: "outputs/portfolio/generated_1732190561.png"
    # unique=True: Chaque image a un chemin unique
    # index=True: Recherche rapide par chemin
    image_path = Column(String(500), nullable=False, unique=True, index=True)
    
    # ========================================
    # MÉTADONNÉES ADDITIONNELLES
    # ========================================
    
    # Temps de génération en secondes
    # Utile pour analyser les performances
    # Ex: 58.3 secondes sur CPU, 8.2 secondes sur GPU
    generation_time = Column(Float, nullable=True)
    
    # Indique si l'optimisation RL a été utilisée
    # True: Prompt optimisé par l'agent RL
    # False: Génération directe sans RL
    use_rl_optimization = Column(Boolean, default=False, nullable=False)
    
    def to_dict(self):
        """
        Convertit l'objet SQLAlchemy en dictionnaire Python standard.
        
        UTILITÉ:
        --------
        - Sérialisation JSON pour l'API REST
        - Export des données
        - Logging et debugging
        
        Transforme:
            <GeneratedImage id=42 prompt="a cat">
        
        En:
            {
                "id": 42,
                "prompt": "a cat",
                "score": 7.2,
                ...
            }
        
        Note: created_at.isoformat() convertit datetime en string ISO 8601
        Ex: datetime(2024, 11, 21, 10, 30) → "2024-11-21T10:30:00"
        """
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "optimized_prompt": self.optimized_prompt,
            "guidance_scale": self.guidance_scale,
            "num_inference_steps": self.num_inference_steps,
            "width": self.width,
            "height": self.height,
            "seed": self.seed,
            "score": self.score,
            "image_path": self.image_path,
            "generation_time": self.generation_time,
            "use_rl_optimization": self.use_rl_optimization,
        }


class UserFeedback(Base):
    """
    Table secondaire: Stocke les retours utilisateurs sur les images générées.
    
    OBJECTIFS:
    ----------
    1. Collecter le feedback humain sur la qualité des images
    2. Comparer score automatique vs perception humaine
    3. Identifier les meilleures générations selon les utilisateurs
    4. Données pour améliorer/réentraîner l'agent RL
    5. Tracking multi-utilisateurs (qui aime quoi)
    
    RELATION AVEC GeneratedImage:
    -----------------------------
    Relation 1-N (One-to-Many):
    - Une image peut avoir plusieurs feedbacks (de différents utilisateurs)
    - Un feedback concerne une seule image
    
    Lien via Foreign Key:
        UserFeedback.generation_id → GeneratedImage.id
    
    WORKFLOW TYPIQUE:
    -----------------
    1. Utilisateur génère une image (→ GeneratedImage créé)
    2. Utilisateur voit l'image et donne son avis
    3. Feedback enregistré (→ UserFeedback créé)
    4. Analyse: Comparer score auto vs feedback humain
    
    Exemple:
        Image #42: "a cat", score auto=7.2
        │
        ├─ Feedback User1: score=9.0, "Superbe !"
        ├─ Feedback User2: score=8.5, "Très réaliste"
        └─ Feedback User3: score=6.0, "Un peu flou"
        
        → Score moyen humain: 7.8 (proche du score auto 7.2)
    """
    __tablename__ = "user_feedbacks"  # Nom de la table SQL
    
    # ========================================
    # COLONNES D'IDENTIFICATION
    # ========================================
    
    # ID unique du feedback
    id = Column(Integer, primary_key=True, index=True)
    
    # Date/heure du feedback
    # Permet de suivre l'évolution des avis dans le temps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    
    # ========================================
    # RELATION AVEC L'IMAGE (FOREIGN KEY)
    # ========================================
    
    # ID de l'image concernée par ce feedback
    # Référence vers GeneratedImage.id (Foreign Key conceptuelle)
    # Note: SQLite ne force pas les FK par défaut, mais on l'utilise comme tel
    # index=True: Permet de récupérer rapidement tous les feedbacks d'une image
    # 
    # Requête typique: "Tous les feedbacks pour l'image #42"
    #   SELECT * FROM user_feedbacks WHERE generation_id = 42
    generation_id = Column(Integer, nullable=False, index=True)
    
    # ========================================
    # FEEDBACK UTILISATEUR
    # ========================================
    
    # Score donné par l'utilisateur
    # Échelle: 0-10 (aligné avec le score esthétique automatique)
    # Ex: 8.5 = "Très bonne image"
    # nullable=False: Obligatoire (pas de feedback sans note)
    score = Column(Float, nullable=False)
    
    # Commentaire textuel optionnel
    # Permet à l'utilisateur d'expliquer sa note
    # Ex: "Très réaliste mais manque de contraste"
    # nullable=True: Optionnel
    comment = Column(Text, nullable=True)
    
    # ========================================
    # TRACKING UTILISATEUR (OPTIONNEL)
    # ========================================
    
    # Identifiant de l'utilisateur qui donne le feedback
    # Permet de:
    # - Analyser les préférences par utilisateur
    # - Éviter les feedbacks multiples du même user
    # - Personnaliser l'expérience
    # 
    # Ex: "user_abc123" ou "email@example.com" ou session_id
    # nullable=True: Optionnel (feedback anonyme possible)
    # index=True: Recherches rapides par utilisateur
    user_id = Column(String(100), nullable=True, index=True)
    
    def to_dict(self):
        """
        Convertit le feedback en dictionnaire pour sérialisation JSON.
        
        Utilisé principalement dans l'API REST pour retourner les feedbacks.
        """
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "generation_id": self.generation_id,
            "score": self.score,
            "comment": self.comment,
            "user_id": self.user_id,
        }


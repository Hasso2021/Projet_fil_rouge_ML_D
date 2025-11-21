"""
Repository Pattern: Couche d'abstraction pour les opérations CRUD.

QU'EST-CE QU'UN REPOSITORY ?
-----------------------------
Un Repository est une couche qui:
1. Abstrait l'accès aux données
2. Encapsule la logique SQL/ORM
3. Fournit une API métier simple
4. Facilite les tests (mock facile)

PATTERN ARCHITECTURAL:
----------------------
Controller/Service → Repository → ORM → Database

Au lieu de:
    # Dans le controller
    db.query(GeneratedImage).filter(id==1).first()  # Logique DB mélangée
    
On fait:
    # Dans le controller
    ImageRepository.get_by_id(db, 1)  # API métier claire
    
    # Toute la logique DB est dans le Repository
    class ImageRepository:
        def get_by_id(db, id):
            return db.query(GeneratedImage).filter(id==id).first()

AVANTAGES:
----------
✅ Séparation des responsabilités
✅ Code réutilisable (API + Gradio utilisent le même Repository)
✅ Testabilité (mock du Repository, pas de la DB)
✅ Évolutivité (changer la DB n'affecte que le Repository)
✅ Maintenabilité (logique SQL centralisée)

REPOSITORIES DISPONIBLES:
-------------------------
- ImageRepository: CRUD pour les images générées
- FeedbackRepository: CRUD pour les feedbacks utilisateurs
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import datetime
from app.database.models import GeneratedImage, UserFeedback

class ImageRepository:
    """
    Repository pour gérer les images générées.
    
    Fournit une API haut-niveau pour toutes les opérations sur GeneratedImage:
    - CREATE: Enregistrer une nouvelle image
    - READ: Récupérer une/plusieurs images
    - UPDATE: (non implémenté, rarement nécessaire pour images)
    - DELETE: Supprimer une image
    - SEARCH: Rechercher par prompt
    - STATS: Statistiques globales
    
    Pattern: Méthodes statiques (@staticmethod)
    Pourquoi ? Pas besoin d'état interne, juste des utilitaires.
    """
    
    @staticmethod
    def create(
        db: Session,
        prompt: str,
        image_path: str,
        negative_prompt: Optional[str] = None,
        optimized_prompt: Optional[str] = None,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 50,
        width: int = 512,
        height: int = 512,
        seed: Optional[int] = None,
        score: Optional[float] = None,
        generation_time: Optional[float] = None,
        use_rl_optimization: bool = False,
    ) -> GeneratedImage:
        """
        Crée une nouvelle entrée d'image générée dans la base de données.
        
        OPÉRATION: CREATE (du CRUD)
        
        Processus:
        1. Crée un objet GeneratedImage avec tous les paramètres
        2. Ajoute à la session DB (pas encore en DB)
        3. Commit: Enregistre réellement en DB
        4. Refresh: Récupère l'ID auto-généré depuis la DB
        5. Retourne l'objet complet avec son ID
        
        Exemple d'utilisation:
            db = SessionLocal()
            image = ImageRepository.create(
                db=db,
                prompt="a cat",
                image_path="outputs/portfolio/generated_123.png",
                guidance_scale=7.5,
                num_inference_steps=35,
                score=7.2,
                generation_time=58.3
            )
            print(f"Image créée avec ID: {image.id}")
            db.close()
        
        Args:
            db: Session de base de données active
            prompt: Prompt original de l'utilisateur
            image_path: Chemin vers le fichier image
            [... tous les autres paramètres de génération ...]
        
        Returns:
            GeneratedImage: L'objet créé avec son ID assigné
        """
        # Créer l'objet ORM
        db_image = GeneratedImage(
            prompt=prompt,
            negative_prompt=negative_prompt,
            optimized_prompt=optimized_prompt,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            width=width,
            height=height,
            seed=seed,
            score=score,
            image_path=image_path,
            generation_time=generation_time,
            use_rl_optimization=use_rl_optimization,
        )
        
        # Ajouter à la session (staging area)
        db.add(db_image)
        
        # Commit: Exécute INSERT INTO generated_images (...)
        db.commit()
        
        # Refresh: Récupère les valeurs auto-générées (id, created_at)
        db.refresh(db_image)
        
        return db_image
    
    @staticmethod
    def get_by_id(db: Session, image_id: int) -> Optional[GeneratedImage]:
        """Récupère une image par son ID"""
        return db.query(GeneratedImage).filter(GeneratedImage.id == image_id).first()
    
    @staticmethod
    def get_by_path(db: Session, image_path: str) -> Optional[GeneratedImage]:
        """Récupère une image par son chemin"""
        return db.query(GeneratedImage).filter(GeneratedImage.image_path == image_path).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "created_at",
        order_desc: bool = True
    ) -> List[GeneratedImage]:
        """
        Récupère toutes les images avec pagination et tri.
        
        OPÉRATION: READ (du CRUD) - Liste paginée
        
        PAGINATION:
        -----------
        Évite de charger toutes les images en mémoire d'un coup.
        Si 10,000 images en DB, on charge seulement 20 à la fois.
        
        - skip: Nombre d'éléments à sauter
        - limit: Nombre max d'éléments à retourner
        
        Exemple: Page 1 (skip=0, limit=20) → Images 1-20
                 Page 2 (skip=20, limit=20) → Images 21-40
                 Page 3 (skip=40, limit=20) → Images 41-60
        
        TRI DYNAMIQUE:
        --------------
        - order_by="created_at": Tri par date (plus récentes en premier)
        - order_by="score": Tri par score esthétique (meilleures en premier)
        - order_desc=True: Ordre décroissant (DESC)
        - order_desc=False: Ordre croissant (ASC)
        
        Utilisation dans Gradio:
            # Onglet Historique
            images = ImageRepository.get_all(
                db=db,
                skip=0,
                limit=20,
                order_by="created_at",
                order_desc=True
            )
            # → 20 images les plus récentes
        
        SQL généré (exemple):
            SELECT * FROM generated_images
            ORDER BY created_at DESC
            LIMIT 20 OFFSET 0
        """
        # Créer la requête de base
        query = db.query(GeneratedImage)
        
        # ========================================
        # TRI (ORDER BY)
        # ========================================
        # Déterminer la colonne de tri
        if order_by == "created_at":
            order_column = GeneratedImage.created_at
        elif order_by == "score":
            order_column = GeneratedImage.score
        else:
            order_column = GeneratedImage.created_at  # Défaut
        
        # Appliquer le tri (ASC ou DESC)
        if order_desc:
            query = query.order_by(desc(order_column))  # DESC
        else:
            query = query.order_by(order_column)  # ASC
        
        # ========================================
        # PAGINATION (OFFSET + LIMIT)
        # ========================================
        # offset(skip): Saute les N premiers résultats
        # limit(limit): Retourne max N résultats
        # all(): Exécute la requête et retourne une liste
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def search_by_prompt(
        db: Session,
        prompt_search: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[GeneratedImage]:
        """
        Recherche les images par mot-clé dans le prompt.
        
        OPÉRATION: SEARCH (recherche textuelle)
        
        Utilise .contains() pour recherche SQL LIKE:
            "cat" → WHERE prompt LIKE '%cat%'
        
        Exemple:
            search_by_prompt(db, "cat") →
                Trouve: "a cat", "cat in space", "black cat"
                Ne trouve pas: "dog", "tiger"
        
        SQL généré:
            SELECT * FROM generated_images
            WHERE prompt LIKE '%cat%'
            ORDER BY created_at DESC
            LIMIT 100 OFFSET 0
        
        Note: Recherche case-sensitive (dépend de la config SQLite)
        """
        return db.query(GeneratedImage).filter(
            GeneratedImage.prompt.contains(prompt_search)
        ).order_by(desc(GeneratedImage.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_best_scored(
        db: Session,
        limit: int = 10
    ) -> List[GeneratedImage]:
        """
        Récupère les N meilleures images par score esthétique.
        
        Utilité:
        - Afficher un "Hall of Fame" des meilleures générations
        - Identifier ce qui fonctionne bien
        - Portfolio automatique
        
        Filtre: .isnot(None) exclut les images sans score
        Tri: score décroissant (meilleures en premier)
        """
        return db.query(GeneratedImage).filter(
            GeneratedImage.score.isnot(None)
        ).order_by(desc(GeneratedImage.score)).limit(limit).all()
    
    @staticmethod
    def get_statistics(db: Session) -> dict:
        """
        Calcule des statistiques globales sur toutes les images.
        
        OPÉRATION: AGGREGATION (COUNT, AVG, MAX, MIN)
        
        Retourne un dictionnaire avec:
        - total_images: Nombre total d'images générées
        - average_score: Score moyen (ex: 6.8/10)
        - max_score: Meilleur score obtenu
        - min_score: Pire score obtenu
        - with_rl_optimization: Nombre avec RL
        - without_rl_optimization: Nombre sans RL
        
        Utilisé dans:
        - Onglet Statistiques de Gradio
        - Dashboard de monitoring
        - Endpoint API /statistics
        
        SQL généré:
            SELECT COUNT(id), AVG(score), MAX(score), MIN(score)
            FROM generated_images;
            
            SELECT COUNT(id) FROM generated_images
            WHERE use_rl_optimization = 1;
        
        Exemple de résultat:
            {
                "total_images": 125,
                "average_score": 6.85,
                "max_score": 9.2,
                "min_score": 3.1,
                "with_rl_optimization": 15,
                "without_rl_optimization": 110
            }
        """
        # ========================================
        # STATISTIQUES DE BASE
        # ========================================
        # func.count, func.avg, etc. sont des fonctions SQL d'agrégation
        # .scalar() retourne une valeur unique (pas une liste)
        
        total = db.query(func.count(GeneratedImage.id)).scalar()
        avg_score = db.query(func.avg(GeneratedImage.score)).scalar()
        max_score = db.query(func.max(GeneratedImage.score)).scalar()
        min_score = db.query(func.min(GeneratedImage.score)).scalar()
        
        # ========================================
        # STATISTIQUES RL
        # ========================================
        # Compter combien d'images ont été générées avec RL
        with_rl = db.query(func.count(GeneratedImage.id)).filter(
            GeneratedImage.use_rl_optimization == True
        ).scalar()
        
        # ========================================
        # CONSTRUCTION DU DICTIONNAIRE
        # ========================================
        # Gestion des cas NULL (ex: DB vide)
        # "or 0" convertit None en 0
        # "round(avg_score, 2)" arrondit à 2 décimales
        return {
            "total_images": total or 0,
            "average_score": round(avg_score, 2) if avg_score else None,
            "max_score": max_score,
            "min_score": min_score,
            "with_rl_optimization": with_rl or 0,
            "without_rl_optimization": (total or 0) - (with_rl or 0),
        }
    
    @staticmethod
    def delete(db: Session, image_id: int) -> bool:
        """Supprime une image de la base de données"""
        db_image = db.query(GeneratedImage).filter(GeneratedImage.id == image_id).first()
        if db_image:
            db.delete(db_image)
            db.commit()
            return True
        return False


class FeedbackRepository:
    """
    Repository pour gérer les feedbacks utilisateurs.
    
    Similaire à ImageRepository mais pour la table user_feedbacks.
    Permet de collecter et analyser les retours humains sur les images générées.
    
    Opérations principales:
    - CREATE: Enregistrer un nouveau feedback
    - READ: Récupérer feedbacks par image ou par utilisateur
    - STATS: Statistiques sur les feedbacks
    """
    
    @staticmethod
    def create(
        db: Session,
        generation_id: int,
        score: float,
        comment: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> UserFeedback:
        """
        Crée un nouveau feedback utilisateur.
        
        VALIDATION:
        -----------
        Vérifie que l'image référencée existe avant d'enregistrer.
        Évite les feedbacks orphelins (generation_id invalide).
        
        Workflow typique:
        1. Utilisateur génère image → GeneratedImage créé (id=42)
        2. Utilisateur voit l'image et clique "👍 J'aime" 
        3. Frontend appelle FeedbackRepository.create(generation_id=42, score=8.5)
        4. Feedback enregistré et lié à l'image #42
        
        Exemple:
            feedback = FeedbackRepository.create(
                db=db,
                generation_id=42,
                score=9.0,
                comment="Magnifique image de chat !",
                user_id="user_abc123"
            )
        
        Args:
            db: Session DB active
            generation_id: ID de l'image concernée (FK vers GeneratedImage)
            score: Note de l'utilisateur (0-10)
            comment: Commentaire textuel optionnel
            user_id: ID de l'utilisateur (optionnel, pour tracking)
        
        Returns:
            UserFeedback: Le feedback créé avec son ID
        
        Raises:
            ValueError: Si generation_id n'existe pas en DB
        """
        # ========================================
        # VALIDATION DE L'INTÉGRITÉ RÉFÉRENTIELLE
        # ========================================
        # Vérifier que l'image existe avant de créer le feedback
        # Simule une contrainte FOREIGN KEY (SQLite ne les force pas toujours)
        image = ImageRepository.get_by_id(db=db, image_id=generation_id)
        if not image:
            raise ValueError(f"Generation {generation_id} not found")
        
        # ========================================
        # CRÉATION DU FEEDBACK
        # ========================================
        feedback = UserFeedback(
            generation_id=generation_id,
            score=score,
            comment=comment,
            user_id=user_id,
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        return feedback
    
    @staticmethod
    def get_by_id(db: Session, feedback_id: int) -> Optional[UserFeedback]:
        """Récupère un feedback par son ID"""
        return db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    
    @staticmethod
    def get_by_generation_id(db: Session, generation_id: int) -> List[UserFeedback]:
        """Récupère tous les feedbacks pour une génération"""
        return db.query(UserFeedback).filter(
            UserFeedback.generation_id == generation_id
        ).order_by(desc(UserFeedback.created_at)).all()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[UserFeedback]:
        """Récupère tous les feedbacks avec pagination"""
        return db.query(UserFeedback).order_by(
            desc(UserFeedback.created_at)
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_statistics(db: Session) -> dict:
        """Récupère les statistiques des feedbacks"""
        total = db.query(func.count(UserFeedback.id)).scalar()
        avg_score = db.query(func.avg(UserFeedback.score)).scalar()
        max_score = db.query(func.max(UserFeedback.score)).scalar()
        min_score = db.query(func.min(UserFeedback.score)).scalar()
        
        return {
            "total_feedbacks": total or 0,
            "average_score": round(avg_score, 2) if avg_score else None,
            "max_score": max_score,
            "min_score": min_score,
        }


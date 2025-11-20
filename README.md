# 🎨 AI Creative Studio

**Plateforme IA** qui génère automatiquement des artworks de haute qualité en combinant :
- **Stable Diffusion** pour la génération d'images
- **Agent RL** pour optimiser les prompts et paramètres
- **API REST** déployée pour usage en production
- **Interface Gradio** pour utilisation interactive
- **Base de données SQLite** pour historique et statistiques

## 📋 Description

AI Creative Studio est un système intelligent qui :
1. Génère des images à partir de prompts textuels avec Stable Diffusion
2. Apprend automatiquement quels prompts produisent les meilleures images via Reinforcement Learning (PPO)
3. Optimise les paramètres (guidance_scale, steps, etc.) pour améliorer la qualité
4. Expose une API REST professionnelle et une interface web interactive
5. Sauvegarde l'historique des générations dans une base de données SQLite

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   FRONTEND                              │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐              ┌─────────────┐          │
│  │   Gradio    │              │   FastAPI   │          │
│  │  (UI Web)   │              │   (REST)    │          │
│  │  Port 7860  │              │  Port 8000  │          │
│  └──────┬──────┘              └──────┬──────┘          │
│         │                             │                 │
│         └──────────────┬──────────────┘                 │
│                        │                                │
├────────────────────────┼────────────────────────────────┤
│                   BACKEND CORE                          │
│         ┌──────────────┼──────────────┐                 │
│         │              │              │                 │
│         ▼              ▼              ▼                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │   STABLE   │  │  RL AGENT  │  │  AESTHETIC │       │
│  │  DIFFUSION │  │  (PPO)     │  │  PREDICTOR │       │
│  │ (txt2img)  │  │  (Prompts) │  │  (Reward)  │       │
│  │   ~4 GB    │  │  ~50 MB    │  │   0 MB     │       │
│  └────────────┘  └────────────┘  └────────────┘       │
│         │              │              │                 │
│         └──────────────┼──────────────┘                 │
│                        │                                │
│                 ┌─────────────┐                         │
│                 │  SQLite DB  │                         │
│                 │  (Historique)│                        │
│                 └─────────────┘                         │
└─────────────────────────────────────────────────────────┘
```

### Composants Principaux

**Backend Core** (`app/models/`) :
- `stable_diffusion.py` : Génération d'images avec Stable Diffusion v1.5 (configurable pour autres modèles)
- `rl_agent.py` : Agent RL (PPO) pour optimisation de prompts
- `aesthetic_scorer.py` : Évaluation de la qualité esthétique des images

**API & Frontend** :
- `app/main.py` : Application FastAPI principale
- `app/gradio_ui.py` : Interface web interactive Gradio
- `app/api/routes.py` : Endpoints REST API
- `app/database/` : Modèles et repository SQLite pour historique

**Training** (`training/`) :
- `rl_env.py` : Environnement Gymnasium pour optimisation de prompts
- `train_rl_agent.py` : Script d'entraînement RL local
- `colab_train_rl.ipynb` : Notebook Colab pour entraînement sur GPU

## 🚀 Démarrage Rapide

### 1. Installation

**Prérequis** :
- Python 3.10, 3.11, ou 3.12
- CUDA (recommandé pour GPU)
- Git

**⚠️ Note Python 3.12** : PyTorch 2.2+ est requis (inclus dans requirements.txt)

```bash
# Cloner le repository
git clone https://github.com/VOTRE-USER/VOTRE-REPO.git
cd Projet_fil_rouge_ML_DL

# Créer environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OU .venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# OU avec uv (plus rapide)
uv pip install -r requirements.txt

# Configuration
cp env.example .env
# Éditer .env selon votre hardware (CPU/GPU)
```

### 2. Test Stable Diffusion

```bash
# Test rapide de génération
python -c "
from app.models.stable_diffusion import sd_generator
image = sd_generator.generate(
    prompt='a beautiful sunset, mountains',
    num_inference_steps=25
)
image.save('test_output.png')
print('✅ Image générée: test_output.png')
"
```

**⏱️ Première fois** : Téléchargement du modèle Stable Diffusion (~4 GB, 5-10 min)

### 3. Lancer l'Interface Gradio (Recommandé)

```bash
python run_gradio.py
```

Interface accessible sur `http://localhost:7860` :
- Génération d'images avec visualisation
- Optimisation RL intégrée
- Historique des générations
- Statistiques et recherche

### 4. Lancer l'API FastAPI (Optionnel)

```bash
python -m app.main
# OU
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API accessible sur `http://localhost:8000` :
- Documentation Swagger : `http://localhost:8000/docs`
- Redoc : `http://localhost:8000/redoc`

## 🤖 Entraînement RL Agent

### Stratégie Recommandée : Workflow Hybride

**Entraînement sur Google Colab (GPU) + Exécution locale**

- ✅ **20-40x plus rapide** sur Colab GPU vs CPU local
- ✅ **Gratuit** avec GPU T4
- ✅ **30 minutes** pour 2500 steps (tests rapides)
- ✅ **1-2 heures** pour 10000 steps (qualité recommandée)

### Entraînement sur Google Colab

#### Étape 1 : Préparer GitHub

**⚠️ IMPORTANT** : Uploader **TOUT le projet** sur GitHub (pas seulement le notebook)

Le notebook Colab a besoin de tout le code car il importe :
- `app.models.rl_agent` → Nécessite `app/`
- `training.rl_env` → Nécessite `training/`
- `app.models.stable_diffusion` → Nécessite `app/models/`

**Commandes Git** :
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

**Fichiers à uploader** :
- ✅ Tous les dossiers `app/`, `training/`, `notebooks/`
- ✅ `requirements.txt`, `README.md`, `.gitignore`
- ❌ Pas de `.env`, `__pycache__/`, `outputs/*.png`, `models/*.zip` (dans `.gitignore`)

#### Étape 2 : Ouvrir sur Google Colab

**Option A : Depuis GitHub (Recommandé)**
1. Aller sur [Google Colab](https://colab.research.google.com/)
2. **File** > **Open notebook** > Onglet **GitHub**
3. Entrer votre URL GitHub : `https://github.com/VOTRE-USER/VOTRE-REPO`
4. Sélectionner `notebooks/colab_train_rl.ipynb`

**Option B : Upload manuel**
1. **File** > **Upload notebook**
2. Sélectionner `notebooks/colab_train_rl.ipynb` depuis votre ordinateur

#### Étape 3 : Activer le GPU (CRUCIAL)

1. **Runtime** > **Change runtime type**
2. Sélectionner **GPU** (T4 gratuit recommandé)
3. Cliquer **Save**

**⚠️ Sans GPU** : L'entraînement sera très lent (20-40x plus lent)

#### Étape 4 : Configurer et Exécuter

1. **Vérifier l'URL du repository** dans la cellule 2 :
   ```python
   REPO_URL = "https://github.com/VOTRE-USER/VOTRE-REPO.git"
   ```

2. **Exécuter les cellules dans l'ordre** :
   - Cellule 1 : Installation dépendances (2-5 min)
   - Cellule 2 : Clone repository (30 sec)
   - Cellule 3 : Vérification GPU (doit afficher "CUDA disponible: True")
   - Cellule 4 : Entraînement RL (**30 minutes** pour 2500 steps, **1-2 heures** pour 10000 steps)

3. **Télécharger le modèle** :
   - Option A : Cellule de téléchargement direct → `rl_agent.zip`
   - Option B : Sauvegarder dans Google Drive → Télécharger depuis Drive

#### Étape 5 : Utiliser le modèle localement

```bash
# Placer le modèle dans le dossier models/
mv ~/Downloads/rl_agent.zip models/rl_agent.zip

# Le modèle sera automatiquement chargé par l'API ou Gradio
```

### Comparaison Temps d'Entraînement

| Steps | Colab (GPU) | Local (CPU) | Gain |
|-------|-------------|-------------|------|
| 2.5k | ~30 min | ~10-20 heures | **20-40x** |
| 10k | ~1-2 heures | ~20-40 heures | **20-40x** |
| 20k | ~2-4 heures | ~40-80 heures | **20-40x** |

**💡 Configuration actuelle** : 2500 steps (~30 minutes) pour tests rapides

Pour meilleure qualité, modifier dans Colab :
```python
TOTAL_TIMESTEPS = 10000  # Au lieu de 2500
```

### Entraînement Local (CPU - Recommandé si Colab s'arrête)

**⚡ Mode rapide activé par défaut** (3-5x plus rapide sur CPU) :

```bash
# Entraînement rapide (2500 steps, ~2-4 heures sur CPU avec fast_mode)
python training/train_rl_agent.py --total_timesteps 2500

# Entraînement complet (5000 steps, ~4-8 heures sur CPU avec fast_mode)
python training/train_rl_agent.py --total_timesteps 5000

# Entraînement qualité maximale (10000 steps, ~8-16 heures sur CPU avec fast_mode)
python training/train_rl_agent.py --total_timesteps 10000

# Désactiver fast_mode pour meilleure qualité (plus lent - seulement si vous avez le temps)
python training/train_rl_agent.py --total_timesteps 5000 --no-fast_mode
```

**💡 Recommandations pour CPU (16GB RAM)** :
- ✅ **Utilisez `fast_mode`** (activé par défaut) : 3-5x plus rapide
- ✅ **Commencez avec 2500 steps** : ~2-4 heures, bon compromis qualité/vitesse
- ✅ **L'entraînement peut être arrêté avec Ctrl+C** : checkpoints sauvegardés automatiquement
- ✅ **Vérifiez `.env`** : `SD_DEVICE=cpu` et `SD_DTYPE=float32`

**⏱️ Temps estimés (CPU, fast_mode activé)** :
- 2500 steps : ~2-4 heures
- 5000 steps : ~4-8 heures  
- 10000 steps : ~8-16 heures

## 🎨 Qualité Artistique

### Modèle Stable Diffusion Actuel

**Configuration par défaut** : `runwayml/stable-diffusion-v1-5`
- ✅ Bon pour démarrer
- ⚠️ Généraliste, pas spécialisé art

### Modèles Recommandés pour Art

**DreamShaper (Recommandé pour art)** :
```bash
# Dans .env
SD_MODEL_ID=lykon/dreamshaper-8
```
- 🎨 Spécialisé styles artistiques
- ✅ Meilleure qualité visuelle
- ✅ Styles variés (réaliste, fantastique, etc.)

**Autres options** :
- `SG161222/Realistic_Vision_V5.1_noVAE` : Art photoréaliste
- `andite/anything-v4.0` : Anime/Art japonais
- `warrior-mama/AbyssOrangeMix2` : Mélange styles

### Prompts Artistiques Efficaces

**Structure recommandée** :
```
[Style artistique], [Sujet], [Détails techniques], [Qualité], [Mood/Lumière]
```

**Exemples** :
```
"Digital art, a majestic dragon, highly detailed scales, vibrant colors, 
cinematic lighting, masterpiece, 8k resolution, trending on artstation"

"Concept art, fantasy castle in the clouds, intricate architecture, 
epic composition, dramatic lighting, professional artwork"
```

**Negative prompts recommandés** :
```
"low quality, blurry, distorted, watermark, signature, 
text, writing, bad anatomy, deformed, ugly, amateur"
```

### Paramètres Optimaux pour Art

```python
guidance_scale = 7.5 - 9.0      # 7.5 OK, 8.5 meilleur pour art
num_inference_steps = 50 - 80   # 50 OK, 70-80 pour qualité max
width = 512                      # Standard
height = 512                     # Standard
# Pour très haute qualité : 768x768 (mais plus lent)
```

## 💻 Utilisation API

### Génération simple

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful landscape with mountains",
    "num_inference_steps": 50,
    "guidance_scale": 7.5
  }'
```

### Génération avec optimisation RL

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful landscape",
    "use_rl_optimization": true
  }'
```

### Historique et Statistiques

```bash
# Obtenir l'historique
curl "http://localhost:8000/api/v1/history?limit=10"

# Rechercher par prompt
curl "http://localhost:8000/api/v1/search?query=landscape"

# Obtenir les meilleures images
curl "http://localhost:8000/api/v1/best?limit=5"

# Statistiques globales
curl "http://localhost:8000/api/v1/statistics"
```

## 📁 Structure du Projet

```
Projet_fil_rouge_ML_DL/
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── env.example
├── .gitignore
│
├── app/
│   ├── main.py                 # FastAPI app
│   ├── gradio_ui.py            # Interface Gradio
│   ├── models/
│   │   ├── stable_diffusion.py # SD pipeline
│   │   ├── rl_agent.py         # Agent RL
│   │   └── aesthetic_scorer.py # Predictor
│   ├── api/
│   │   ├── routes.py           # Endpoints
│   │   └── schemas.py          # Pydantic models
│   ├── database/
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── database.py         # DB config
│   │   └── repository.py       # CRUD operations
│   └── utils/
│       ├── config.py           # Configuration
│       └── helpers.py          # Fonctions utilitaires
│
├── training/
│   ├── train_rl_agent.py       # Script entraînement RL
│   ├── evaluate_agent.py       # Évaluation
│   └── rl_env.py               # Environnement Gym custom
│
├── notebooks/
│   └── colab_train_rl.ipynb    # Notebook Colab pour GPU
│
├── models/                     # Modèles sauvegardés
│   └── rl_agent.zip            # Agent RL entraîné
│
├── outputs/                    # Images générées
│   ├── portfolio/
│   └── experiments/
│
├── data/                       # Base de données SQLite
│   └── ai_creative_studio.db   # Historique générations
│
└── tests/
    ├── test_api.py
    └── test_models.py
```

## 🐳 Déploiement avec Docker

```bash
# Build l'image
docker build -t ai-creative-studio .

# Lancer le container
docker run -p 8000:8000 \
  -e SD_DEVICE=cpu \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/models:/app/models \
  ai-creative-studio
```

### Docker Compose

```bash
docker-compose up
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest tests/

# Avec coverage
pytest tests/ --cov=app --cov-report=html
```

## 📊 Critères d'Évaluation

- **Technique (25 pts)** : GenAI (10), RL Agent (10), MLOps (5)
- **Innovation & Ambition (7 pts)** : Créativité, qualité, ambition
- **Intégration (7 pts)** : GenAI + RL cohérent, déploiement
- **Déploiement (6 pts)** : Docker, AWS, documentation
- **Présentation (5 pts)** : Démo, explication, slides

## ⚠️ Notes Importantes

- **CUDA Out of Memory** : Utilisez `float32` au lieu de `float16` ou réduisez la résolution
- **Python 3.12** : PyTorch 2.2+ requis (inclus dans requirements.txt)
- **Agent RL** : 2500 steps minimum pour tests, 10000 steps recommandés pour qualité
- **Entraînement** : Utiliser Colab GPU pour 20-40x plus rapide que CPU local
- **Modèle SD** : Premier chargement télécharge ~4 GB (5-10 min)

## 🔗 Ressources

- [Stable Diffusion Docs](https://huggingface.co/docs/diffusers/)
- [Stable-Baselines3 Docs](https://stable-baselines3.readthedocs.io/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Gymnasium Docs](https://gymnasium.farama.org/)
- [Gradio Docs](https://gradio.app/)

## 📝 License

Ce projet est créé dans le cadre d'un projet académique.

---

**Bon courage ! 🚀**

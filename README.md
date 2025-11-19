# 🎨 AI Creative Studio

**Plateforme IA** qui génère automatiquement des artworks de haute qualité en combinant :
- **Stable Diffusion** pour la génération d'images
- **Agent RL** pour optimiser les prompts et paramètres
- **API REST** déployée pour usage en production

## 📋 Description

AI Creative Studio est un système intelligent qui :
1. Génère des images à partir de prompts textuels
2. Apprend automatiquement quels prompts produisent les meilleures images
3. Optimise les paramètres (guidance_scale, steps, etc.) via Reinforcement Learning
4. Expose une API REST professionnelle et déployable

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
└─────────────────────────────────────────────────────────┘
```

📋 **Voir l'architecture détaillée : `BACKEND_ARCHITECTURE.md`**


## 🎯 Stratégie Recommandée : Workflow Hybride

**Entraînement RL sur Google Colab + Exécution locale**

- **Sprint 2 (RL)** : Entraîner sur Colab avec GPU (1-2h vs 20-40h local)
- **Sprints 1, 3, 4** : Exécuter localement avec modèle pré-entraîné

📋 **Voir le guide complet : `WORKFLOW_HYBRIDE.md`**

## 🚀 Démarrage Rapide

📋 **Voir le guide complet étape par étape : `GETTING_STARTED.md`**

**Ordre d'exécution recommandé :**

1. **Installation** → Dépendances et configuration
2. **Test Stable Diffusion** → Vérifier la génération
3. **Entraînement RL** → Sur Colab (recommandé) ou local
4. **Lancement API** → Démarrer FastAPI
5. **Test API** → Vérifier que tout fonctionne

## 🚀 Installation

### Prérequis

- **Python 3.10, 3.11, ou 3.12** (3.10 ou 3.11 recommandés pour compatibilité maximale)
- CUDA (recommandé pour GPU)
- Git

**⚠️ Note** : Si vous utilisez Python 3.12, PyTorch 2.2+ est requis (torch 2.1.1 ne supporte que Python 3.8-3.11)

### Installation avec pip

```bash
# Cloner le repository
git clone <votre-repo>
cd Projet_fil_rouge_ML_DL

# Créer environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OU .venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt
```

### Installation avec uv (recommandé)

```bash
# Installer uv si pas déjà fait
curl -LsSf https://astral.sh/uv/install.sh | sh

# Créer environnement
uv venv .venv
source .venv/bin/activate

# Installer dépendances
uv pip install -r requirements.txt
```

### Configuration

```bash
# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env selon vos besoins
# Notamment SD_DEVICE (cuda/cpu) selon votre hardware
```

## 💻 Utilisation

### Lancer l'Interface Gradio (Recommandé)

```bash
# Lancer l'interface Gradio interactive
python run_gradio.py

# OU directement
python -m app.gradio_ui
```

L'interface sera accessible sur `http://localhost:7860`
- Interface web interactive
- Génération d'images avec visualisation
- Optimisation RL intégrée
- Paramètres ajustables

### Lancer l'API FastAPI (Optionnel)

```bash
# Lancer le serveur FastAPI
python -m app.main

# Ou avec uvicorn directement
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

L'API sera accessible sur `http://localhost:8000`
- Documentation Swagger : `http://localhost:8000/docs`
- Redoc : `http://localhost:8000/redoc`

### Entraîner l'agent RL

```bash
# Entraînement de base (10000 steps)
python training/train_rl_agent.py

# Avec options personnalisées
python training/train_rl_agent.py --total_timesteps 20000 --save_path models/rl_agent_custom.zip
```

### Évaluer l'agent RL

```bash
# Tester l'optimisation sur un prompt
python training/evaluate_agent.py --prompt "a beautiful sunset" --n_iterations 10
```

### Utiliser l'API

#### Génération simple

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful landscape with mountains",
    "num_inference_steps": 50,
    "guidance_scale": 7.5
  }'
```

#### Génération avec optimisation RL

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful landscape",
    "use_rl_optimization": true
  }'
```

#### Optimiser un prompt

```bash
curl -X POST "http://localhost:8000/api/v1/optimize" \
  -H "Content-Type: application/json" \
  -d '{
    "base_prompt": "a cat",
    "n_iterations": 10
  }'
```

## 🐳 Déploiement avec Docker

### Build l'image

```bash
docker build -t ai-creative-studio .
```

### Lancer le container

```bash
docker run -p 8000:8000 \
  -e SD_DEVICE=cpu \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/models:/app/models \
  ai-creative-studio
```

### Docker Compose (optionnel)

Créer un fichier `docker-compose.yml` :

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SD_DEVICE=cpu
    volumes:
      - ./outputs:/app/outputs
      - ./models:/app/models
```

Puis :

```bash
docker-compose up
```

## 📁 Structure du Projet

```
ai-creative-studio/
├── README.md
├── requirements.txt
├── Dockerfile
├── .env.example
│
├── app/
│   ├── main.py                 # FastAPI app
│   ├── models/
│   │   ├── stable_diffusion.py # SD pipeline
│   │   ├── rl_agent.py         # Agent RL
│   │   └── aesthetic_scorer.py # Predictor
│   ├── api/
│   │   ├── routes.py           # Endpoints
│   │   └── schemas.py          # Pydantic models
│   └── utils/
│       ├── config.py           # Configuration
│       └── helpers.py          # Fonctions utilitaires
│
├── training/
│   ├── train_rl_agent.py       # Script entraînement RL
│   ├── evaluate_agent.py       # Évaluation
│   └── rl_env.py               # Environnement Gym custom
│
├── models/                     # Modèles sauvegardés
│   ├── sd_model/
│   └── rl_agent.zip
│
├── outputs/                    # Images générées
│   ├── portfolio/
│   └── experiments/
│
└── tests/
    ├── test_api.py
    └── test_models.py
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

## 🔗 Ressources

- [Stable Diffusion Docs](https://huggingface.co/docs/diffusers/)
- [Stable-Baselines3 Docs](https://stable-baselines3.readthedocs.io/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Gymnasium Docs](https://gymnasium.farama.org/)

## ⚠️ Notes Importantes

- **CUDA Out of Memory** : Utilisez `float32` au lieu de `float16` ou réduisez la résolution
- **Docker image grosse** : Les modèles SD sont téléchargés au runtime, pas inclus dans l'image
- **Agent RL** : 10000 steps minimum recommandés pour de bons résultats

## 📝 License

Ce projet est créé dans le cadre d'un projet académique.

---

**Bon courage ! 🚀**


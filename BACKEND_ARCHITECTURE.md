# 🔧 Architecture du Backend - AI Creative Studio

Documentation de l'architecture backend du projet.

## 📋 Vue d'Ensemble

Le backend est composé de **deux couches principales** :

1. **Backend Core** : Modèles ML et logique métier (couche métier)
2. **Backend API** : FastAPI (API REST) + Gradio (Interface web)

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND / INTERFACE                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐                    ┌─────────────┐        │
│  │   Gradio    │                    │   FastAPI   │        │
│  │  (UI Web)   │                    │   (REST)    │        │
│  │  Port 7860  │                    │  Port 8000  │        │
│  └──────┬──────┘                    └──────┬──────┘        │
│         │                                   │               │
│         └──────────────┬────────────────────┘               │
│                        │                                    │
├────────────────────────┼────────────────────────────────────┤
│                   BACKEND CORE                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  app/models/                                         │  │
│  │  ├── stable_diffusion.py   (Génération images)      │  │
│  │  ├── rl_agent.py            (Optimisation prompts)   │  │
│  │  └── aesthetic_scorer.py   (Évaluation qualité)     │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  app/utils/                                          │  │
│  │  ├── config.py          (Configuration)             │  │
│  │  └── helpers.py         (Fonctions utilitaires)     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Backend Core (Couche Métier)

Le **backend core** contient la logique métier et les modèles ML. C'est la couche indépendante qui fait le vrai travail.

### Structure : `app/models/`

#### 1. **Stable Diffusion** (`stable_diffusion.py`)

**Rôle** : Génération d'images à partir de prompts textuels

```python
from app.models.stable_diffusion import sd_generator

# Génération d'image
image = sd_generator.generate(
    prompt="a beautiful landscape",
    guidance_scale=7.5,
    num_inference_steps=50,
    width=512,
    height=512
)
```

**Fichier** : `app/models/stable_diffusion.py`
- Classe : `StableDiffusionGenerator`
- Instance globale : `sd_generator`
- Modèle : Hugging Face `runwayml/stable-diffusion-v1-5`

#### 2. **RL Agent** (`rl_agent.py`)

**Rôle** : Optimisation de prompts avec Reinforcement Learning

```python
from app.models.rl_agent import get_rl_optimizer

rl_optimizer = get_rl_optimizer()
result = rl_optimizer.optimize_prompt(
    base_prompt="a cat",
    n_iterations=10
)
```

**Fichier** : `app/models/rl_agent.py`
- Classe : `RLOptimizer`
- Algorithme : PPO (Proximal Policy Optimization)
- Modèle : Stable-Baselines3

#### 3. **Aesthetic Scorer** (`aesthetic_scorer.py`)

**Rôle** : Évaluation de la qualité esthétique des images

```python
from app.models.aesthetic_scorer import aesthetic_scorer

score = aesthetic_scorer.score(image)  # Retourne 0-10
```

**Fichier** : `app/models/aesthetic_scorer.py`
- Classe : `AestheticScorer`
- Instance globale : `aesthetic_scorer`
- Méthode : Heuristique simple (peut être améliorée avec CLIP)

### Structure : `app/utils/`

#### 1. **Configuration** (`config.py`)

**Rôle** : Gestion de la configuration via variables d'environnement

```python
from app.utils.config import settings

# Accès à la configuration
print(settings.SD_DEVICE)  # cuda ou cpu
print(settings.SD_MODEL_ID)  # runwayml/stable-diffusion-v1-5
```

**Fichier** : `app/utils/config.py`
- Classe : `Settings` (Pydantic)
- Source : Fichier `.env` ou variables d'environnement

#### 2. **Helpers** (`helpers.py`)

**Rôle** : Fonctions utilitaires (chemins, dossiers, etc.)

```python
from app.utils.helpers import get_output_path

output_dir = get_output_path("portfolio")  # outputs/portfolio/
```

**Fichier** : `app/utils/helpers.py`

---

## 🌐 Backend API (Couches d'Exposition)

Le **backend API** expose le backend core via deux interfaces différentes.

### Option 1 : FastAPI (API REST)

**Fichier** : `app/main.py` + `app/api/routes.py`

**Rôle** : API REST pour intégration avec d'autres services

**Endpoints** :
- `POST /api/v1/generate` : Générer une image
- `POST /api/v1/optimize` : Optimiser un prompt
- `GET /api/v1/health` : Health check
- `GET /api/v1/` : Root endpoint

**Utilisation** :
```bash
# Lancer l'API
python -m app.main

# Accès : http://localhost:8000
# Docs : http://localhost:8000/docs
```

**Exemple de requête** :
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cat", "use_rl_optimization": true}'
```

**Structure** :
- `app/main.py` : Application FastAPI principale
- `app/api/routes.py` : Définition des routes/endpoints
- `app/api/schemas.py` : Modèles Pydantic pour validation

### Option 2 : Gradio (Interface Web Interactive)

**Fichier** : `app/gradio_ui.py`

**Rôle** : Interface web interactive pour utilisateurs finaux

**Fonctionnalités** :
- Interface graphique avec sliders, checkboxes, etc.
- Visualisation directe des images générées
- Onglets pour différentes fonctionnalités
- Exemples de prompts intégrés

**Utilisation** :
```bash
# Lancer l'interface Gradio
python run_gradio.py

# Accès : http://localhost:7860
```

**Structure** :
- `app/gradio_ui.py` : Interface Gradio complète
- `run_gradio.py` : Script de lancement

---

## 🔄 Flux de Données

### Flux avec FastAPI

```
Client (curl/Postman/Postman)
    ↓
FastAPI (app/main.py)
    ↓
Routes (app/api/routes.py)
    ↓
Backend Core (app/models/)
    ├── sd_generator.generate()
    ├── rl_optimizer.optimize_prompt()
    └── aesthetic_scorer.score()
    ↓
Réponse JSON
```

### Flux avec Gradio

```
Utilisateur (Navigateur)
    ↓
Gradio UI (app/gradio_ui.py)
    ↓
Backend Core (app/models/)
    ├── sd_generator.generate()
    ├── rl_optimizer.optimize_prompt()
    └── aesthetic_scorer.score()
    ↓
Interface Web (Image + Infos)
```

**⚠️ Important** : Gradio utilise **directement** le backend core, **pas via FastAPI**.

---

## 📊 Comparaison FastAPI vs Gradio

| Aspect | FastAPI | Gradio |
|--------|---------|--------|
| **Type** | API REST | Interface Web |
| **Utilisation** | Intégration avec d'autres services | Utilisateurs finaux |
| **Format** | JSON (HTTP requests) | Interface graphique |
| **Documentation** | Swagger automatique | Interface intuitive |
| **Port** | 8000 | 7860 |
| **Accès Backend** | Via routes FastAPI | Direct au backend core |
| **Cas d'usage** | Production, API publique | Démo, tests, développement |

---

## 🎯 Architecture en Détail

### Backend Core (Indépendant)

Le backend core peut être utilisé **indépendamment** des API :

```python
# Utilisation directe du backend core
from app.models.stable_diffusion import sd_generator
from app.models.rl_agent import get_rl_optimizer
from app.models.aesthetic_scorer import aesthetic_scorer

# Génération
image = sd_generator.generate(prompt="test")

# Optimisation
rl_optimizer = get_rl_optimizer()
result = rl_optimizer.optimize_prompt("a cat")

# Scoring
score = aesthetic_scorer.score(image)
```

### Backend API (Exposition)

Les API exposent le backend core de manière différente :

**FastAPI** : Via endpoints HTTP/JSON
```python
# app/api/routes.py
@router.post("/generate")
async def generate_image(request: GenerateRequest):
    # Appelle le backend core
    image = sd_generator.generate(...)
    return JSONResponse(...)
```

**Gradio** : Via interface graphique
```python
# app/gradio_ui.py
def generate_image(prompt, ...):
    # Appelle directement le backend core
    image = sd_generator.generate(...)
    return image, info_text
```

---

## 📁 Structure des Fichiers Backend

```
app/
├── main.py                 # FastAPI app (Backend API)
├── gradio_ui.py            # Gradio interface (Backend API)
│
├── models/                 # Backend Core (Modèles ML)
│   ├── stable_diffusion.py
│   ├── rl_agent.py
│   └── aesthetic_scorer.py
│
├── api/                    # FastAPI routes (Backend API)
│   ├── routes.py
│   └── schemas.py
│
└── utils/                  # Backend Core (Utilitaires)
    ├── config.py
    └── helpers.py
```

---

## 🔑 Points Clés

### 1. Backend Core = Logique Métier

Le backend core (`app/models/`) contient :
- ✅ La logique de génération d'images
- ✅ La logique d'optimisation RL
- ✅ La logique d'évaluation esthétique
- ✅ **Indépendant** des API (FastAPI ou Gradio)

### 2. Backend API = Exposition

Le backend API contient :
- ✅ **FastAPI** : Exposition via API REST (JSON)
- ✅ **Gradio** : Exposition via interface web interactive
- ✅ **Les deux utilisent le même backend core**

### 3. Modularité

- Le backend core peut être utilisé **sans API**
- Les API peuvent être utilisées **indépendamment**
- Facile d'ajouter d'autres API (GraphQL, gRPC, etc.)

---

## 💡 Utilisation Recommandée

### Développement / Démo
```bash
# Utiliser Gradio (interface interactive)
python run_gradio.py
# Accès : http://localhost:7860
```

### Production / Intégration
```bash
# Utiliser FastAPI (API REST)
python -m app.main
# Accès : http://localhost:8000
# Docs : http://localhost:8000/docs
```

### Scripts / Tests
```python
# Utiliser directement le backend core
from app.models.stable_diffusion import sd_generator
image = sd_generator.generate("test")
```

---

## 📚 Résumé

**Backend = Backend Core + Backend API**

- **Backend Core** (`app/models/`) : Logique métier et modèles ML
- **Backend API** :
  - **FastAPI** (`app/main.py` + `app/api/`) : API REST
  - **Gradio** (`app/gradio_ui.py`) : Interface web interactive

Les deux API utilisent le **même backend core**, donc la logique est centralisée et réutilisable.


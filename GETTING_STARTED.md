# 🚀 Guide de Démarrage - Ordre d'Exécution

Guide étape par étape pour lancer le projet AI Creative Studio dans le bon ordre.

## 📋 Vue d'Ensemble

Le projet doit être lancé dans cet ordre :

1. **Installation** - Dépendances et configuration
2. **Test Stable Diffusion** - Vérifier que la génération fonctionne
3. **Entraînement RL** - Entraîner l'agent (sur Colab recommandé)
4. **Lancement API** - Démarrer l'API FastAPI
5. **Test API** - Vérifier que tout fonctionne

---

## 🎯 Ordre d'Exécution Détaillé

### Étape 1 : Installation ⚙️

**Durée** : 10-30 minutes

#### 1.1 Créer l'environnement virtuel

```bash
# Créer environnement virtuel
python -m venv .venv

# Activer l'environnement
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

#### 1.2 Installer les dépendances

```bash
# Installer toutes les dépendances
pip install -r requirements.txt

# OU avec uv (si vous utilisez uv)
uv pip install -r requirements.txt
```

**⏱️ Temps estimé** : 10-20 minutes (téléchargement de PyTorch, Diffusers, etc.)

**⚠️ Note Python 3.12** : Si vous utilisez Python 3.12, les versions dans requirements.txt sont automatiquement compatibles (PyTorch 2.2+). Pour Python 3.10-3.11, vous pouvez aussi utiliser ces versions.

#### 1.3 Configuration

```bash
# Créer le fichier .env depuis le template
cp env.example .env

# Éditer .env selon votre hardware
# Si CPU:
#   SD_DEVICE=cpu
#   SD_DTYPE=float32
# Si GPU:
#   SD_DEVICE=cuda
#   SD_DTYPE=float16
```

**✅ Validation** : Vérifier que `.env` existe et contient la bonne configuration

---

### Étape 2 : Test Stable Diffusion 🎨

**Durée** : 2-5 minutes (CPU) ou 30 secondes (GPU)

#### 2.1 Test rapide de génération

```bash
# Créer un script de test simple
python -c "
from app.models.stable_diffusion import sd_generator
print('🔄 Chargement du modèle Stable Diffusion...')
print('⏱️ Première fois: téléchargement ~4 GB (5-10 min)')
print('📦 Modèle en cache ensuite')
image = sd_generator.generate(
    prompt='a beautiful sunset, mountains',
    num_inference_steps=25,  # Moins de steps pour test rapide
    width=512,
    height=512
)
print('✅ Génération réussie!')
image.save('test_output.png')
print('💾 Image sauvegardée: test_output.png')
"
```

**✅ Validation** : 
- Vérifier qu'il n'y a pas d'erreur
- Vérifier que `test_output.png` existe
- Ouvrir l'image pour vérifier la qualité

**⚠️ Note** : La première fois, le modèle Stable Diffusion sera téléchargé (~4 GB, 5-10 minutes)

---

### Étape 3 : Entraînement RL Agent 🤖

**Durée** : 1-2 heures (Colab GPU) ou 20-40 heures (Local CPU)

**📌 IMPORTANT** : Entraînement recommandé sur **Google Colab** (20-40x plus rapide)

#### Option A : Sur Google Colab (Recommandé) ⚡

1. **Ouvrir le notebook Colab**
   - Aller sur [Google Colab](https://colab.research.google.com/)
   - Upload `notebooks/colab_train_rl.ipynb`
   - **OU** cloner votre repo directement dans Colab

2. **Activer GPU**
   - `Runtime > Change runtime type > GPU (T4 ou V100)`

3. **Modifier l'URL du repo** (si clonage)
   ```python
   REPO_URL = "https://github.com/VOTRE-USER/VOTRE-REPO.git"
   ```

4. **Exécuter toutes les cellules**
   - Installation des dépendances
   - Entraînement RL (10k steps = ~1-2h)
   - Téléchargement du modèle

5. **Télécharger le modèle**
   - Le notebook télécharge automatiquement `rl_agent.zip`
   - Placer le fichier dans `models/rl_agent.zip` de votre projet local

**✅ Validation** : Vérifier que `models/rl_agent.zip` existe (~10-50 MB)

#### Option B : Local (CPU) 🐌

```bash
# Entraînement local (TRÈS LENT sur CPU)
python training/train_rl_agent.py --total_timesteps 10000

# ⚠️ ATTENTION: 20-40 heures sur CPU
```

**💡 Recommandation** : Utiliser Colab pour l'entraînement, même si vous exécutez l'API localement.

---

### Étape 4 : Test de l'Agent RL 🧪

**Durée** : 2-5 minutes

```bash
# Tester que l'agent fonctionne
python training/evaluate_agent.py --prompt "a cat" --n_iterations 5

# Vérifier les résultats:
# - Prompt original vs optimisé
# - Score original vs optimisé
# - Amélioration mesurée
```

**✅ Validation** : Vérifier que l'optimisation fonctionne et améliore le score

---

### Étape 5 : Lancement de l'Interface Gradio 🚀

**Durée** : Instantané (démarrage)

```bash
# Lancer l'interface Gradio interactive (RECOMMANDÉ)
python run_gradio.py

# OU directement
python -m app.gradio_ui
```

**✅ Validation** :
- Interface accessible sur `http://localhost:7860`
- Interface web interactive avec génération d'images
- Visualisation directe des résultats
- Optimisation RL intégrée

**⚠️ Note** : L'interface chargera automatiquement :
- Stable Diffusion au démarrage (~4 GB en mémoire si GPU)
- Agent RL depuis `models/rl_agent.zip` (si disponible)

### Étape 5bis : Lancer l'API FastAPI (Optionnel) 🌐

Si vous préférez utiliser l'API REST au lieu de Gradio :

```bash
# Lancer l'API FastAPI
python -m app.main

# OU avec uvicorn directement
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**✅ Validation** :
- API accessible sur `http://localhost:8000`
- Documentation Swagger : `http://localhost:8000/docs`
- Health check : `http://localhost:8000/api/v1/health`

---

### Étape 6 : Test de l'Interface Gradio 🧪

**Durée** : 2 minutes

#### 6.1 Ouvrir l'interface

1. Ouvrir votre navigateur
2. Aller sur `http://localhost:7860`
3. Vous devriez voir l'interface Gradio avec plusieurs onglets

#### 6.2 Test Génération Simple

1. **Onglet "Génération d'Images"**
2. Entrer un prompt : `a beautiful landscape with mountains`
3. Cocher ou décocher "Utiliser optimisation RL" (selon disponibilité du modèle)
4. Ajuster les paramètres si nécessaire (steps, guidance scale, etc.)
5. Cliquer sur "🎨 Générer"
6. Attendre la génération (~3-5 minutes sur CPU, ~10-30s sur GPU)

**✅ Validation** : 
- Vérifier que l'image apparaît dans la zone de sortie
- Vérifier les informations (score, temps de génération, etc.)
- Vérifier que l'image est sauvegardée dans `outputs/portfolio/`

#### 6.3 Test Optimisation RL (si modèle entraîné)

1. **Onglet "🤖 Optimisation RL"**
2. Entrer un prompt simple : `a cat`
3. Ajuster le nombre d'itérations (10 recommandé)
4. Cliquer sur "🚀 Optimiser"
5. Attendre les résultats

**✅ Validation** : 
- Vérifier que le prompt optimisé est différent du prompt original
- Vérifier l'amélioration du score
- Vérifier les paramètres optimaux recommandés

#### 6.4 Test Génération avec RL

1. **Onglet "Génération d'Images"**
2. Entrer un prompt simple : `a cat`
3. **Cocher "Utiliser optimisation RL"**
4. Cliquer sur "🎨 Générer"

**✅ Validation** : 
- Vérifier que le prompt optimisé est affiché dans les informations
- Vérifier l'amélioration du score
- Vérifier que l'image est générée

### Étape 6bis : Test de l'API FastAPI (si utilisée) 🌐

Si vous utilisez l'API FastAPI au lieu de Gradio :

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Génération simple
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful landscape", "num_inference_steps": 25}'
```

---

## 📊 Résumé de l'Ordre

| Étape | Action | Durée | Obligatoire |
|-------|--------|-------|-------------|
| **1** | Installation dépendances | 10-30 min | ✅ Oui |
| **2** | Test Stable Diffusion | 30s-5min | ✅ Oui |
| **3** | Entraînement RL Agent | 1-2h (Colab) | ✅ Oui |
| **4** | Test Agent RL | 2-5 min | ⚠️ Recommandé |
| **5** | Lancement API | Instantané | ✅ Oui |
| **6** | Test API | 2 min | ⚠️ Recommandé |

---

## 🔄 Workflow Recommandé par Sprint

### Sprint 1 : GenAI (Développement Local)

```bash
# 1. Installation
pip install -r requirements.txt
cp env.example .env

# 2. Test Stable Diffusion
python -c "from app.models.stable_diffusion import sd_generator; \
           image = sd_generator.generate(prompt='test', num_inference_steps=25); \
           image.save('test.png')"

# 3. Lancement API
python -m app.main

# 4. Test API (sans RL)
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a landscape"}'
```

**Pas besoin d'agent RL pour Sprint 1**

---

### Sprint 2 : RL Agent (Entraînement Colab)

1. **Sur Colab** : Entraîner l'agent (`notebooks/colab_train_rl.ipynb`)
2. **Télécharger** : `models/rl_agent.zip`
3. **Placer** : Dans `models/rl_agent.zip` du projet local
4. **Tester** : `python training/evaluate_agent.py --prompt "test"`

---

### Sprint 3-4 : Déploiement (Local)

```bash
# 1. Vérifier que le modèle RL existe
ls -lh models/rl_agent.zip

# 2. Lancer l'API (avec modèle RL pré-entraîné)
python -m app.main

# 3. Test complet avec RL
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cat", "use_rl_optimization": true}'

# 4. Docker (optionnel)
docker build -t ai-creative-studio .
docker run -p 8000:8000 ai-creative-studio
```

---

## ⚠️ Erreurs Courantes

### Problème : Modèle Stable Diffusion non trouvé

**Solution** :
```bash
# Vérifier que le cache Hugging Face existe
# Le modèle sera téléchargé automatiquement au premier usage
# Cache: ~/.cache/huggingface/hub/
```

### Problème : Agent RL non trouvé

**Solution** :
```bash
# Vérifier que le modèle existe
ls -lh models/rl_agent.zip

# Si absent, entraîner d'abord (Étape 3)
# ou télécharger depuis Colab
```

### Problème : Out of Memory

**Solution** :
```bash
# Dans .env:
SD_DEVICE=cpu
SD_DTYPE=float32

# Ou réduire la résolution:
width=384
height=384
```

### Problème : API ne démarre pas

**Solution** :
```bash
# Vérifier que le port 8000 n'est pas utilisé
# Windows:
netstat -ano | findstr :8000
# Linux/Mac:
lsof -i :8000

# Utiliser un autre port:
uvicorn app.main:app --port 8001
```

---

## ✅ Checklist de Démarrage

- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichier `.env` créé depuis `env.example`
- [ ] Stable Diffusion testé et fonctionnel
- [ ] Agent RL entraîné (`models/rl_agent.zip` existe)
- [ ] Agent RL testé et fonctionnel
- [ ] API lancée et accessible sur `http://localhost:8000`
- [ ] Tests API réussis (health, generate, optimize)

---

## 📚 Ressources

- **Guide workflow hybride** : `WORKFLOW_HYBRIDE.md`
- **Documentation API** : `http://localhost:8000/docs`
- **README principal** : `README.md`

---

**🎯 Une fois toutes les étapes complétées, votre projet est prêt ! 🚀**


# 🤖 Guide : Entraîner l'Agent RL sur Google Colab

Guide étape par étape pour entraîner votre agent RL sur Google Colab avec GPU gratuit.

## 🎯 Pourquoi Google Colab ?

- ✅ **GPU gratuit** (T4 ou V100) - 20-40x plus rapide que CPU
- ✅ **Pas d'installation** - Tout fonctionne dans le navigateur
- ✅ **1-2 heures** pour 10k steps (vs 20-40h sur CPU local)

---

## 📋 Étapes Détaillées

### Étape 1 : Préparer votre projet sur GitHub

**⚠️ IMPORTANT** : Votre projet doit être sur GitHub pour que Colab puisse le cloner.

1. **Créer un repository GitHub** (si pas déjà fait)
   - Aller sur [GitHub](https://github.com)
   - Créer un nouveau repository
   - Uploader votre code

2. **Noter l'URL du repository**
   - Exemple : `https://github.com/votre-username/votre-repo.git`

---

### Étape 2 : Ouvrir Google Colab

1. Aller sur [Google Colab](https://colab.research.google.com/)
2. Se connecter avec votre compte Google
3. Cliquer sur **"Nouveau notebook"** ou **"File > New notebook"**

---

### Étape 3 : Uploader le notebook

**Option A : Depuis votre ordinateur**
1. Dans Colab : **File > Upload notebook**
2. Sélectionner `notebooks/colab_train_rl.ipynb` de votre projet local

**Option B : Créer un nouveau notebook**
1. Créer un nouveau notebook dans Colab
2. Copier-coller le contenu des cellules (voir ci-dessous)

---

### Étape 4 : Activer le GPU

**⚠️ CRUCIAL** : Sans GPU, l'entraînement sera très lent !

1. Dans Colab : **Runtime > Change runtime type**
2. Sélectionner :
   - **Hardware accelerator** : **GPU**
   - **GPU type** : **T4** (gratuit) ou **V100** (si disponible)
3. Cliquer sur **"Save"**

---

### Étape 5 : Exécuter les cellules du notebook

Le notebook `colab_train_rl.ipynb` contient toutes les étapes. Exécutez-les dans l'ordre :

#### Cellule 1 : Installation des dépendances

```python
# Installation PyTorch avec CUDA 11.8 (pour GPU Colab)
%pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118 -q

# Dépendances principales pour RL
%pip install diffusers transformers accelerate -q
%pip install stable-baselines3[extra] gymnasium -q
%pip install pillow numpy requests pydantic pydantic-settings -q

print("✅ Dépendances installées")
```

**⏱️ Temps** : 2-5 minutes

#### Cellule 2 : Cloner votre repository

```python
# ⚠️ MODIFIER CETTE URL avec votre repository GitHub
REPO_URL = "https://github.com/VOTRE-USERNAME/VOTRE-REPO.git"

import os

# Cloner le repo
if not os.path.exists("Projet_fil_rouge_ML_DL"):
    !git clone {REPO_URL}

%cd Projet_fil_rouge_ML_DL

# Configuration pour Colab (GPU)
os.environ["SD_DEVICE"] = "cuda"
os.environ["SD_DTYPE"] = "float16"
os.environ["OUTPUT_DIR"] = "outputs"
os.environ["MODELS_DIR"] = "models"
os.environ["RL_AGENT_PATH"] = "models/rl_agent.zip"

print("✅ Projet configuré")
```

**⚠️ IMPORTANT** : Remplacer `REPO_URL` par l'URL de votre repository GitHub !

**⏱️ Temps** : 30 secondes

#### Cellule 3 : Vérifier le GPU

```python
!nvidia-smi

import torch
print(f"✅ PyTorch version: {torch.__version__}")
print(f"✅ CUDA disponible: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
    print(f"✅ Mémoire GPU: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
else:
    print("\n❌ ERREUR: Aucun GPU détecté!")
```

**✅ Vérification** : Vous devriez voir "CUDA disponible: True" et le nom du GPU

#### Cellule 4 : Entraîner l'agent RL

```python
# Configuration de l'entraînement
TOTAL_TIMESTEPS = 10000  # Ajustez selon vos besoins
SAVE_PATH = "models/rl_agent.zip"

print(f"🚀 Démarrage entraînement RL agent...")
print(f"📊 Steps d'entraînement: {TOTAL_TIMESTEPS}")
print(f"⏱️ Temps estimé: {TOTAL_TIMESTEPS // 5000:.1f}-{TOTAL_TIMESTEPS // 2500:.1f} heures")
print("\n" + "="*50 + "\n")

# Importer les modules
from app.models.rl_agent import RLOptimizer
from training.rl_env import PromptOptimizationEnv

# Créer environnement et agent
env = PromptOptimizationEnv()
agent = RLOptimizer(env=env)

# Entraîner l'agent
agent.train(
    total_timesteps=TOTAL_TIMESTEPS,
    save_path=SAVE_PATH
)

print("\n" + "="*50)
print("✅ Entraînement terminé !")
print(f"📦 Modèle sauvegardé: {SAVE_PATH}")
```

**⏱️ Temps** : 
- **10k steps** : ~1-2 heures
- **20k steps** : ~2-4 heures

**💡 Astuce** : Commencez avec 1000-2000 steps pour tester rapidement, puis augmentez.

#### Cellule 5 : Vérifier le modèle

```python
import os
model_path = "models/rl_agent.zip"

if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"✅ Modèle trouvé: {model_path}")
    print(f"📦 Taille: {size_mb:.2f} MB")
else:
    print(f"❌ ERREUR: Modèle non trouvé")
```

#### Cellule 6 : Télécharger le modèle

**Option A : Téléchargement direct**

```python
from google.colab import files

model_path = "models/rl_agent.zip"
if os.path.exists(model_path):
    print(f"📥 Téléchargement de {model_path}...")
    files.download(model_path)
    print("✅ Téléchargement terminé !")
    print("\n💡 Placez le fichier dans le dossier 'models/' de votre projet local")
else:
    print(f"❌ Modèle non trouvé: {model_path}")
```

**Option B : Sauvegarder dans Google Drive**

```python
from google.colab import drive
drive.mount('/content/drive')

# Créer dossier de sauvegarde
DRIVE_MODELS_DIR = "/content/drive/MyDrive/ai-creative-studio/models"
os.makedirs(DRIVE_MODELS_DIR, exist_ok=True)

# Copier le modèle vers Drive
!cp models/rl_agent.zip {DRIVE_MODELS_DIR}/rl_agent.zip

print(f"✅ Modèle sauvegardé dans Google Drive")
print(f"📦 Chemin: {DRIVE_MODELS_DIR}/rl_agent.zip")
```

---

## 📥 Étape 6 : Récupérer le modèle localement

### Option A : Téléchargement direct depuis Colab

1. Exécuter la cellule de téléchargement
2. Le fichier `rl_agent.zip` sera téléchargé automatiquement
3. Placer le fichier dans `models/rl_agent.zip` de votre projet local

### Option B : Depuis Google Drive

1. Aller sur [Google Drive](https://drive.google.com)
2. Naviguer vers `ai-creative-studio/models/`
3. Télécharger `rl_agent.zip`
4. Placer dans `models/rl_agent.zip` de votre projet local

---

## ✅ Étape 7 : Vérifier localement

```bash
# Vérifier que le modèle existe
ls -lh models/rl_agent.zip

# Le fichier devrait faire ~10-50 MB
```

---

## 🧪 Test rapide (optionnel sur Colab)

Avant de télécharger, vous pouvez tester le modèle :

```python
# Test rapide d'optimisation
test_prompt = "a cat"

result = agent.optimize_prompt(
    base_prompt=test_prompt,
    n_iterations=5
)

print(f"Prompt original: {result['original_prompt']}")
print(f"Prompt optimisé: {result['optimized_prompt']}")
print(f"Amélioration: {result['improvement']:+.2f}")
```

---

## ⚠️ Points d'Attention

### 1. Session Colab limitée

- **Gratuit** : 12 heures max par session
- **Colab Pro** : 24 heures max
- **Solution** : Sauvegarder régulièrement dans Drive

### 2. GPU indisponible

Parfois pas de GPU disponible :
- Attendre quelques minutes
- Réessayer plus tard
- Utiliser Colab Pro (plus de GPU disponibles)

### 3. Interruption de session

Si la session s'interrompt :
- Les checkpoints sont sauvegardés dans `models/checkpoints/`
- Vous pouvez reprendre l'entraînement depuis un checkpoint
- Le modèle final est dans `models/rl_agent.zip`

### 4. Taille du modèle

Le modèle fait ~10-50 MB, facilement téléchargeable.

---

## 📊 Paramètres d'Entraînement Recommandés

| Objectif | Steps | Temps estimé | Qualité |
|---------|-------|--------------|---------|
| **Test rapide** | 1,000 | ~10-15 min | Basique |
| **Minimum viable** | 5,000 | ~30-60 min | Acceptable |
| **Recommandé** | 10,000 | ~1-2 heures | Bon |
| **Optimal** | 20,000 | ~2-4 heures | Excellent |

**💡 Pour le projet** : 10,000 steps est un bon compromis.

---

## 🔄 Reprendre un Entraînement

Si l'entraînement est interrompu, vous pouvez reprendre :

```python
# Charger depuis un checkpoint
from stable_baselines3 import PPO
from training.rl_env import PromptOptimizationEnv

env = PromptOptimizationEnv()
# Charger le dernier checkpoint
agent.model = PPO.load("models/checkpoints/ppo_prompt_opt_5000_steps.zip", env=env)

# Continuer l'entraînement
agent.train(total_timesteps=5000, save_path="models/rl_agent.zip")
```

---

## 📝 Checklist Complète

### Avant de commencer
- [ ] Projet uploadé sur GitHub
- [ ] URL du repository notée
- [ ] Notebook Colab ouvert
- [ ] GPU activé dans Colab

### Pendant l'entraînement
- [ ] Dépendances installées
- [ ] Repository cloné
- [ ] GPU vérifié
- [ ] Entraînement lancé
- [ ] Progression surveillée

### Après l'entraînement
- [ ] Modèle vérifié (taille ~10-50 MB)
- [ ] Modèle téléchargé ou sauvegardé dans Drive
- [ ] Modèle placé dans `models/rl_agent.zip` localement
- [ ] Testé localement

---

## 🆘 Dépannage

### Problème : "No module named 'app'"

**Solution** : Vérifier que vous êtes dans le bon répertoire
```python
%cd Projet_fil_rouge_ML_DL
import os
print(os.getcwd())  # Devrait afficher .../Projet_fil_rouge_ML_DL
```

### Problème : GPU non disponible

**Solution** :
1. Attendre quelques minutes
2. Réessayer
3. Utiliser Colab Pro

### Problème : Out of Memory

**Solution** : Réduire les paramètres d'entraînement
```python
# Dans training/rl_env.py ou agent, réduire batch_size
agent.model = PPO(
    "MlpPolicy",
    env,
    batch_size=32,  # Au lieu de 64
    n_steps=1024,   # Au lieu de 2048
)
```

### Problème : Entraînement très lent

**Vérifier** :
- GPU activé : `Runtime > Change runtime type > GPU`
- CUDA disponible : `torch.cuda.is_available()` doit être `True`

---

## 📚 Ressources

- **Notebook Colab** : `notebooks/colab_train_rl.ipynb`
- **Workflow hybride** : `WORKFLOW_HYBRIDE.md`
- **Documentation Stable-Baselines3** : https://stable-baselines3.readthedocs.io/

---

**🎯 Une fois le modèle téléchargé, vous pouvez l'utiliser localement dans votre API ou interface Gradio !**


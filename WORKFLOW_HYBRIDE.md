# 🔄 Workflow Hybride : Entraînement Colab + Exécution Locale

Guide pour **entraîner l'agent RL sur Google Colab** et **utiliser le modèle localement**.

## 🎯 Stratégie

1. **Entraînement RL** : Google Colab (GPU gratuit, rapide)
2. **Téléchargement modèle** : Depuis Colab vers local
3. **Exécution API** : Localement avec modèle pré-entraîné

## 📋 Workflow Complet

### Phase 1 : Entraînement sur Colab (Sprint 2)

#### Étape 1 : Ouvrir le notebook Colab

1. Aller sur [Google Colab](https://colab.research.google.com/)
2. Ouvrir le notebook : `notebooks/colab_train_rl.ipynb`
3. **Activer GPU** : `Runtime > Change runtime type > GPU (T4 ou V100)`

#### Étape 2 : Configurer le repository

Dans le notebook, modifier :
```python
REPO_URL = "https://github.com/VOTRE-USER/VOTRE-REPO.git"
```

#### Étape 3 : Lancer l'entraînement

Exécuter toutes les cellules. L'entraînement prendra :
- **10k steps** : ~1-2 heures
- **20k steps** : ~2-4 heures

#### Étape 4 : Télécharger le modèle

**Option A : Téléchargement direct**
- La dernière cellule du notebook télécharge automatiquement `rl_agent.zip`
- Cliquer sur le fichier téléchargé et le placer dans `models/rl_agent.zip`

**Option B : Google Drive**
- Le modèle est automatiquement sauvegardé dans Drive
- Télécharger depuis `ai-creative-studio/models/rl_agent.zip`

### Phase 2 : Utilisation Locale (Sprints 1, 3, 4)

#### Étape 1 : Placer le modèle

```bash
# Vérifier que le modèle est au bon endroit
ls -lh models/rl_agent.zip

# Le chemin doit correspondre à celui dans .env
# RL_AGENT_PATH=models/rl_agent.zip
```

#### Étape 2 : Configurer le projet local

```bash
# Créer .env
cp env.example .env

# Modifier .env pour CPU (si pas de GPU)
# SD_DEVICE=cpu
# SD_DTYPE=float32
```

#### Étape 3 : Lancer l'API

```bash
# Lancer l'API
python -m app.main

# Ou avec uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Étape 4 : Utiliser le modèle entraîné

L'API chargera automatiquement le modèle depuis `models/rl_agent.zip` si disponible.

```bash
# Génération avec optimisation RL
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful landscape",
    "use_rl_optimization": true
  }'
```

## 📊 Comparaison Temps d'Entraînement

| Steps | Colab (GPU) | Local (CPU) |
|-------|-------------|-------------|
| 1k | ~10-15 min | ~2-4 heures |
| 10k | ~1-2 heures | **20-40 heures** |
| 20k | ~2-4 heures | **40-80 heures** |

**💡 Gain de temps : 20-40x plus rapide sur Colab !**

## 🔄 Workflow Par Sprint

### Sprint 1 : GenAI (Local)
- ✅ Développement local de l'API
- ✅ Tests de génération d'images
- ✅ Pas besoin de modèle RL encore

### Sprint 2 : RL Agent (Colab)
- ✅ Entraînement sur Colab (`colab_train_rl.ipynb`)
- ✅ Téléchargement du modèle
- ✅ Test rapide sur Colab (optionnel)

### Sprint 3 : Déploiement (Local)
- ✅ Utilisation du modèle pré-entraîné
- ✅ API locale avec Docker
- ✅ Démonstration

### Sprint 4 : Finalisation (Local)
- ✅ Utilisation du modèle dans l'API
- ✅ Portfolio de générations
- ✅ Présentation

## 📁 Structure des Fichiers

```
Projet_fil_rouge_ML_DL/
├── models/
│   ├── rl_agent.zip          # ← Modèle téléchargé depuis Colab
│   └── checkpoints/          # Checkpoints d'entraînement (optionnel)
├── notebooks/
│   └── colab_train_rl.ipynb  # ← Notebook pour entraînement Colab
├── app/
│   └── models/
│       └── rl_agent.py       # Charge le modèle depuis models/rl_agent.zip
└── .env                      # RL_AGENT_PATH=models/rl_agent.zip
```

## ✅ Checklist

### Avant Entraînement Colab
- [ ] Notebook `colab_train_rl.ipynb` prêt
- [ ] GPU activé dans Colab
- [ ] Repository GitHub clonable (ou code uploadé)
- [ ] ~2-4 heures disponibles pour l'entraînement

### Après Entraînement Colab
- [ ] Modèle `rl_agent.zip` téléchargé
- [ ] Modèle placé dans `models/rl_agent.zip` localement
- [ ] Taille du modèle vérifiée (~10-50 MB)
- [ ] Modèle sauvegardé dans Drive (backup)

### Avant Utilisation Locale
- [ ] Fichier `.env` configuré
- [ ] `RL_AGENT_PATH=models/rl_agent.zip` dans `.env`
- [ ] API testée sans optimisation RL
- [ ] Modèle testé avec optimisation RL

## 🔧 Dépannage

### Problème : Modèle non trouvé localement

**Vérifier le chemin** :
```bash
# Vérifier que le fichier existe
ls -lh models/rl_agent.zip

# Vérifier le chemin dans .env
cat .env | grep RL_AGENT_PATH
```

### Problème : Erreur lors du chargement

**Vérifier la compatibilité** :
- Le modèle doit être entraîné avec la même version de stable-baselines3
- Vérifier dans `requirements.txt` : `stable-baselines3==2.2.1`

### Problème : Modèle trop gros pour Drive

**Compression** :
```python
# Dans Colab, compresser avant upload
import zipfile
import os

model_path = "models/rl_agent.zip"
if os.path.exists(model_path):
    # Vérifier taille
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"Taille: {size_mb:.2f} MB")
    
    # Si > 100 MB, considérer utiliser GitHub Releases ou Drive Pro
```

## 💡 Astuces

1. **Backup multiple** : Sauvegarder dans Drive ET télécharger directement
2. **Versioning** : Nommer le modèle avec timestamp : `rl_agent_20250119.zip`
3. **Checkpoints** : Sauvegarder aussi les checkpoints intermédiaires
4. **Tests** : Tester le modèle sur Colab avant téléchargement

## 📚 Ressources

- **Notebook Colab** : `notebooks/colab_train_rl.ipynb`
- **Code Agent RL** : `app/models/rl_agent.py`
- **Configuration** : `.env` et `env.example`

---

**🎯 Résultat : Entraînement rapide sur Colab + Exécution locale confortable !**


# 📤 Guide : Upload du Projet sur GitHub pour Colab

Guide pour préparer votre projet pour l'entraînement RL sur Google Colab.

## 🎯 Ce qu'il faut uploader sur GitHub

### ✅ **TOUT LE PROJET** (pas seulement le notebook)

Le notebook Colab a besoin de **tout le code du projet** pour fonctionner car il importe :
- `app.models.rl_agent` → Nécessite `app/`
- `training.rl_env` → Nécessite `training/`
- `app.models.stable_diffusion` → Nécessite `app/models/`
- etc.

---

## 📁 Structure à uploader sur GitHub

```
Projet_fil_rouge_ML_DL/
├── README.md                    ✅ À uploader
├── requirements.txt             ✅ À uploader
├── Dockerfile                   ✅ À uploader
├── docker-compose.yml           ✅ À uploader
├── env.example                  ✅ À uploader
├── .gitignore                   ✅ À uploader
│
├── app/                         ✅ TOUT LE DOSSIER
│   ├── __init__.py
│   ├── main.py
│   ├── gradio_ui.py
│   ├── models/
│   │   ├── stable_diffusion.py
│   │   ├── rl_agent.py
│   │   └── aesthetic_scorer.py
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── database/
│   │   ├── models.py
│   │   ├── database.py
│   │   └── repository.py
│   └── utils/
│       ├── config.py
│       └── helpers.py
│
├── training/                    ✅ TOUT LE DOSSIER
│   ├── train_rl_agent.py
│   ├── evaluate_agent.py
│   └── rl_env.py
│
├── notebooks/                   ✅ Le notebook Colab
│   └── colab_train_rl.ipynb
│
├── tests/                       ✅ Tests (optionnel)
│   ├── test_api.py
│   └── test_models.py
│
├── models/                      ⚠️ Dossier vide (créé automatiquement)
├── outputs/                     ⚠️ Dossier vide
└── data/                        ⚠️ Dossier vide
```

---

## ⚠️ Fichiers à NE PAS uploader

Ces fichiers sont dans `.gitignore` et ne doivent **pas** être sur GitHub :

```
❌ .env                    (variables d'environnement personnelles)
❌ .venv/                  (environnement virtuel)
❌ __pycache__/           (cache Python)
❌ outputs/**/*.png       (images générées)
❌ models/*.zip           (modèles entraînés - trop gros)
❌ models/*.pt            (modèles - trop gros)
❌ data/*.db              (base de données SQLite)
❌ test.png               (fichiers de test locaux)
```

---

## 📋 Étapes pour uploader sur GitHub

### Option 1 : Depuis votre ordinateur (Recommandé)

#### 1. Créer le repository sur GitHub

1. Aller sur [GitHub](https://github.com)
2. Cliquer sur **"New repository"** (ou **"+"** > **"New repository"**)
3. Nommer le repository : `Projet_fil_rouge_ML_DL` (ou autre nom)
4. **Ne pas** cocher "Initialize with README" (déjà présent)
5. Cliquer sur **"Create repository"**

#### 2. Initialiser Git localement

```bash
# Dans le dossier de votre projet
cd C:\Users\hasso\Projet_fil_rouge_ML_DL

# Initialiser Git
git init

# Vérifier que .gitignore existe
cat .gitignore

# Ajouter tous les fichiers (sauf ceux dans .gitignore)
git add .

# Premier commit
git commit -m "Initial commit: AI Creative Studio project"

# Lier avec GitHub (remplacer par votre URL)
git remote add origin https://github.com/VOTRE-USERNAME/VOTRE-REPO.git

# Push sur GitHub
git branch -M main
git push -u origin main
```

#### 3. Vérifier sur GitHub

1. Aller sur votre repository GitHub
2. Vérifier que tous les fichiers sont présents :
   - ✅ `app/` avec tous les sous-dossiers
   - ✅ `training/` avec les fichiers Python
   - ✅ `notebooks/colab_train_rl.ipynb`
   - ✅ `requirements.txt`, `README.md`, etc.

---

### Option 2 : Via GitHub Desktop (Plus facile)

1. Télécharger [GitHub Desktop](https://desktop.github.com/)
2. Se connecter avec votre compte GitHub
3. **File > Add Local Repository**
4. Sélectionner votre dossier `Projet_fil_rouge_ML_DL`
5. **Publish repository** ou **Push origin**
6. Tous les fichiers seront uploadés automatiquement (sauf ceux dans `.gitignore`)

---

## 🔍 Vérification : Que doit contenir le repository GitHub ?

### ✅ Fichiers essentiels présents :

```
✅ app/
   ✅ models/
      ✅ stable_diffusion.py
      ✅ rl_agent.py
      ✅ aesthetic_scorer.py
   ✅ api/
      ✅ routes.py
      ✅ schemas.py
   ✅ database/
      ✅ models.py
      ✅ database.py
      ✅ repository.py
   ✅ utils/
      ✅ config.py
      ✅ helpers.py

✅ training/
   ✅ rl_env.py
   ✅ train_rl_agent.py
   ✅ evaluate_agent.py

✅ notebooks/
   ✅ colab_train_rl.ipynb

✅ requirements.txt
✅ README.md
✅ .gitignore
```

### ❌ Fichiers qui NE doivent PAS être présents :

```
❌ .env
❌ .venv/
❌ __pycache__/
❌ outputs/*.png
❌ models/*.zip
❌ data/*.db
❌ test.png
```

---

## 🎯 Pourquoi tout le projet ?

Le notebook Colab fait ceci :

```python
# Cloner le repository
!git clone https://github.com/votre-user/votre-repo.git

# Aller dans le dossier
%cd Projet_fil_rouge_ML_DL

# Importer les modules de votre projet
from app.models.rl_agent import RLOptimizer      # Besoin de app/models/rl_agent.py
from training.rl_env import PromptOptimizationEnv  # Besoin de training/rl_env.py
```

**Si vous n'uploadez que le notebook**, ces imports échoueront car le code n'existera pas !

---

## ✅ Checklist avant de push sur GitHub

- [ ] Tous les fichiers Python dans `app/` sont présents
- [ ] Tous les fichiers Python dans `training/` sont présents
- [ ] Le notebook `notebooks/colab_train_rl.ipynb` est présent
- [ ] `requirements.txt` est présent
- [ ] `.gitignore` est présent
- [ ] Pas de fichiers `.env` (devrait être ignoré)
- [ ] Pas de dossiers `__pycache__/` (ignorés automatiquement)
- [ ] Pas d'images dans `outputs/` (devrait être ignoré)
- [ ] Pas de modèles `.zip` dans `models/` (devrait être ignoré)

---

## 🚀 Après l'upload sur GitHub

1. **Copier l'URL du repository** :
   - Exemple : `https://github.com/votre-username/votre-repo.git`

2. **Dans le notebook Colab** :
   - Modifier la cellule avec `REPO_URL = "..."` 
   - Coller votre URL GitHub

3. **Exécuter le notebook** :
   - Colab clonera automatiquement tout le projet
   - Les imports fonctionneront car tout le code sera là

---

## 📝 Résumé

**✅ À UPLOADER** : Tout le projet (code source, notebooks, configs)

**❌ À NE PAS UPLOADER** : 
- Fichiers personnels (`.env`)
- Cache Python (`__pycache__/`)
- Modèles entraînés (`models/*.zip`) - trop gros
- Images générées (`outputs/*.png`)
- Base de données (`data/*.db`)

**💡 Le `.gitignore` s'occupe automatiquement d'exclure les fichiers à ne pas uploader.**


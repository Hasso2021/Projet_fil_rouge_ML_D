# 📥 Récupération des modèles RL depuis RunPod

## 🎯 Problème

Vous avez entraîné votre modèle RL sur RunPod, mais les fichiers sont encore sur le serveur cloud et pas sur votre machine locale.

## ✅ Solution en 3 étapes

### Étape 1 : Vérifier les modèles sur RunPod

Dans votre Jupyter Notebook RunPod (`https://9vhfnmz7qaqzg8-8888.proxy.runpod.net`), créez une nouvelle cellule :

```python
import os

print("=== 📂 Vérification des modèles ===\n")

# Vérifier le modèle principal
if os.path.exists("models/rl_agent.zip"):
    size_mb = os.path.getsize("models/rl_agent.zip") / (1024 * 1024)
    print(f"✅ Modèle principal : models/rl_agent.zip ({size_mb:.2f} MB)")
else:
    print("❌ models/rl_agent.zip introuvable")

# Vérifier les checkpoints
if os.path.exists("models/checkpoints/"):
    checkpoints = [f for f in os.listdir("models/checkpoints/") if f.endswith(".zip")]
    if checkpoints:
        print(f"\n✅ {len(checkpoints)} checkpoint(s) trouvé(s) :")
        for cp in sorted(checkpoints):
            size_mb = os.path.getsize(f"models/checkpoints/{cp}") / (1024 * 1024)
            print(f"   - {cp} ({size_mb:.2f} MB)")
    else:
        print("\n⚠️ Aucun checkpoint trouvé")
else:
    print("\n❌ Dossier models/checkpoints/ introuvable")

# Vérifier l'espace disque
print("\n=== 💾 Espace disque ===")
stat = os.statvfs(".")
free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
print(f"Espace libre : {free_gb:.2f} GB")
```

**Résultat attendu** :
```
✅ Modèle principal : models/rl_agent.zip (250.45 MB)
✅ 3 checkpoint(s) trouvé(s) :
   - ppo_prompt_opt_1000_steps.zip (245.12 MB)
   - ppo_prompt_opt_2000_steps.zip (246.89 MB)
   - ppo_prompt_opt_3000_steps.zip (247.34 MB)
```

---

### Étape 2 : Créer une archive téléchargeable

#### Option A : Archive complète (RECOMMANDÉ)

```python
import shutil
from datetime import datetime

# Créer un nom unique avec timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
archive_name = f"rl_models_{timestamp}"

print(f"📦 Création de l'archive {archive_name}.zip...")

# Créer l'archive de tout le dossier models/
shutil.make_archive(archive_name, 'zip', 'models/')

# Afficher le résultat
if os.path.exists(f"{archive_name}.zip"):
    size_mb = os.path.getsize(f"{archive_name}.zip") / (1024 * 1024)
    print(f"✅ Archive créée : {archive_name}.zip ({size_mb:.2f} MB)")
    print(f"\n📥 Pour télécharger :")
    print(f"   1. Rafraîchir le navigateur de fichiers Jupyter")
    print(f"   2. Clic droit sur '{archive_name}.zip'")
    print(f"   3. Sélectionner 'Download'")
else:
    print("❌ Erreur lors de la création de l'archive")
```

#### Option B : Modèle principal seulement (Plus rapide)

```python
import shutil
import os

# Copier le modèle principal dans le répertoire racine pour faciliter le téléchargement
if os.path.exists("models/rl_agent.zip"):
    shutil.copy("models/rl_agent.zip", "rl_agent_trained.zip")
    size_mb = os.path.getsize("rl_agent_trained.zip") / (1024 * 1024)
    print(f"✅ Modèle copié : rl_agent_trained.zip ({size_mb:.2f} MB)")
    print(f"\n📥 Clic droit sur 'rl_agent_trained.zip' → Download")
else:
    print("❌ Modèle principal introuvable")
```

---

### Étape 3 : Télécharger l'archive

1. **Rafraîchir** le navigateur de fichiers Jupyter (bouton refresh en haut)
2. **Trouver** le fichier `rl_models_YYYYMMDD_HHMMSS.zip` ou `rl_agent_trained.zip`
3. **Clic droit** sur le fichier → **Download**
4. **Attendre** le téléchargement (peut prendre quelques minutes selon la taille)

---

### Étape 4 : Installer sur votre machine locale

#### Sur Windows (PowerShell) :

```powershell
# Aller dans le dossier du projet
cd C:\Users\hasso\Projet_fil_rouge_ML_DL

# Créer le dossier models/ s'il n'existe pas
New-Item -ItemType Directory -Force -Path "models"

# Si vous avez téléchargé l'archive complète
Expand-Archive -Path "C:\Users\hasso\Downloads\rl_models_*.zip" -DestinationPath "models\" -Force

# OU si vous avez téléchargé seulement le modèle principal
Copy-Item "C:\Users\hasso\Downloads\rl_agent_trained.zip" -Destination "models\rl_agent.zip"

# Vérifier que le fichier existe
ls models\rl_agent.zip
```

#### Vérification :

```powershell
# Le fichier doit exister et faire ~200-300 MB
Get-Item models\rl_agent.zip | Select-Object Name, Length
```

---

### Étape 5 : Tester le modèle

Lancez le script de test :

```powershell
python test_rl_model.py
```

**Résultat attendu** :
```
============================================================
🧪 TEST DU MODÈLE RL
============================================================
✅ Modèle trouvé : models/rl_agent.zip (245.67 MB)

🔄 Chargement du modèle RL...
OK: Modele RL charge depuis models/rl_agent.zip
✅ Modèle chargé avec succès !

🧪 Test d'optimisation d'un prompt simple...

📊 Résultats de l'optimisation :
   - Prompt original : a cat
   - Prompt optimisé : a cat, professional photography, detailed...
   - Amélioration : +1.23
   - Score original : 5.45
   - Score optimisé : 6.68

✅ Le modèle RL fonctionne correctement !
============================================================
✅ TEST RÉUSSI - Modèle RL prêt à l'emploi !
============================================================
```

---

## 🚀 Activer l'optimisation RL dans Gradio

Une fois le modèle installé, vous pouvez l'activer dans l'interface :

1. Lancez Gradio :
   ```powershell
   python run_gradio.py
   ```

2. Dans l'interface Gradio, cochez la case :
   ```
   ✨ Optimisation automatique du prompt (RL)
   ```

3. Générez une image pour tester !

---

## ⚠️ Dépannage

### "❌ Modèle introuvable"

- Vérifiez que le fichier est bien nommé `rl_agent.zip`
- Vérifiez qu'il est dans le dossier `models/` (pas `models/checkpoints/`)
- Vérifiez les permissions du fichier

### "❌ Erreur lors du chargement"

Le fichier est peut-être corrompu :

```python
# Sur RunPod, vérifier l'intégrité
import zipfile

try:
    with zipfile.ZipFile("models/rl_agent.zip", 'r') as zip_ref:
        print("✅ Archive valide")
        print(f"Fichiers : {len(zip_ref.namelist())}")
except Exception as e:
    print(f"❌ Archive corrompue : {e}")
```

### "Incompatibilité de version"

Si le modèle a été entraîné avec une version différente de stable-baselines3 :

```powershell
# Vérifier la version
pip show stable-baselines3

# Réinstaller si nécessaire
pip install stable-baselines3==2.2.1 --force-reinstall
```

---

## 📊 Alternatives de transfert

### Via GitHub (si < 100 MB)

```bash
# Sur RunPod
git add models/rl_agent.zip
git commit -m "Add trained RL model"
git push origin main

# Sur votre machine locale
git pull origin main
```

**⚠️ Limite GitHub** : 100 MB par fichier

### Via Google Drive

```python
# Sur RunPod (installer d'abord)
!pip install gdown

# Uploader (nécessite authentification Google)
from google.colab import drive
drive.mount('/content/drive')

# Copier vers Drive
!cp models/rl_agent.zip /content/drive/MyDrive/
```

### Via wget/curl (Advanced)

Si vous avez un serveur web personnel :

```python
# Sur RunPod
!curl -X POST -F "file=@models/rl_agent.zip" https://your-server.com/upload
```

---

## 🎯 Checklist finale

- [ ] Modèle vérifié sur RunPod
- [ ] Archive créée et téléchargée
- [ ] Fichier `models/rl_agent.zip` présent localement
- [ ] Test du modèle réussi (`python test_rl_model.py`)
- [ ] Optimisation RL activable dans Gradio

**Une fois tout coché, votre modèle RL est prêt ! 🎉**


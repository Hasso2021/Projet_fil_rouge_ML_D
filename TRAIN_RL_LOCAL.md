# 🚀 Guide : Entraînement RL Local sur CPU

Guide pour entraîner l'agent RL localement sur votre PC (CPU, 16GB RAM).

## ✅ Prérequis

1. **Environnement Python activé** :
   ```powershell
   # Activer l'environnement virtuel
   .venv\Scripts\activate
   ```

2. **Configuration `.env`** :
   Vérifiez que votre fichier `.env` contient :
   ```env
   SD_DEVICE=cpu
   SD_DTYPE=float32
   SD_MODEL_ID=lykon/dreamshaper-8  # ou autre modèle
   ```

3. **Dépendances installées** :
   ```powershell
   pip install -r requirements.txt
   ```

## 🚀 Lancer l'Entraînement

### Option 1 : PowerShell (Recommandé)

```powershell
# Activer l'environnement virtuel
.venv\Scripts\activate

# Définir PYTHONPATH
$env:PYTHONPATH="$PWD"

# Entraînement rapide (2500 steps, ~2-4 heures)
python training/train_rl_agent.py --total_timesteps 2500

# Entraînement complet (5000 steps, ~4-8 heures)
python training/train_rl_agent.py --total_timesteps 5000
```

### Option 2 : Depuis le répertoire racine

```powershell
# Activer l'environnement virtuel
.venv\Scripts\activate

# Lancer avec PYTHONPATH
python -m training.train_rl_agent --total_timesteps 2500
```

### Option 3 : Script batch (Windows)

Créez `train_rl.bat` :
```batch
@echo off
call .venv\Scripts\activate
set PYTHONPATH=%CD%
python training\train_rl_agent.py --total_timesteps 2500
pause
```

## ⚡ Mode Rapide (Fast Mode)

**Activé par défaut** pour CPU - 3-5x plus rapide :

- ✅ Steps SD : 20 (au lieu de 50)
- ✅ n_steps PPO : 512 (au lieu de 2048)
- ✅ Temps estimé : ~2-4 heures pour 2500 steps (CPU)

**Pour désactiver** (meilleure qualité mais plus lent) :
```powershell
python training/train_rl_agent.py --total_timesteps 2500 --no-fast_mode
```

## ⏱️ Temps d'Entraînement Estimés

| Steps | Fast Mode (CPU) | Normal Mode (CPU) |
|-------|-----------------|-------------------|
| 2500  | ~2-4 heures     | ~10-15 heures     |
| 5000  | ~4-8 heures     | ~20-30 heures     |
| 10000 | ~8-16 heures    | ~40-60 heures     |

**💡 Recommandation** : Commencez avec 2500 steps en fast_mode pour tester.

## 🛑 Arrêter/Reprendre l'Entraînement

- **Arrêter** : Appuyez sur `Ctrl+C`
- **Checkpoints** : Sauvegardés automatiquement dans `models/checkpoints/`
- **Reprendre** : Relancez avec les mêmes paramètres (le modèle sera chargé automatiquement)

## 📊 Vérifier le Modèle Entraîné

```powershell
# Vérifier que le modèle existe
Test-Path models/rl_agent.zip

# Tester le modèle
python -m training.evaluate_agent --prompt "a beautiful landscape"
```

## 🔧 Options Disponibles

```powershell
python training/train_rl_agent.py --help
```

**Options principales** :
- `--total_timesteps` : Nombre de steps (défaut: 2500)
- `--save_path` : Chemin de sauvegarde (défaut: models/rl_agent.zip)
- `--fast_mode` : Activer mode rapide (défaut: activé)
- `--no-fast_mode` : Désactiver mode rapide

## ❓ Problèmes Fréquents

### "ModuleNotFoundError: No module named 'app'"

**Solution** : Définir PYTHONPATH :
```powershell
$env:PYTHONPATH="$PWD"
```

### L'entraînement est trop lent

**Solution** : Vérifiez que fast_mode est activé :
```powershell
python training/train_rl_agent.py --total_timesteps 2500 --fast_mode
```

### Out of Memory

**Solution** : 
1. Réduisez `--total_timesteps` (commencez avec 1000)
2. Fermez les autres applications
3. Vérifiez que `SD_DEVICE=cpu` dans `.env`

## 🎯 Exemple Complet

```powershell
# 1. Activer l'environnement
.venv\Scripts\activate

# 2. Vérifier la configuration
cat .env | Select-String "SD_DEVICE"

# 3. Lancer l'entraînement
$env:PYTHONPATH="$PWD"
python training/train_rl_agent.py --total_timesteps 2500

# 4. Vérifier le résultat
Test-Path models/rl_agent.zip
```

## 📝 Notes

- ⏱️ **L'entraînement sur CPU est lent mais fonctionne** - prévoyez plusieurs heures
- 💾 **Les checkpoints sont sauvegardés** toutes les 1000 steps automatiquement
- 🔄 **Vous pouvez interrompre et reprendre** à tout moment
- 🎨 **Fast mode réduit légèrement la qualité** mais accélère significativement


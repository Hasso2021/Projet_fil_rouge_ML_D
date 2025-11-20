# 🚀 Modèles Stable Diffusion Puissants

Guide des modèles Stable Diffusion les plus performants disponibles.

## 🏆 Top Modèles Recommandés

### 1. **DreamShaper 8** ⭐ RECOMMANDÉ
- **ID** : `lykon/dreamshaper-8`
- **Taille** : ~4 GB
- **Avantages** :
  - 🎨 Excellent pour l'art et les styles artistiques
  - ✅ Compatible SD 1.5 (même taille que le modèle de base)
  - ✅ Qualité supérieure au modèle standard
  - ✅ Styles variés (réaliste, fantastique, concept art)
- **Configuration** : 
  ```
  SD_MODEL_ID=lykon/dreamshaper-8
  ```

### 2. **Realistic Vision V5.1**
- **ID** : `SG161222/Realistic_Vision_V5.1_noVAE`
- **Taille** : ~4 GB
- **Avantages** :
  - 📸 Excellent pour art photoréaliste
  - ✅ Détails très fins
  - ✅ Peau et textures naturelles
  - ✅ Portraits réalistes
- **Configuration** :
  ```
  SD_MODEL_ID=SG161222/Realistic_Vision_V5.1_noVAE
  ```

### 3. **Deliberate V3**
- **ID** : `XpucT/Deliberate-v3`
- **Taille** : ~4 GB
- **Avantages** :
  - 🎨 Très polyvalent
  - ✅ Bon compromis qualité/style
  - ✅ Large gamme de styles
- **Configuration** :
  ```
  SD_MODEL_ID=XpucT/Deliberate-v3
  ```

### 4. **Stable Diffusion XL (SDXL)** ⚠️ Nécessite plus de RAM
- **ID** : `stabilityai/stable-diffusion-xl-base-1.0`
- **Taille** : ~13 GB
- **Avantages** :
  - 🔥 LE PLUS PUISSANT
  - ✅ Résolution native 1024x1024 (au lieu de 512x512)
  - ✅ Qualité exceptionnelle
  - ✅ Meilleure compréhension des prompts
- **Inconvénients** :
  - ⚠️ Nécessite beaucoup plus de RAM (~16GB+)
  - ⚠️ Plus lent sur CPU
  - ⚠️ Nécessite modifications du code (dimensions différentes)
- **Configuration** :
  ```
  SD_MODEL_ID=stabilityai/stable-diffusion-xl-base-1.0
  # Note: Nécessite adapter le code pour dimensions 1024x1024
  ```

## 📊 Comparaison Rapide

| Modèle | Qualité | Vitesse | RAM | Recommandé Pour |
|--------|---------|---------|-----|-----------------|
| **DreamShaper 8** | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | 8GB+ | Art général |
| **Realistic Vision** | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | 8GB+ | Art réaliste |
| **Deliberate V3** | ⭐⭐⭐⭐ | ⚡⚡⚡ | 8GB+ | Polyvalent |
| **SDXL** | ⭐⭐⭐⭐⭐ | ⚡⚡ | 16GB+ | Qualité maximale |
| **SD v1.5** (actuel) | ⭐⭐⭐ | ⚡⚡⚡ | 8GB+ | Standard |

## 🔧 Comment Changer de Modèle

### Option 1 : Modifier le fichier `.env`

1. **Ouvrir le fichier** :
   ```powershell
   notepad .env
   ```

2. **Changer la ligne** :
   ```env
   SD_MODEL_ID=lykon/dreamshaper-8
   ```

3. **Sauvegarder** et redémarrer l'application

### Option 2 : Via PowerShell

```powershell
# Remplacer le modèle dans .env
(Get-Content .env) -replace 'SD_MODEL_ID=.*', 'SD_MODEL_ID=lykon/dreamshaper-8' | Set-Content .env

# Vérifier
Get-Content .env | Select-String "SD_MODEL_ID"
```

## ⚠️ Notes Importantes

### Pour CPU (votre configuration actuelle)
- ✅ **DreamShaper 8** : Compatible, meilleur choix
- ✅ **Realistic Vision** : Compatible
- ⚠️ **SDXL** : Peut être trop lent/consommateur sur CPU

### Premier Chargement
- Le modèle sera **téléchargé automatiquement** depuis Hugging Face (~4-13 GB)
- Temps de téléchargement : 5-20 minutes selon votre connexion
- Le modèle est mis en cache ensuite (pas de re-téléchargement)

### Après Changement de Modèle
- Redémarrer l'application (Gradio ou API)
- Le nouveau modèle sera chargé automatiquement

## 🎯 Recommandation

**Pour votre système (CPU, 16GB RAM)** :
- **Meilleur choix** : `lykon/dreamshaper-8`
  - Excellent rapport qualité/vitesse
  - Compatible avec votre configuration
  - Qualité nettement supérieure au modèle de base

## 📚 Ressources

- [Hugging Face Models](https://huggingface.co/models?library=diffusers)
- [Civitai Models](https://civitai.com/models?types=CHECKPOINT)


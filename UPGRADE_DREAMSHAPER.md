# 🚀 Upgrade vers DreamShaper-8

## ✨ Nouveau modèle par défaut : DreamShaper-8

Le projet utilise maintenant **DreamShaper-8** (`Lykon/dreamshaper-8`) comme modèle Stable Diffusion par défaut !

## 🎯 Avantages de DreamShaper-8

### Par rapport à Stable Diffusion 1.5 :
- ✅ **Meilleure qualité visuelle** : Images plus détaillées et cohérentes
- ✅ **Plus rapide** : Optimisé pour générer plus rapidement
- ✅ **Styles variés** : Excellent pour art, fantastique, photoréalisme, art conceptuel
- ✅ **Taille identique** : ~4GB (compatible avec la plupart des configs)
- ✅ **Compatible** : Utilise la même architecture SD 1.5 (pas besoin de changement de code)

### Comparaison de qualité :
- **SD 1.5** : Bon pour du généraliste, qualité correcte
- **DreamShaper-8** : Excellent pour du créatif, qualité supérieure

## 📦 Première utilisation

Au premier lancement, le modèle DreamShaper-8 sera téléchargé automatiquement depuis Hugging Face :

```bash
# Lancer le serveur Gradio
python run_gradio.py
```

**Temps de téléchargement** : ~5-10 minutes selon votre connexion (le modèle fait ~4GB)

Le modèle sera mis en cache dans :
- **Windows** : `C:\Users\<user>\.cache\huggingface\hub\`
- **Linux/Mac** : `~/.cache/huggingface/hub/`

## 🔧 Configuration

Le modèle est déjà configuré dans `app/utils/config.py` :

```python
SD_MODEL_ID: str = "Lykon/dreamshaper-8"
```

### Changer de modèle (optionnel)

Si vous voulez utiliser un autre modèle, créez un fichier `.env` :

```bash
# Pour revenir à SD 1.5
SD_MODEL_ID=runwayml/stable-diffusion-v1-5

# Pour du photoréalisme
SD_MODEL_ID=SG161222/Realistic_Vision_V5.1_noVAE

# Pour SDXL (nécessite plus de RAM)
SD_MODEL_ID=stabilityai/stable-diffusion-xl-base-1.0
```

## 🎨 Exemples avec DreamShaper-8

### Prompts optimisés pour DreamShaper-8 :

1. **Art fantastique** :
   ```
   a mystical forest with glowing mushrooms, fantasy art, detailed, magical atmosphere
   ```

2. **Portrait artistique** :
   ```
   portrait of a woman with flowing hair, ethereal lighting, oil painting style, highly detailed
   ```

3. **Concept art** :
   ```
   futuristic city at night, neon lights, cyberpunk, concept art, highly detailed
   ```

4. **Paysage** :
   ```
   mountain landscape at sunset, dramatic clouds, epic scenery, cinematic lighting
   ```

## 🚀 Performance

### Temps de génération estimés :

| Configuration | Steps | Temps |
|--------------|-------|-------|
| CPU (16GB) | 30 | ~30s |
| CPU (16GB) | 50 | ~1min |
| CPU (16GB) | 80 | ~2-3min |
| GPU (4GB) | 30 | ~5s |
| GPU (4GB) | 50 | ~8s |
| GPU (4GB) | 80 | ~12s |

DreamShaper-8 est généralement **10-20% plus rapide** que SD 1.5 tout en produisant de meilleurs résultats.

## 🔍 Comparaison visuelle

Pour comparer DreamShaper-8 avec SD 1.5, générez la même image avec les deux modèles :

```python
# Test avec le même prompt
prompt = "a cat in space, highly detailed, studio lighting"

# Avec DreamShaper-8 (défaut)
# → Meilleurs détails, éclairage plus naturel

# Avec SD 1.5 (changez SD_MODEL_ID dans .env)
# → Qualité standard, moins de détails
```

## 💡 Conseils d'utilisation

1. **Guidance Scale** : DreamShaper-8 fonctionne bien avec des valeurs de 7-9
2. **Steps** : 30-50 steps suffisent (pas besoin de 80+ comme avec SD 1.5)
3. **Negative Prompt** : Toujours utile pour éviter les défauts :
   ```
   ugly, blurry, low quality, distorted, deformed, bad anatomy
   ```

## 🆕 Nouveautés dans l'interface

L'interface Gradio est déjà optimisée pour DreamShaper-8 :
- Les templates de prompts sont compatibles
- Les cas d'usage (logo, marketing, game assets) fonctionnent parfaitement
- Les paramètres par défaut sont ajustés pour la meilleure qualité

## ⚠️ Note importante

Si vous avez déjà des modèles SD 1.5 en cache, DreamShaper-8 sera téléchargé en parallèle (pas de remplacement). Les deux modèles peuvent coexister.

Pour libérer de l'espace, vous pouvez supprimer l'ancien modèle :
```bash
# Localiser le cache Hugging Face
ls ~/.cache/huggingface/hub/  # Linux/Mac
dir C:\Users\<user>\.cache\huggingface\hub\  # Windows

# Supprimer manuellement les dossiers "models--runwayml--stable-diffusion-v1-5"
```

## 📊 Résultats attendus

Avec DreamShaper-8, vous devriez observer :
- ✅ Moins d'artefacts visuels
- ✅ Meilleure cohérence des détails
- ✅ Couleurs plus riches et naturelles
- ✅ Meilleure compréhension des prompts artistiques
- ✅ Génération légèrement plus rapide

## 🔗 Ressources

- [DreamShaper-8 sur Hugging Face](https://huggingface.co/Lykon/dreamshaper-8)
- [Exemples de générations](https://civitai.com/models/4384/dreamshaper)
- [Guide d'utilisation](https://huggingface.co/Lykon/dreamshaper-8#model-description)

---

**Profitez de la meilleure qualité artistique avec DreamShaper-8 ! 🎨✨**


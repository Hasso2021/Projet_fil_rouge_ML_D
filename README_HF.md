---
title: AI Creative Studio
emoji: 🎨
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "5.0.0"
app_file: app.py
pinned: false
license: mit
tags:
  - stable-diffusion
  - image-generation
  - dreamshaper
  - art
  - creative
---

# 🎨 AI Creative Studio

**Générateur d'images IA professionnel** utilisant Stable Diffusion (DreamShaper-8).

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces)

## ✨ Fonctionnalités

- 🎨 **Génération d'images haute qualité** avec DreamShaper-8
- 📝 **Templates de prompts optimisés** pour différents cas d'usage :
  - 🏷️ Design de logos
  - 📢 Visuels marketing
  - 🎮 Assets de jeux vidéo
  - 🖼️ Art créatif
- ⭐ **Score esthétique automatique** (0-10)
- 📊 **Historique et statistiques** de vos générations
- 🌡️ **Contrôle de qualité** via le curseur de température
- 💾 **Sauvegarde automatique** de toutes les générations

## 🚀 Utilisation

### Mode Simple
1. **Entrez un prompt** (ex: "a cat")
2. **Ajustez la température** (0.3 = rapide, 0.5 = équilibré, 0.8 = qualité max)
3. **Cliquez sur "Générer"**

### Mode Avancé (avec templates)
1. Sélectionnez un **cas d'usage** (Logo, Marketing, etc.)
2. Choisissez un **style** (s'affiche dynamiquement)
3. Entrez votre prompt de base
4. Les keywords optimisés sont ajoutés automatiquement !

## 🎯 Exemples de prompts

| Prompt | Cas d'usage | Style | Résultat |
|--------|-------------|-------|----------|
| `a cat` | General | - | Chat détaillé avec lighting professionnel |
| `tech startup` | Logo | Minimalist | Logo minimaliste moderne |
| `summer sale` | Marketing | Banner | Bannière publicitaire attractive |
| `magic sword` | Game Assets | Fantasy | Épée magique style jeu vidéo |
| `sunset beach` | Artistic | Photorealistic | Plage au coucher de soleil photoréaliste |

## 🤖 Modèle utilisé

**DreamShaper-8** par [Lykon](https://huggingface.co/Lykon/dreamshaper-8)

- Spécialisé pour l'art créatif
- Plus rapide et meilleur que Stable Diffusion 1.5 standard
- Excellent pour styles variés (réaliste, fantastique, art conceptuel)
- Taille: ~4GB (téléchargé automatiquement au premier lancement)

## ⚙️ Paramètres techniques

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| **Modèle** | DreamShaper-8 | Variante optimisée de SD 1.5 |
| **Scheduler** | DPM-Solver++ | Génération rapide (20-50 steps) |
| **Device** | CPU/GPU | Auto-détecté |
| **Résolution** | 512x512 | Standard SD 1.5 |
| **Guidance Scale** | 6.0-9.0 | Optimal pour DreamShaper-8 |

## 📈 Temps de génération

| Configuration | Température 0.3 | Température 0.5 | Température 0.8 |
|---------------|-----------------|-----------------|-----------------|
| **CPU** | ~30-40s (20 steps) | ~1min (35 steps) | ~1.5min (44 steps) |
| **GPU** | ~5s (20 steps) | ~8s (35 steps) | ~12s (44 steps) |

💡 **Astuce** : Sur CPU, utilisez température 0.3-0.5 pour de meilleurs temps de réponse.

## 🏗️ Architecture

Le projet utilise une architecture modulaire :

```
📦 AI Creative Studio
├── 🎨 Génération d'images (Stable Diffusion + DreamShaper-8)
├── 📝 Système de templates (Prompts optimisés par cas d'usage)
├── ⭐ Aesthetic Scorer (Évaluation automatique de qualité)
├── 🗄️ Base de données SQLite (Historique et métadonnées)
└── 🖥️ Interface Gradio (UI interactive)
```

**Technologies** : Python, PyTorch, Diffusers, Gradio, SQLAlchemy

## 📊 Fonctionnalités avancées

### Onglet Historique
- Consulter toutes vos générations passées
- Trier par date ou score esthétique
- Voir tous les paramètres de génération

### Onglet Statistiques
- Nombre total d'images générées
- Score moyen des générations
- Performances au fil du temps

## ⚠️ Notes importantes

### Sur CPU (gratuit)
- Génération plus lente (~1-2 minutes)
- Utilisez température 0.3-0.5 pour meilleur compromis
- 20-35 steps suffisent pour bonne qualité

### Sur GPU (si activé)
- Génération rapide (~5-10 secondes)
- Peut utiliser température plus élevée (0.7-1.0)
- 35-50 steps pour qualité maximale

### Prompts
- Les prompts simples sont **automatiquement enrichis**
- Exemple : "a cat" → "a cat, highly detailed, professional quality, sharp focus, beautiful lighting"
- Utilisez les templates pour résultats optimaux

## 🔗 Ressources

- 📖 [Documentation DreamShaper-8](https://huggingface.co/Lykon/dreamshaper-8)
- 🎨 [Exemples de générations](https://civitai.com/models/4384/dreamshaper)
- 💻 [Code source du projet](https://github.com/Hasso2021/Projet_fil_rouge_ML_D)

## 📝 Licence

MIT License - Libre d'utilisation et modification

---

**Développé avec ❤️ pour la création artistique assistée par IA**

*Projet académique - Formation Machine Learning & Deep Learning*


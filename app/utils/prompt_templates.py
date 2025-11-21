"""
Templates de prompts pour différents cas d'usage
Adaptés pour générer des contenus optimisés selon le contexte (logo, marketing, game assets, artistic)
"""
from typing import Dict, List, Optional, Tuple
from enum import Enum


class UseCase(str, Enum):
    """Cas d'usage supportés"""
    LOGO = "logo"
    MARKETING = "marketing"
    GAME_ASSETS = "game_assets"
    ARTISTIC = "artistic"
    GENERAL = "general"  # Cas par défaut sans template spécifique


# Styles disponibles par cas d'usage
USE_CASE_STYLES: Dict[str, List[str]] = {
    UseCase.LOGO: [
        "minimalist",
        "modern",
        "vintage",
        "geometric",
        "handdrawn",
        "3d",
        "abstract",
        "corporate"
    ],
    UseCase.MARKETING: [
        "social_media",
        "banner",
        "poster",
        "advertisement",
        "promotional",
        "branded",
        "product_showcase",
        "infographic"
    ],
    UseCase.GAME_ASSETS: [
        "pixel_art",
        "cartoon",
        "realistic",
        "low_poly",
        "hand_painted",
        "anime",
        "fantasy",
        "sci_fi"
    ],
    UseCase.ARTISTIC: [
        "photorealistic",
        "digital_art",
        "watercolor",
        "oil_painting",
        "sketch",
        "abstract",
        "surreal",
        "impressionist"
    ],
    UseCase.GENERAL: ["general"]
}


def get_logo_prompt(base_prompt: str, style: str = "minimalist") -> Tuple[str, str, Dict]:
    """
    Génère un prompt optimisé pour la création de logos.
    
    Args:
        base_prompt: Description du logo (ex: "a cat", "company name")
        style: Style du logo (minimalist, modern, vintage, etc.)
    
    Returns:
        tuple: (prompt optimisé, negative_prompt, paramètres recommandés)
    """
    style_keywords = {
        "minimalist": "minimalist, clean lines, simple shapes, elegant, timeless",
        "modern": "modern, sleek, contemporary, bold, clean design",
        "vintage": "vintage, retro, classic, aged texture, nostalgic",
        "geometric": "geometric shapes, precise lines, symmetry, mathematical",
        "handdrawn": "hand drawn, sketch style, organic, natural lines, artistic",
        "3d": "3D render, isometric, depth, dimensional, professional",
        "abstract": "abstract design, creative shapes, unique, innovative",
        "corporate": "corporate, professional, business, trustworthy, solid"
    }
    
    style_text = style_keywords.get(style.lower(), style_keywords["minimalist"])
    
    # Prompt optimisé pour logos
    optimized_prompt = f"{base_prompt}, logo design, {style_text}, high contrast, vector style, scalable, professional logo, centered composition, white background or transparent"
    
    # Negative prompt spécifique logos
    negative_prompt = "low quality, blurry, pixelated, text overlay, watermark, signature, complex background, cluttered, amateur design, distorted"
    
    # Paramètres optimisés pour logos
    params = {
        "guidance_scale": 9.0,  # Plus élevé pour meilleure fidélité au prompt
        "num_inference_steps": 50,
        "width": 512,
        "height": 512
    }
    
    return optimized_prompt, negative_prompt, params


def get_marketing_prompt(base_prompt: str, style: str = "social_media") -> Tuple[str, str, Dict]:
    """
    Génère un prompt optimisé pour la création de visuels marketing.
    
    Args:
        base_prompt: Description du visuel (ex: "product promotion", "event announcement")
        style: Type de visuel marketing (social_media, banner, poster, etc.)
    
    Returns:
        tuple: (prompt optimisé, negative_prompt, paramètres recommandés)
    """
    style_keywords = {
        "social_media": "social media post, vibrant colors, eye-catching, modern design, square format, optimized for Instagram",
        "banner": "banner design, horizontal layout, professional, clear text space, attention-grabbing",
        "poster": "poster design, vertical layout, bold typography, high impact, professional layout",
        "advertisement": "advertisement design, commercial, persuasive, professional photography style",
        "promotional": "promotional material, festive, attractive, engaging, colorful",
        "branded": "branded content, consistent color scheme, professional, corporate identity",
        "product_showcase": "product photography, studio lighting, professional, clean background, high quality",
        "infographic": "infographic style, clear information hierarchy, visual data representation, educational"
    }
    
    style_text = style_keywords.get(style.lower(), style_keywords["social_media"])
    
    # Prompt optimisé pour marketing
    optimized_prompt = f"{base_prompt}, {style_text}, marketing design, professional, high quality, engaging, commercial photography"
    
    # Negative prompt spécifique marketing
    negative_prompt = "low quality, blurry, amateur, unprofessional, cluttered, confusing layout, bad composition, watermark, text errors"
    
    # Paramètres optimisés pour marketing
    params = {
        "guidance_scale": 8.5,
        "num_inference_steps": 50,
        "width": 1024 if style in ["banner", "poster"] else 512,
        "height": 512 if style == "banner" else (1024 if style == "poster" else 512)
    }
    
    return optimized_prompt, negative_prompt, params


def get_game_assets_prompt(base_prompt: str, style: str = "pixel_art") -> Tuple[str, str, Dict]:
    """
    Génère un prompt optimisé pour la création d'assets de jeu vidéo.
    
    Args:
        base_prompt: Description de l'asset (ex: "sword", "tree", "character")
        style: Style graphique (pixel_art, cartoon, realistic, etc.)
    
    Returns:
        tuple: (prompt optimisé, negative_prompt, paramètres recommandés)
    """
    style_keywords = {
        "pixel_art": "pixel art, 8-bit style, retro game graphics, low resolution, sprite sheet",
        "cartoon": "cartoon style, vibrant colors, stylized, game asset, character design",
        "realistic": "realistic game asset, high quality texture, detailed, PBR material, game ready",
        "low_poly": "low poly 3D, geometric shapes, flat shading, minimalist, game asset",
        "hand_painted": "hand painted texture, stylized art, game asset, artistic brush strokes",
        "anime": "anime style, Japanese art style, vibrant, stylized character design",
        "fantasy": "fantasy game asset, magical, detailed, stylized, game ready",
        "sci_fi": "sci-fi game asset, futuristic, high tech, cyberpunk, detailed"
    }
    
    style_text = style_keywords.get(style.lower(), style_keywords["pixel_art"])
    
    # Prompt optimisé pour game assets
    optimized_prompt = f"{base_prompt}, {style_text}, game asset, isolated on transparent background, clean edges, usable in game engine, high quality texture"
    
    # Negative prompt spécifique game assets
    negative_prompt = "low quality, blurry, bad edges, complex background, cluttered, unusable in game, amateur, distorted"
    
    # Paramètres optimisés pour game assets
    params = {
        "guidance_scale": 8.0,
        "num_inference_steps": 50,
        "width": 512,
        "height": 512
    }
    
    return optimized_prompt, negative_prompt, params


def get_artistic_prompt(base_prompt: str, style: str = "photorealistic") -> Tuple[str, str, Dict]:
    """
    Génère un prompt optimisé pour la création artistique.
    
    Args:
        base_prompt: Description artistique (ex: "landscape", "portrait", "abstract composition")
        style: Style artistique (photorealistic, digital_art, watercolor, etc.)
    
    Returns:
        tuple: (prompt optimisé, negative_prompt, paramètres recommandés)
    """
    style_keywords = {
        "photorealistic": "photorealistic, highly detailed, 8K resolution, professional photography, sharp focus",
        "digital_art": "digital art, concept art, highly detailed, trending on ArtStation, vibrant colors",
        "watercolor": "watercolor painting, soft colors, artistic brush strokes, elegant, traditional art",
        "oil_painting": "oil painting, classical art style, rich colors, textured brush strokes, masterpiece",
        "sketch": "pencil sketch, line art, artistic drawing, detailed shading, black and white",
        "abstract": "abstract art, creative composition, artistic interpretation, unique, innovative",
        "surreal": "surreal art, dreamlike, imaginative, fantastical elements, artistic masterpiece",
        "impressionist": "impressionist painting, soft brush strokes, light and color, artistic style, masterpiece"
    }
    
    style_text = style_keywords.get(style.lower(), style_keywords["photorealistic"])
    
    # Prompt optimisé pour art
    optimized_prompt = f"{base_prompt}, {style_text}, masterpiece, high quality, artistic composition, award winning"
    
    # Negative prompt spécifique art
    negative_prompt = "low quality, blurry, amateur, distorted, bad anatomy, watermark, signature, text, ugly"
    
    # Paramètres optimisés pour art
    params = {
        "guidance_scale": 7.5,
        "num_inference_steps": 60,  # Plus de steps pour meilleure qualité artistique
        "width": 512,
        "height": 512
    }
    
    return optimized_prompt, negative_prompt, params


def apply_prompt_template(
    base_prompt: str,
    use_case: Optional[str] = None,
    style: Optional[str] = "general"
) -> Tuple[str, str, Dict]:
    """
    Applique le template de prompt approprié selon le cas d'usage et le style.
    
    Args:
        base_prompt: Prompt de base de l'utilisateur
        use_case: Cas d'usage ("logo", "marketing", "game_assets", "artistic", ou None)
        style: Style spécifique du cas d'usage (par défaut "general")
    
    Returns:
        tuple: (prompt optimisé, negative_prompt, paramètres recommandés)
    """
    # Si pas de use_case ou "general", enrichir automatiquement les prompts simples
    if not use_case or use_case == UseCase.GENERAL:
        # Enrichir automatiquement les prompts simples
        enriched_prompt = base_prompt.strip()
        
        # Si le prompt est très court (< 15 caractères), l'enrichir avec des keywords de qualité
        if len(enriched_prompt) < 15:
            enriched_prompt = f"{enriched_prompt}, highly detailed, professional quality, sharp focus, beautiful lighting"
        # Si le prompt ne contient pas de keywords de qualité, en ajouter quelques-uns
        elif not any(word in enriched_prompt.lower() for word in ["detailed", "quality", "professional", "sharp", "beautiful", "stunning", "high"]):
            enriched_prompt = f"{enriched_prompt}, high quality, detailed"
        
        # Negative prompt plus fort pour DreamShaper-8
        negative_prompt = "ugly, blurry, low quality, distorted, deformed, bad anatomy, bad proportions, watermark, signature, text, worst quality, low res, error, cropped"
        
        # Paramètres optimisés pour DreamShaper-8 sur CPU
        params = {
            "guidance_scale": 7.0,  # DreamShaper fonctionne bien avec 7-8
            "num_inference_steps": 35,  # Réduit de 50 à 35 pour CPU
            "width": 512,
            "height": 512
        }
        return enriched_prompt, negative_prompt, params
    
    # Normaliser use_case
    use_case = use_case.lower()
    
    # Appliquer le template approprié
    if use_case == UseCase.LOGO:
        return get_logo_prompt(base_prompt, style)
    elif use_case == UseCase.MARKETING:
        return get_marketing_prompt(base_prompt, style)
    elif use_case == UseCase.GAME_ASSETS:
        return get_game_assets_prompt(base_prompt, style)
    elif use_case == UseCase.ARTISTIC:
        return get_artistic_prompt(base_prompt, style)
    else:
        # Cas non reconnu, utiliser defaults
        negative_prompt = "low quality, blurry, distorted, watermark, signature, text, bad anatomy"
        params = {
            "guidance_scale": 7.5,
            "num_inference_steps": 50,
            "width": 512,
            "height": 512
        }
        return base_prompt, negative_prompt, params


def get_available_styles(use_case: Optional[str] = None) -> List[str]:
    """
    Retourne la liste des styles disponibles pour un cas d'usage donné.
    
    Args:
        use_case: Cas d'usage (None pour tous les styles)
    
    Returns:
        list: Liste des styles disponibles
    """
    if not use_case or use_case == UseCase.GENERAL:
        return ["general"]
    
    use_case = use_case.lower()
    return USE_CASE_STYLES.get(use_case, ["general"])


def get_available_use_cases() -> List[str]:
    """
    Retourne la liste de tous les cas d'usage disponibles.
    
    Returns:
        list: Liste des cas d'usage (strings)
    """
    return [UseCase.LOGO.value, UseCase.MARKETING.value, UseCase.GAME_ASSETS.value, UseCase.ARTISTIC.value, UseCase.GENERAL.value]


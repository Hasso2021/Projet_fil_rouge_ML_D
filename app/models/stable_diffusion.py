"""
Générateur d'images avec Stable Diffusion (DreamShaper-8).

Ce module gère:
- Chargement du modèle Stable Diffusion
- Configuration du scheduler pour génération optimisée
- Optimisations mémoire (CPU/GPU)
- Génération d'images à partir de prompts textuels
"""
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
from typing import Optional
from app.utils.config import settings

class StableDiffusionGenerator:
    """
    Classe principale pour la génération d'images avec Stable Diffusion.
    
    Architecture:
    - Modèle: DreamShaper-8 (variante optimisée de SD 1.5)
    - Scheduler: DPM-Solver++ (plus rapide que DDIM)
    - Device: GPU (CUDA) ou CPU selon configuration
    
    Optimisations appliquées:
    - Attention slicing: Réduit l'usage mémoire
    - Mixed precision (float16/float32): Accélère le calcul
    - Scheduler optimisé: DPM-Solver pour génération en 20-50 steps
    """
    def __init__(self):
        """
        Initialise le générateur Stable Diffusion.
        
        Processus d'initialisation:
        1. Configuration du device (GPU/CPU) et du dtype (float16/float32)
        2. Téléchargement/chargement du modèle DreamShaper-8 depuis Hugging Face
        3. Configuration du scheduler optimisé (DPM-Solver++)
        4. Application des optimisations mémoire
        
        Note: Au premier lancement, le modèle (~4GB) est téléchargé depuis
        Hugging Face et mis en cache localement.
        """
        # Configuration du device et du type de précision
        self.device = settings.SD_DEVICE
        self.dtype = torch.float16 if settings.SD_DTYPE == "float16" else torch.float32
        
        # ========================================
        # CHARGEMENT DU MODÈLE STABLE DIFFUSION
        # ========================================
        # Télécharge depuis Hugging Face Hub au premier lancement
        # Modèle utilisé: DreamShaper-8 (spécialisé art créatif)
        self.pipe = StableDiffusionPipeline.from_pretrained(
            settings.SD_MODEL_ID,
            dtype=self.dtype,              # Précision (float16 pour GPU, float32 pour CPU)
            safety_checker=None,           # Désactivé pour plus de liberté créative
            requires_safety_checker=False  # Ne pas exiger de vérificateur de contenu
        ).to(self.device)
        
        # ========================================
        # CONFIGURATION DU SCHEDULER OPTIMISÉ
        # ========================================
        # Le scheduler contrôle le processus de débruitage (denoising)
        # DPM-Solver++: Plus rapide que DDIM, même qualité en moins de steps
        # Avantage: Génération en 20-50 steps vs 50-80 steps avec DDIM
        try:
            scheduler_config = self.pipe.scheduler.config.copy()
            
            # Fix de compatibilité pour DreamShaper-8
            # Certains modèles ont final_sigmas_type="zero" incompatible avec algorithm_type="deis"
            if hasattr(scheduler_config, 'final_sigmas_type'):
                if scheduler_config.get('final_sigmas_type') == 'zero' and \
                   scheduler_config.get('algorithm_type') == 'deis':
                    # Correction: utiliser "sigma_min" au lieu de "zero"
                    scheduler_config['final_sigmas_type'] = 'sigma_min'
            
            # Appliquer le nouveau scheduler optimisé
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                scheduler_config
            )
        except Exception as e:
            # Fallback: Utiliser le scheduler par défaut du modèle si erreur
            # Cela n'affecte pas la qualité, juste la vitesse
            print(f"WARNING: Impossible de configurer DPM-Solver, utilisation du scheduler par defaut: {e}")
            print("INFO: Le modele utilisera son scheduler par defaut (generalement aussi efficace)")
        
        # ========================================
        # OPTIMISATIONS MÉMOIRE
        # ========================================
        # Ces optimisations permettent de:
        # - Réduire l'usage mémoire VRAM/RAM
        # - Éviter les OutOfMemory errors
        # - Permettre génération sur hardware limité
        
        if self.device == "cuda":
            # GPU: Attention slicing pour réduire usage VRAM
            # Divise les calculs d'attention en chunks plus petits
            self.pipe.enable_attention_slicing()
            
            # xFormers (optionnel, si installé): Encore plus d'optimisation
            # Réduit VRAM de 30-40% supplémentaires
            # self.pipe.enable_xformers_memory_efficient_attention()
        else:
            # CPU: Attention slicing critique pour performance acceptable
            # Sans cela, génération prend 10-20 minutes
            # Avec: ~1-2 minutes
            self.pipe.enable_attention_slicing(1)
            # CPU mode : utiliser float32 pour compatibilité et stabilité
            if self.dtype == torch.float16:
                print("WARNING: float16 sur CPU non recommande, passage a float32 pour compatibilite")
                self.dtype = torch.float32
                # Recharger avec float32
                self.pipe = StableDiffusionPipeline.from_pretrained(
                    settings.SD_MODEL_ID,
                    dtype=torch.float32,  # Utiliser dtype au lieu de torch_dtype (déprécié)
                    safety_checker=None,
                    requires_safety_checker=False
                ).to(self.device)
                
                # Configurer le scheduler (gérer les configurations différentes)
                try:
                    scheduler_config = self.pipe.scheduler.config.copy()
                    if hasattr(scheduler_config, 'final_sigmas_type'):
                        if scheduler_config.get('final_sigmas_type') == 'zero' and \
                           scheduler_config.get('algorithm_type') == 'deis':
                            scheduler_config['final_sigmas_type'] = 'sigma_min'
                    self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                        scheduler_config
                    )
                except Exception as e:
                    print(f"WARNING: Scheduler par defaut utilise: {e}")
                
                self.pipe.enable_attention_slicing(1)
    
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 50,
        width: int = 512,
        height: int = 512,
        seed: Optional[int] = None
    ) -> Image.Image:
        """
        Génère une image à partir d'un prompt textuel avec Stable Diffusion.
        
        Processus de génération:
        1. Encodage du prompt en embeddings via CLIP
        2. Génération de bruit gaussien initial
        3. Débruitage itératif guidé par le prompt (num_inference_steps fois)
        4. Décodage du latent en image RGB finale
        
        Args:
            prompt: Description textuelle de l'image désirée
                   Ex: "a majestic cat on a throne, royal palace, cinematic lighting"
                   
            negative_prompt: Éléments à éviter dans l'image (optionnel)
                           Ex: "ugly, blurry, low quality, distorted"
                           
            guidance_scale: Force d'adhésion au prompt (CFG - Classifier Free Guidance)
                          - 1-5: Créatif mais peut dévier du prompt
                          - 7-9: Équilibré (optimal pour DreamShaper-8)
                          - 10-15: Très fidèle au prompt mais peut saturer
                          
            num_inference_steps: Nombre d'étapes de débruitage
                               - 20-30: Rapide (~30s CPU, ~5s GPU)
                               - 35-50: Équilibré (~1min CPU, ~8s GPU)
                               - 50-80: Haute qualité (~2min CPU, ~12s GPU)
                               
            width, height: Dimensions de l'image en pixels
                          - 512x512: Standard SD 1.5 (rapide)
                          - 768x512 ou 512x768: Portrait/Paysage
                          Note: Dimensions doivent être multiples de 64
                          
            seed: Graine aléatoire pour reproductibilité (optionnel)
                 Même seed + même prompt = même image
        
        Returns:
            PIL.Image: Image générée (format RGB)
        
        Temps de génération estimés (DreamShaper-8, 35 steps):
        - GPU (RTX 3060): ~8 secondes
        - CPU (i7-10700K): ~1 minute
        """
        # ========================================
        # CONFIGURATION DU GÉNÉRATEUR ALÉATOIRE
        # ========================================
        # Si un seed est fourni, on peut reproduire exactement la même image
        # Utile pour: tests, comparaisons, debugging
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        
        # ========================================
        # GÉNÉRATION DE L'IMAGE
        # ========================================
        # inference_mode: Désactive le calcul des gradients pour économiser mémoire
        # Plus rapide que eval() et utilise moins de VRAM/RAM
        with torch.inference_mode():
            image = self.pipe(
                prompt=prompt,                          # Prompt principal
                negative_prompt=negative_prompt,        # Ce qu'on veut éviter
                num_inference_steps=num_inference_steps, # Nombre de steps de débruitage
                guidance_scale=guidance_scale,          # Force du guidage CFG
                width=width,                            # Largeur cible
                height=height,                          # Hauteur cible
                generator=generator                     # Générateur aléatoire (seed)
            ).images[0]  # Récupère la première (et seule) image générée
        
        return image

# Instance globale
sd_generator = StableDiffusionGenerator()


import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
from typing import Optional
from app.utils.config import settings

class StableDiffusionGenerator:
    def __init__(self):
        self.device = settings.SD_DEVICE
        self.dtype = torch.float16 if settings.SD_DTYPE == "float16" else torch.float32
        
        # Charger le modèle
        self.pipe = StableDiffusionPipeline.from_pretrained(
            settings.SD_MODEL_ID,
            dtype=self.dtype,  # Utiliser dtype au lieu de torch_dtype (déprécié)
            safety_checker=None,
            requires_safety_checker=False
        ).to(self.device)
        
        # Optimiser avec DPM-Solver (gérer les configurations différentes des modèles)
        try:
            scheduler_config = self.pipe.scheduler.config.copy()
            
            # Fix pour certains modèles qui ont final_sigmas_type="zero"
            # (ex: DreamShaper 8 avec algorithm_type="deis")
            if hasattr(scheduler_config, 'final_sigmas_type'):
                if scheduler_config.get('final_sigmas_type') == 'zero' and \
                   scheduler_config.get('algorithm_type') == 'deis':
                    scheduler_config['final_sigmas_type'] = 'sigma_min'
            
            # Créer le scheduler avec la config corrigée
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                scheduler_config
            )
        except Exception as e:
            # Si erreur, utiliser le scheduler par défaut du modèle
            print(f"⚠️ Impossible de configurer DPM-Solver, utilisation du scheduler par défaut: {e}")
            print("💡 Le modèle utilisera son scheduler par défaut (généralement aussi efficace)")
        
        # Optimisations mémoire
        if self.device == "cuda":
            self.pipe.enable_attention_slicing()
            # self.pipe.enable_xformers_memory_efficient_attention()  # Si xformers installé
        else:
            # Optimisations pour CPU
            self.pipe.enable_attention_slicing(1)  # Attention slicing aussi sur CPU
            # CPU mode : utiliser float32 pour compatibilité et stabilité
            if self.dtype == torch.float16:
                print("⚠️ float16 sur CPU non recommandé, passage à float32 pour compatibilité")
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
                    print(f"⚠️ Scheduler par défaut utilisé: {e}")
                
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
        Génère une image avec Stable Diffusion.
        
        Args:
            prompt: Prompt textuel
            negative_prompt: Prompt négatif (optionnel)
            guidance_scale: Force d'adhésion au prompt
            num_inference_steps: Nombre d'étapes de débruitage
            width: Largeur de l'image
            height: Hauteur de l'image
            seed: Seed pour reproductibilité
        
        Returns:
            PIL.Image: Image générée
        """
        # Générateur avec seed
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        
        # Génération
        with torch.inference_mode():
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                width=width,
                height=height,
                generator=generator
            ).images[0]
        
        return image

# Instance globale
sd_generator = StableDiffusionGenerator()


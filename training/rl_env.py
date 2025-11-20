import gymnasium as gym
from gymnasium import spaces
import numpy as np
from app.models.stable_diffusion import sd_generator
from app.models.aesthetic_scorer import aesthetic_scorer

class PromptOptimizationEnv(gym.Env):
    """
    Environnement Gym pour optimiser les prompts Stable Diffusion.
    
    Observation: Embedding du prompt actuel + paramètres SD
    Action: Modifications du prompt (ajout de keywords, changement de params)
    Reward: Score esthétique de l'image générée
    """
    
    def __init__(self, fast_mode: bool = False):
        super().__init__()
        
        self.fast_mode = fast_mode
        
        # Espace d'actions : 10 keywords possibles à ajouter + 5 ajustements de params
        self.action_space = spaces.Discrete(15)
        
        # Espace d'observations : [embedding prompt (512) + guidance (1) + steps (1)]
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(514,),
            dtype=np.float32
        )
        
        # Keywords disponibles pour enrichir les prompts
        self.keywords = [
            "highly detailed",
            "8k resolution",
            "trending on artstation",
            "photorealistic",
            "volumetric lighting",
            "cinematic",
            "masterpiece",
            "award winning",
            "vibrant colors",
            "sharp focus"
        ]
        
        # État initial
        self.base_prompt = ""
        self.current_prompt = ""
        self.guidance_scale = 7.5
        # Mode rapide : 20 steps au lieu de 50 (gain de vitesse ~2.5x)
        self.num_steps = 20 if fast_mode else 50
        
        # Historique des scores
        self.scores_history = []
        
    def reset(self, seed=None, options=None):
        """Réinitialise l'environnement."""
        super().reset(seed=seed)
        
        # Prompt de base (peut être passé en options)
        self.base_prompt = options.get("base_prompt", "a beautiful landscape") if options else "a beautiful landscape"
        self.current_prompt = self.base_prompt
        self.guidance_scale = 7.5
        # Mode rapide : 20 steps au lieu de 50
        self.num_steps = 20 if self.fast_mode else 50
        self.scores_history = []
        
        # Observation initiale
        obs = self._get_observation()
        info = {"prompt": self.current_prompt}
        
        return obs, info
    
    def step(self, action):
        """Exécute une action et retourne le résultat."""
        
        # Interpréter l'action
        if action < 10:
            # Ajouter un keyword
            keyword = self.keywords[action]
            if keyword not in self.current_prompt:
                self.current_prompt += f", {keyword}"
        elif action == 10:
            # Augmenter guidance_scale
            self.guidance_scale = min(20.0, self.guidance_scale + 1.0)
        elif action == 11:
            # Diminuer guidance_scale
            self.guidance_scale = max(1.0, self.guidance_scale - 1.0)
        elif action == 12:
            # Augmenter num_steps
            self.num_steps = min(100, self.num_steps + 10)
        elif action == 13:
            # Diminuer num_steps
            self.num_steps = max(20, self.num_steps - 10)
        else:
            # Reset prompt
            self.current_prompt = self.base_prompt
        
        # Générer image avec les paramètres actuels
        image = sd_generator.generate(
            prompt=self.current_prompt,
            guidance_scale=self.guidance_scale,
            num_inference_steps=self.num_steps
        )
        
        # Calculer reward (score esthétique)
        reward = aesthetic_scorer.score(image)
        self.scores_history.append(reward)
        
        # Observation suivante
        obs = self._get_observation()
        
        # Episode terminé après N actions
        terminated = len(self.scores_history) >= 10
        truncated = False
        
        info = {
            "prompt": self.current_prompt,
            "guidance_scale": self.guidance_scale,
            "num_steps": self.num_steps,
            "score": reward
        }
        
        return obs, reward, terminated, truncated, info
    
    def _get_observation(self):
        """Retourne l'observation actuelle."""
        # TODO: Utiliser un text encoder (CLIP) pour l'embedding du prompt
        # Pour simplifier, on utilise un embedding aléatoire ici
        prompt_embedding = np.random.randn(512).astype(np.float32)
        
        # Ajouter les paramètres SD normalisés
        params = np.array([
            self.guidance_scale / 20.0,  # Normalisé [0, 1]
            self.num_steps / 100.0       # Normalisé [0, 1]
        ], dtype=np.float32)
        
        obs = np.concatenate([prompt_embedding, params])
        return obs


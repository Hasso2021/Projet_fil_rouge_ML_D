import os
from typing import Optional, Dict, Any
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from app.utils.config import settings
from training.rl_env import PromptOptimizationEnv

class RLOptimizer:
    """
    Agent RL qui optimise les prompts pour Stable Diffusion.
    """
    
    def __init__(self, env: Optional[PromptOptimizationEnv] = None, fast_mode: bool = False):
        self.env = env or PromptOptimizationEnv(fast_mode=fast_mode)
        self.model: Optional[PPO] = None
        self.fast_mode = fast_mode
        
        # Charger modèle si existe
        if os.path.exists(settings.RL_AGENT_PATH):
            try:
                self.model = PPO.load(settings.RL_AGENT_PATH, env=self.env)
                print(f"OK: Modele RL charge depuis {settings.RL_AGENT_PATH}")
            except Exception as e:
                print(f"WARNING: Erreur lors du chargement du modele RL: {e}")
                print(f"INFO: Verifiez que le modele existe et est compatible avec stable-baselines3==2.2.1")
                self.model = None
        else:
            print(f"ℹ️ Modèle RL non trouvé à {settings.RL_AGENT_PATH}")
            print(f"INFO: Entrainez d'abord le modele avec training/train_rl_agent.py")
            print(f"   ou téléchargez-le depuis Colab (voir WORKFLOW_HYBRIDE.md)")
            self.model = None
    
    def train(self, total_timesteps: int = 10000, save_path: Optional[str] = None):
        """
        Entraîne l'agent RL.
        
        Args:
            total_timesteps: Nombre total de steps d'entraînement
            save_path: Chemin pour sauvegarder le modèle
        """
        if self.model is None:
            # Créer nouveau modèle PPO
            # Mode rapide : n_steps réduit de 2048 à 512 (gain de vitesse ~4x)
            n_steps_ppo = 512 if self.fast_mode else 2048
            self.model = PPO(
                "MlpPolicy",
                self.env,
                learning_rate=3e-4,
                n_steps=n_steps_ppo,
                batch_size=64,
                n_epochs=10,
                gamma=0.99,
                gae_lambda=0.95,
                clip_range=0.2,
                ent_coef=0.01,
                verbose=1,
                tensorboard_log="./logs/ppo_prompt_optimizer/",
                device="cpu"  # PPO fonctionne mieux sur CPU pour MlpPolicy (évite warning GPU)
            )
            print("OK: Nouveau modele PPO cree")
            if self.fast_mode:
                print("⚡ Mode rapide activé: n_steps PPO réduit à 512 (au lieu de 2048)")
        
        # Callbacks
        save_path = save_path or settings.RL_AGENT_PATH
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        checkpoint_callback = CheckpointCallback(
            save_freq=1000,
            save_path="./models/checkpoints/",
            name_prefix="ppo_prompt_opt"
        )
        
        print(f"Demarrage entrainement PPO ({total_timesteps} steps)...")
        self.model.learn(
            total_timesteps=total_timesteps,
            callback=checkpoint_callback,
            progress_bar=True
        )
        
        # Sauvegarde finale
        self.model.save(save_path)
        print(f"OK: Entrainement termine et modele sauvegarde dans {save_path}")
    
    def optimize_prompt(
        self,
        base_prompt: str,
        n_iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Utilise l'agent entraîné pour optimiser un prompt.
        
        Args:
            base_prompt: Prompt de base à optimiser
            n_iterations: Nombre d'itérations d'optimisation
        
        Returns:
            dict: Résultats de l'optimisation
        """
        if self.model is None:
            raise ValueError("Modèle RL non entraîné. Appelez train() d'abord.")
        
        # Reset env avec nouveau prompt
        obs, _ = self.env.reset(options={"base_prompt": base_prompt})
        
        # Génération originale (baseline)
        from app.models.stable_diffusion import sd_generator
        from app.models.aesthetic_scorer import aesthetic_scorer
        
        original_image = sd_generator.generate(
            prompt=base_prompt,
            guidance_scale=7.5,
            num_inference_steps=50
        )
        original_score = aesthetic_scorer.score(original_image)
        
        # Optimisation avec agent
        best_prompt = base_prompt
        best_score = original_score
        best_image = original_image
        best_info = {}
        
        for i in range(n_iterations):
            action, _ = self.model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info = self.env.step(action)
            
            if reward > best_score:
                best_score = reward
                best_prompt = info['prompt']
                best_info = info
            
            if done or truncated:
                break
        
        # Générer meilleure image avec meilleur prompt
        best_image = sd_generator.generate(
            prompt=best_prompt,
            guidance_scale=best_info.get('guidance_scale', 7.5),
            num_inference_steps=best_info.get('num_steps', 50)
        )
        
        return {
            'original_prompt': base_prompt,
            'optimized_prompt': best_prompt,
            'original_score': float(original_score),
            'optimized_score': float(best_score),
            'improvement': float(best_score - original_score),
            'best_params': {
                'guidance_scale': best_info.get('guidance_scale', 7.5),
                'num_steps': best_info.get('num_steps', 50)
            }
        }

# Instance globale (chargée à la demande)
rl_optimizer: Optional[RLOptimizer] = None

def get_rl_optimizer(fast_mode: bool = False) -> RLOptimizer:
    """Retourne l'instance globale de l'optimiseur RL."""
    global rl_optimizer
    if rl_optimizer is None:
        rl_optimizer = RLOptimizer(fast_mode=fast_mode)
    return rl_optimizer


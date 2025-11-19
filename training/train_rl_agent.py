"""
Script d'entraînement de l'agent RL pour optimiser les prompts.
"""
import argparse
from app.models.rl_agent import RLOptimizer
from training.rl_env import PromptOptimizationEnv

def main():
    parser = argparse.ArgumentParser(description="Entraîner l'agent RL")
    parser.add_argument(
        "--total_timesteps",
        type=int,
        default=10000,
        help="Nombre total de steps d'entraînement"
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default=None,
        help="Chemin pour sauvegarder le modèle"
    )
    
    args = parser.parse_args()
    
    # Créer environnement
    env = PromptOptimizationEnv()
    
    # Créer et entraîner agent
    agent = RLOptimizer(env=env)
    agent.train(
        total_timesteps=args.total_timesteps,
        save_path=args.save_path
    )
    
    print("✅ Entraînement terminé!")

if __name__ == "__main__":
    main()


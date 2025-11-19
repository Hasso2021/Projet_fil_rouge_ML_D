"""
Script pour évaluer l'agent RL entraîné.
"""
import argparse
from app.models.rl_agent import RLOptimizer
from training.rl_env import PromptOptimizationEnv

def main():
    parser = argparse.ArgumentParser(description="Évaluer l'agent RL")
    parser.add_argument(
        "--prompt",
        type=str,
        default="a beautiful landscape",
        help="Prompt de base à optimiser"
    )
    parser.add_argument(
        "--n_iterations",
        type=int,
        default=10,
        help="Nombre d'itérations d'optimisation"
    )
    
    args = parser.parse_args()
    
    # Créer environnement et agent
    env = PromptOptimizationEnv()
    agent = RLOptimizer(env=env)
    
    if agent.model is None:
        print("❌ Erreur: Modèle RL non trouvé. Entraînez d'abord avec train_rl_agent.py")
        return
    
    # Optimiser le prompt
    print(f"🔄 Optimisation du prompt: '{args.prompt}'...")
    result = agent.optimize_prompt(
        base_prompt=args.prompt,
        n_iterations=args.n_iterations
    )
    
    # Afficher résultats
    print("\n📊 Résultats de l'optimisation:")
    print(f"  Prompt original: {result['original_prompt']}")
    print(f"  Prompt optimisé: {result['optimized_prompt']}")
    print(f"  Score original: {result['original_score']:.2f}")
    print(f"  Score optimisé: {result['optimized_score']:.2f}")
    print(f"  Amélioration: {result['improvement']:+.2f}")
    print(f"  Paramètres optimaux: {result['best_params']}")

if __name__ == "__main__":
    main()


"""
Script d'entraînement de l'agent RL pour optimiser les prompts.

⚠️ IMPORTANT pour CPU (16GB RAM) :
- Utilise fast_mode=True par défaut (3-5x plus rapide)
- Recommandé : 2500 steps (~2-4 heures) ou 5000 steps (~4-8 heures)
- Pour GPU : désactivez fast_mode pour meilleure qualité
"""
import argparse
import os
from app.models.rl_agent import RLOptimizer
from training.rl_env import PromptOptimizationEnv

def main():
    parser = argparse.ArgumentParser(
        description="Entraîner l'agent RL pour optimiser les prompts Stable Diffusion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  # Entraînement rapide sur CPU (2500 steps, ~2-4 heures)
  python training/train_rl_agent.py --total_timesteps 2500 --fast_mode

  # Entraînement complet sur CPU (5000 steps, ~4-8 heures)
  python training/train_rl_agent.py --total_timesteps 5000 --fast_mode

  # Entraînement qualité sur GPU (10000 steps, ~1-2 heures)
  python training/train_rl_agent.py --total_timesteps 10000 --no-fast_mode
        """
    )
    parser.add_argument(
        "--total_timesteps",
        type=int,
        default=2500,
        help="Nombre total de steps d'entraînement (défaut: 2500 pour tests rapides)"
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default=None,
        help="Chemin pour sauvegarder le modèle (défaut: models/rl_agent.zip)"
    )
    parser.add_argument(
        "--fast_mode",
        action="store_true",
        default=True,  # Activé par défaut pour CPU
        help="Mode rapide: réduit steps SD (20) et n_steps PPO (512) - 3-5x plus rapide (DÉFAUT)"
    )
    parser.add_argument(
        "--no-fast_mode",
        dest="fast_mode",
        action="store_false",
        help="Désactiver le mode rapide pour meilleure qualité (recommandé pour GPU)"
    )
    
    args = parser.parse_args()
    
    # Afficher configuration
    print("="*60)
    print("🚀 ENTRAÎNEMENT RL AGENT - Optimisation de Prompts")
    print("="*60)
    print(f"📊 Steps d'entraînement: {args.total_timesteps}")
    print(f"⚡ Mode rapide: {'ACTIVÉ' if args.fast_mode else 'DÉSACTIVÉ'}")
    
    if args.fast_mode:
        print("   - Steps SD: 20 (au lieu de 50)")
        print("   - n_steps PPO: 512 (au lieu de 2048)")
        est_time_cpu = args.total_timesteps / 10  # ~10 steps/min sur CPU en fast_mode
        est_time_gpu = args.total_timesteps / 100  # ~100 steps/min sur GPU en fast_mode
        print(f"   - Temps estimé CPU: ~{est_time_cpu/60:.1f} heures ({est_time_cpu:.0f} min)")
        print(f"   - Temps estimé GPU: ~{est_time_gpu/60:.1f} heures ({est_time_gpu:.0f} min)")
    else:
        print("   - Steps SD: 50 (qualité maximale)")
        print("   - n_steps PPO: 2048 (qualité maximale)")
        est_time_cpu = args.total_timesteps / 2  # ~2 steps/min sur CPU
        est_time_gpu = args.total_timesteps / 50  # ~50 steps/min sur GPU
        print(f"   - Temps estimé CPU: ~{est_time_cpu/60:.1f} heures ({est_time_cpu:.0f} min)")
        print(f"   - Temps estimé GPU: ~{est_time_gpu/60:.1f} heures ({est_time_gpu:.0f} min)")
    
    device = os.environ.get("SD_DEVICE", "cpu")
    print(f"🖥️  Device: {device.upper()}")
    print(f"💾 Modèle sauvegardé: {args.save_path or 'models/rl_agent.zip'}")
    print("="*60)
    print()
    
    # Créer environnement avec fast_mode
    env = PromptOptimizationEnv(fast_mode=args.fast_mode)
    
    # Créer et entraîner agent avec fast_mode
    agent = RLOptimizer(env=env, fast_mode=args.fast_mode)
    
    print("🔄 Démarrage de l'entraînement...")
    print("💡 Vous pouvez arrêter avec Ctrl+C - le modèle sera sauvegardé à chaque checkpoint")
    print()
    
    try:
        agent.train(
            total_timesteps=args.total_timesteps,
            save_path=args.save_path
        )
        print()
        print("="*60)
        print("✅ Entraînement terminé avec succès!")
        print(f"💾 Modèle sauvegardé: {args.save_path or 'models/rl_agent.zip'}")
        print("="*60)
    except KeyboardInterrupt:
        print()
        print("⚠️  Entraînement interrompu par l'utilisateur")
        print("💾 Checkpoints disponibles dans: models/checkpoints/")
        print("💡 Vous pouvez reprendre l'entraînement plus tard")

if __name__ == "__main__":
    main()


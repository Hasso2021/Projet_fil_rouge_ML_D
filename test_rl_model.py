"""
Script pour tester si le modele RL est correctement charge
"""
import os
from app.models.rl_agent import RLOptimizer

def test_rl_model():
    """Test le chargement du modele RL"""
    
    print("="*60)
    print("TEST DU MODELE RL")
    print("="*60)
    
    # Verifier que le fichier existe
    model_path = "models/rl_agent.zip"
    if not os.path.exists(model_path):
        print(f"ERREUR: Modele introuvable : {model_path}")
        print("\nTelecharger d'abord le modele depuis RunPod !")
        print("   1. Voir les instructions dans RECUPERER_MODELES_RUNPOD.md")
        print("   2. Placer le fichier dans models/rl_agent.zip")
        return False
    
    # Verifier la taille
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"OK: Modele trouve : {model_path} ({size_mb:.2f} MB)")
    
    # Tenter de charger le modele
    try:
        print("\nChargement du modele RL...")
        rl_optimizer = RLOptimizer()
        
        if rl_optimizer.model is None:
            print("ERREUR: Modele non charge (model is None)")
            return False
        
        print("OK: Modele charge avec succes !")
        
        # Test d'optimisation simple
        print("\nTest d'optimisation d'un prompt simple...")
        test_prompt = "a cat"
        
        try:
            result = rl_optimizer.optimize_prompt(
                base_prompt=test_prompt,
                n_iterations=3  # Petit nombre pour test rapide
            )
            
            print("\nResultats de l'optimisation :")
            print(f"   - Prompt original : {result['original_prompt']}")
            print(f"   - Prompt optimise : {result['optimized_prompt']}")
            print(f"   - Amelioration : {result['improvement']:+.2f}")
            print(f"   - Score original : {result['original_score']:.2f}")
            print(f"   - Score optimise : {result['optimized_score']:.2f}")
            
            print("\nOK: Le modele RL fonctionne correctement !")
            return True
            
        except Exception as e:
            print(f"ATTENTION: Erreur lors de l'optimisation : {e}")
            print("   Le modele est charge mais l'optimisation a echoue")
            return False
        
    except Exception as e:
        print(f"ERREUR: Erreur lors du chargement : {e}")
        print("\nSolutions possibles :")
        print("   1. Verifier que le fichier n'est pas corrompu")
        print("   2. Verifier la compatibilite avec stable-baselines3==2.2.1")
        print("   3. Re-entrainer le modele si necessaire")
        return False

if __name__ == "__main__":
    success = test_rl_model()
    
    print("\n" + "="*60)
    if success:
        print("OK: TEST REUSSI - Modele RL pret a l'emploi !")
        print("\nVous pouvez maintenant activer l'optimisation RL dans Gradio")
    else:
        print("ERREUR: TEST ECHOUE - Veuillez telecharger/corriger le modele")
        print("\nInstructions pour telecharger depuis RunPod :")
        print("   1. Ouvrir Jupyter sur RunPod")
        print("   2. Creer une cellule avec le code de compression")
        print("   3. Telecharger l'archive creee")
        print("   4. Extraire dans models/")
    print("="*60)

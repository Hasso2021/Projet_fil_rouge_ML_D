"""
Script pour tester si le modèle RL est correctement chargé
"""
import os
from app.models.rl_agent import RLOptimizer

def test_rl_model():
    """Test le chargement du modèle RL"""
    
    print("="*60)
    print("🧪 TEST DU MODÈLE RL")
    print("="*60)
    
    # Vérifier que le fichier existe
    model_path = "models/rl_agent.zip"
    if not os.path.exists(model_path):
        print(f"❌ Modèle introuvable : {model_path}")
        print("\n💡 Téléchargez d'abord le modèle depuis RunPod !")
        print("   1. Voir les instructions dans le terminal")
        print("   2. Placer le fichier dans models/rl_agent.zip")
        return False
    
    # Vérifier la taille
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"✅ Modèle trouvé : {model_path} ({size_mb:.2f} MB)")
    
    # Tenter de charger le modèle
    try:
        print("\n🔄 Chargement du modèle RL...")
        rl_optimizer = RLOptimizer()
        
        if rl_optimizer.model is None:
            print("❌ Modèle non chargé (model is None)")
            return False
        
        print("✅ Modèle chargé avec succès !")
        
        # Test d'optimisation simple
        print("\n🧪 Test d'optimisation d'un prompt simple...")
        test_prompt = "a cat"
        
        try:
            result = rl_optimizer.optimize_prompt(
                base_prompt=test_prompt,
                n_iterations=3  # Petit nombre pour test rapide
            )
            
            print("\n📊 Résultats de l'optimisation :")
            print(f"   - Prompt original : {result['original_prompt']}")
            print(f"   - Prompt optimisé : {result['optimized_prompt']}")
            print(f"   - Amélioration : {result['improvement']:+.2f}")
            print(f"   - Score original : {result['original_score']:.2f}")
            print(f"   - Score optimisé : {result['optimized_score']:.2f}")
            
            print("\n✅ Le modèle RL fonctionne correctement !")
            return True
            
        except Exception as e:
            print(f"⚠️ Erreur lors de l'optimisation : {e}")
            print("   Le modèle est chargé mais l'optimisation a échoué")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        print("\n💡 Solutions possibles :")
        print("   1. Vérifiez que le fichier n'est pas corrompu")
        print("   2. Vérifiez la compatibilité avec stable-baselines3==2.2.1")
        print("   3. Ré-entraînez le modèle si nécessaire")
        return False

if __name__ == "__main__":
    success = test_rl_model()
    
    print("\n" + "="*60)
    if success:
        print("✅ TEST RÉUSSI - Modèle RL prêt à l'emploi !")
        print("\n💡 Vous pouvez maintenant activer l'optimisation RL dans Gradio")
    else:
        print("❌ TEST ÉCHOUÉ - Veuillez télécharger/corriger le modèle")
        print("\n📥 Instructions pour télécharger depuis RunPod :")
        print("   1. Ouvrir Jupyter sur RunPod")
        print("   2. Créer une cellule avec le code de compression")
        print("   3. Télécharger l'archive créée")
        print("   4. Extraire dans models/")
    print("="*60)


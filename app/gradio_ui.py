"""
Interface Gradio pour AI Creative Studio
Interface web interactive pour génération d'images avec Stable Diffusion et optimisation RL.
"""
import gradio as gr
from PIL import Image
import time
from pathlib import Path
from app.models.stable_diffusion import sd_generator
from app.models.aesthetic_scorer import aesthetic_scorer
from app.models.rl_agent import get_rl_optimizer
from app.utils.helpers import get_output_path
from app.database.database import SessionLocal, init_db
from app.database.repository import ImageRepository

def temperature_to_params(temperature: float):
    """
    Convertit la température (0-1) en paramètres optimaux.
    
    Temperature mapping:
    - 0.0-0.3: Fast, basic quality (guidance=5-6, steps=30-40)
    - 0.4-0.6: Balanced (guidance=7-8, steps=50-60)
    - 0.7-1.0: Best quality, slower (guidance=8.5-10, steps=70-80)
    """
    # Clamp temperature to [0, 1]
    temp = max(0.0, min(1.0, temperature))
    
    # Map temperature to guidance_scale (5.0 to 10.0)
    guidance_scale = 5.0 + (temp * 5.0)
    
    # Map temperature to num_inference_steps (30 to 80)
    num_steps = int(30 + (temp * 50))
    
    return guidance_scale, num_steps

def generate_image(
    prompt: str,
    temperature: float = 0.7,
    use_rl_optimization: bool = False
):
    """
    Génère une image avec Stable Diffusion (interface simplifiée).
    
    Args:
        prompt: Prompt textuel (ex: "nano banana")
        temperature: Qualité de l'image (0.0 = rapide, 1.0 = meilleure qualité)
        use_rl_optimization: Utiliser l'optimisation RL (optionnel)
    
    Returns:
        tuple: (image, info_text)
    """
    try:
        if not prompt or not prompt.strip():
            return None, "❌ Veuillez entrer un prompt pour générer une image."
        
        # Convertir température en paramètres
        guidance_scale, num_steps = temperature_to_params(temperature)
        
        # Paramètres optimaux fixes
        width = 512
        height = 512
        seed_value = None  # Toujours aléatoire pour plus de variété
        
        # Negative prompt optimisé par défaut pour meilleure qualité
        negative_prompt = "low quality, blurry, distorted, watermark, signature, text, writing, bad anatomy, deformed, ugly, amateur"
        
        # Optimisation RL si demandée
        optimized_prompt = None
        optimization_info = ""
        final_prompt = prompt
        
        if use_rl_optimization:
            try:
                rl_optimizer = get_rl_optimizer()
                optimization_result = rl_optimizer.optimize_prompt(
                    base_prompt=prompt,
                    n_iterations=10
                )
                optimized_prompt = optimization_result['optimized_prompt']
                final_prompt = optimized_prompt
                optimization_info = f"""
**✨ Optimisation RL activée**
- Prompt original : {optimization_result['original_prompt']}
- Prompt optimisé : {optimization_result['optimized_prompt']}
- Amélioration estimée : {optimization_result['improvement']:+.2f}
"""
            except Exception as e:
                optimization_info = f"⚠️ Optimisation RL non disponible ({str(e)[:50]}...)\n💡 Génération sans optimisation RL"
        
        # Génération de l'image
        start_time = time.time()
        image = sd_generator.generate(
            prompt=final_prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            num_inference_steps=num_steps,
            width=width,
            height=height,
            seed=seed_value
        )
        generation_time = time.time() - start_time
        
        # Sauvegarder l'image
        output_dir = get_output_path("portfolio")
        timestamp = int(time.time())
        filename = f"generated_{timestamp}.png"
        filepath = output_dir / filename
        image.save(filepath)
        
        # Calculer le score esthétique
        score = aesthetic_scorer.score(image)
        
        # Sauvegarder dans la base de données
        db = SessionLocal()
        try:
            ImageRepository.create(
                db=db,
                prompt=prompt,
                image_path=str(filepath),
                negative_prompt=negative_prompt if negative_prompt else None,
                optimized_prompt=optimized_prompt,
                guidance_scale=guidance_scale,
                num_inference_steps=num_steps,
                width=width,
                height=height,
                seed=seed_value,
                score=score,
                generation_time=generation_time,
                use_rl_optimization=use_rl_optimization,
            )
        except Exception as e:
            print(f"⚠️ Erreur lors de la sauvegarde en base de données: {e}")
        finally:
            db.close()
        
        # Info textuelle simplifiée
        quality_label = "Rapide" if temperature < 0.4 else "Équilibrée" if temperature < 0.7 else "Haute qualité"
        
        info_text = f"""
**✅ Image générée avec succès !**

**📝 Prompt :** {prompt}
**🌡️ Qualité :** {quality_label} (Température: {temperature:.1f})
**⏱️ Temps :** {generation_time:.1f} secondes
**⭐ Score esthétique :** {score:.2f}/10

{optimization_info}

💾 **Image sauvegardée automatiquement**
"""
        
        return image, info_text
        
    except Exception as e:
        error_text = f"❌ Erreur lors de la génération : {str(e)}"
        return None, error_text

def optimize_prompt_only(prompt: str, n_iterations: int = 10):
    """
    Optimise uniquement le prompt sans générer d'image.
    
    Args:
        prompt: Prompt de base à optimiser
        n_iterations: Nombre d'itérations d'optimisation
    
    Returns:
        str: Résultats de l'optimisation
    """
    try:
        rl_optimizer = get_rl_optimizer()
        result = rl_optimizer.optimize_prompt(
            base_prompt=prompt,
            n_iterations=n_iterations
        )
        
        info_text = f"""
**Optimisation RL terminée !**

**Résultats :**
- Prompt original : {result['original_prompt']}
- Prompt optimisé : {result['optimized_prompt']}
- Score original : {result['original_score']:.2f}
- Score optimisé : {result['optimized_score']:.2f}
- Amélioration : {result['improvement']:+.2f}
- Paramètres optimaux :
  - Guidance scale : {result['best_params']['guidance_scale']}
  - Steps : {result['best_params']['num_steps']}

**💡 Utilisez le prompt optimisé dans la génération d'image !**
"""
        return info_text
        
    except Exception as e:
        return f"❌ Erreur lors de l'optimisation : {str(e)}\n(Vérifiez que le modèle RL est entraîné : models/rl_agent.zip)"

# Interface Gradio
with gr.Blocks(title="AI Creative Studio", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🎨 AI Creative Studio
        
        **Générateur d'images IA simple et intuitif**
        
        Entrez votre prompt et ajustez la qualité avec le curseur de température. C'est tout !
        """
    )
    
    with gr.Tabs():
        # Tab 1: Génération d'images (simplifiée)
        with gr.Tab("🎨 Générer une Image"):
            with gr.Row():
                with gr.Column(scale=1):
                    prompt_input = gr.Textbox(
                        label="💬 Décrivez votre image",
                        placeholder="nano banana, highly detailed, studio lighting",
                        lines=3,
                        info="Exemples: 'nano banana', 'a cat in space', 'futuristic city'"
                    )
                    
                    temperature_slider = gr.Slider(
                        label="🌡️ Qualité (Température)",
                        minimum=0.0,
                        maximum=1.0,
                        value=0.7,
                        step=0.1,
                        info="0.0 = Rapide (30s) | 0.5 = Équilibré (1min) | 1.0 = Meilleure qualité (2-3min)"
                    )
                    
                    use_rl_opt = gr.Checkbox(
                        label="✨ Optimisation automatique du prompt (RL)",
                        value=False,
                        info="Améliore automatiquement votre prompt pour de meilleurs résultats"
                    )
                    
                    generate_btn = gr.Button("🎨 Générer", variant="primary", size="lg")
                
                with gr.Column(scale=1):
                    image_output = gr.Image(
                        label="Image générée",
                        type="pil",
                        height=500
                    )
                    info_output = gr.Markdown(label="Informations")
        
        # Tab 2: Optimisation de prompt
        with gr.Tab("🤖 Optimisation RL"):
            gr.Markdown(
                """
                ### Optimisez vos prompts avec l'agent RL
                
                Entrez un prompt simple et l'agent RL le transformera en prompt optimisé avec les meilleurs keywords et paramètres !
                """
            )
            
            with gr.Row():
                with gr.Column():
                    optimize_prompt_input = gr.Textbox(
                        label="Prompt à optimiser",
                        placeholder="a cat",
                        lines=2
                    )
                    optimize_iterations = gr.Slider(
                        label="Nombre d'itérations",
                        minimum=5,
                        maximum=20,
                        value=10,
                        step=1,
                        info="Plus d'itérations = meilleure optimisation mais plus lent"
                    )
                    optimize_btn = gr.Button("🚀 Optimiser", variant="primary")
                
                with gr.Column():
                    optimize_output = gr.Markdown(label="Résultats")
        
        # Tab 3: Historique
        with gr.Tab("📊 Historique"):
            gr.Markdown(
                """
                ### Historique des générations
                
                Consultez l'historique de toutes vos images générées avec leurs métadonnées.
                """
            )
            
            with gr.Row():
                with gr.Column():
                    history_limit = gr.Slider(
                        label="Nombre d'images à afficher",
                        minimum=5,
                        maximum=100,
                        value=20,
                        step=5
                    )
                    history_order = gr.Dropdown(
                        label="Trier par",
                        choices=["created_at", "score"],
                        value="created_at"
                    )
                    history_order_desc = gr.Checkbox(
                        label="Ordre décroissant",
                        value=True
                    )
                    history_btn = gr.Button("📊 Charger l'historique", variant="primary")
                
                with gr.Column():
                    history_output = gr.Markdown(label="Historique")
            
            def load_history(limit, order_by, order_desc):
                """Charge l'historique depuis la base de données"""
                db = SessionLocal()
                try:
                    images = ImageRepository.get_all(
                        db=db,
                        skip=0,
                        limit=int(limit),
                        order_by=order_by,
                        order_desc=order_desc
                    )
                    
                    if not images:
                        return "**Aucune image dans l'historique pour le moment.**"
                    
                    history_text = f"**📊 Historique ({len(images)} images)**\n\n"
                    history_text += "---\n\n"
                    
                    for img in images:
                        history_text += f"""
**Image #{img.id}** (Créée le {img.created_at.strftime('%Y-%m-%d %H:%M:%S')})
- **Prompt** : {img.prompt[:100]}{'...' if len(img.prompt) > 100 else ''}
- **Score** : {img.score:.2f}/10
- **Dimensions** : {img.width}x{img.height}
- **Steps** : {img.num_steps}
- **Guidance** : {img.guidance_scale}
- **RL Optimisé** : {'✅ Oui' if img.use_rl_optimization else '❌ Non'}
- **Chemin** : `{img.image_path}`

---
"""
                    return history_text
                except Exception as e:
                    return f"❌ Erreur lors du chargement de l'historique : {str(e)}"
                finally:
                    db.close()
            
            history_btn.click(
                fn=load_history,
                inputs=[history_limit, history_order, history_order_desc],
                outputs=[history_output]
            )
            
            # Statistiques
            gr.Markdown("### 📈 Statistiques")
            stats_btn = gr.Button("📊 Charger les statistiques")
            stats_output = gr.Markdown()
            
            def load_statistics():
                """Charge les statistiques depuis la base de données"""
                db = SessionLocal()
                try:
                    stats = ImageRepository.get_statistics(db=db)
                    
                    stats_text = f"""
**📈 Statistiques Globales**

- **Total d'images générées** : {stats['total_images']}
- **Score moyen** : {stats['average_score']:.2f}/10
- **Score maximum** : {stats['max_score']:.2f}/10
- **Score minimum** : {stats['min_score']:.2f}/10
- **Avec optimisation RL** : {stats['with_rl_optimization']}
- **Sans optimisation RL** : {stats['without_rl_optimization']}
"""
                    return stats_text
                except Exception as e:
                    return f"❌ Erreur lors du chargement des statistiques : {str(e)}"
                finally:
                    db.close()
            
            stats_btn.click(fn=load_statistics, outputs=[stats_output])
        
        # Tab 4: À propos
        with gr.Tab("ℹ️ À propos"):
            gr.Markdown(
                """
                ## 🤖 AI Creative Studio
                
                **Plateforme IA** qui génère automatiquement des artworks de haute qualité en combinant :
                - **Stable Diffusion** pour la génération d'images
                - **Agent RL** (PPO) pour optimiser les prompts et paramètres
                - **Aesthetic Scorer** pour évaluer la qualité des images
                
                ### 📋 Fonctionnalités
                
                1. **Génération d'images** : Créez des images à partir de prompts textuels
                2. **Optimisation RL** : Améliorez automatiquement vos prompts avec l'agent RL
                3. **Paramètres ajustables** : Contrôlez la qualité, la taille et les paramètres de génération
                
                ### 🚀 Utilisation Simple
                
                1. **Entrez votre prompt** - Décrivez l'image que vous voulez (ex: "nano banana")
                2. **Ajustez la qualité** - Utilisez le curseur de température (0.0 = rapide, 1.0 = meilleure qualité)
                3. **Activez l'optimisation RL** (optionnel) - Pour améliorer automatiquement votre prompt
                4. **Générez !** - Cliquez sur "Générer" et attendez
                
                ### 💡 Astuces
                
                - **Température basse (0.0-0.3)** : Rapide, idéale pour tester des idées (~30 secondes)
                - **Température moyenne (0.4-0.6)** : Bon compromis qualité/vitesse (~1 minute)
                - **Température haute (0.7-1.0)** : Meilleure qualité, plus lent (~2-3 minutes)
                - **Optimisation RL** : Activez-la pour de meilleurs résultats automatiques
                
                ### ⚠️ Note importante
                
                L'optimisation RL nécessite un modèle entraîné (`models/rl_agent.zip`).
                Si le modèle n'est pas disponible, vous pouvez quand même générer des images sans optimisation.
                
                Pour entraîner le modèle, voir `notebooks/colab_train_rl.ipynb` (Google Colab recommandé).
                """
            )
    
    # Events
    generate_btn.click(
        fn=generate_image,
        inputs=[
            prompt_input,
            temperature_slider,
            use_rl_opt
        ],
        outputs=[image_output, info_output]
    )
    
    optimize_btn.click(
        fn=optimize_prompt_only,
        inputs=[optimize_prompt_input, optimize_iterations],
        outputs=[optimize_output]
    )
    
    # Exemples
    gr.Examples(
        examples=[
            ["nano banana, highly detailed, studio lighting, macro photography", 0.8, False],
            ["a cat in space, astronaut suit, stars in background", 0.7, True],
            ["futuristic city at night, neon lights, cyberpunk style", 0.9, False],
            ["beautiful landscape with mountains and sunset, cinematic", 0.6, False],
        ],
        inputs=[
            prompt_input,
            temperature_slider,
            use_rl_opt
        ]
    )

if __name__ == "__main__":
    # Initialiser la base de données
    init_db()
    
    # Lancer l'interface Gradio
    demo.launch(
        server_name="0.0.0.0",  # Accessible depuis l'extérieur
        server_port=7860,       # Port par défaut de Gradio
        share=False             # Mettre à True pour créer un lien public
    )


@echo off
REM Script Windows pour entraîner l'agent RL localement
REM Usage: train_rl.bat [total_timesteps] [--fast_mode|--no-fast_mode]

echo ============================================================
echo 🚀 Entraînement RL Agent - Local (CPU)
echo ============================================================
echo.

REM Activer l'environnement virtuel
if exist .venv\Scripts\activate.bat (
    echo ✅ Activation de l'environnement virtuel...
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️  Environnement virtuel non trouvé (.venv\Scripts\activate.bat)
    echo 💡 Créez d'abord l'environnement : python -m venv .venv
    pause
    exit /b 1
)

REM Définir PYTHONPATH
set PYTHONPATH=%CD%
echo ✅ PYTHONPATH défini: %PYTHONPATH%
echo.

REM Vérifier les arguments
if "%1"=="" (
    set TIMESTEPS=2500
    echo 💡 Utilisation de la valeur par défaut: 2500 steps
) else (
    set TIMESTEPS=%1
    echo 📊 Steps d'entraînement: %TIMESTEPS%
)

REM Vérifier fast_mode
set FAST_MODE=--fast_mode
if "%2"=="--no-fast_mode" (
    set FAST_MODE=--no-fast_mode
    echo ⚠️  Mode rapide DÉSACTIVÉ (meilleure qualité mais plus lent)
) else (
    echo ⚡ Mode rapide ACTIVÉ (3-5x plus rapide)
)

echo.
echo ============================================================
echo 🚀 Démarrage de l'entraînement...
echo ============================================================
echo 💡 Vous pouvez arrêter avec Ctrl+C - checkpoints sauvegardés automatiquement
echo.

REM Lancer l'entraînement
python training\train_rl_agent.py --total_timesteps %TIMESTEPS% %FAST_MODE%

echo.
echo ============================================================
if exist models\rl_agent.zip (
    echo ✅ Entraînement terminé! Modèle sauvegardé: models\rl_agent.zip
) else (
    echo ⚠️  Modèle non trouvé. Vérifiez les erreurs ci-dessus.
)
echo ============================================================
pause


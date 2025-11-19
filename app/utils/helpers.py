import os
from pathlib import Path
from typing import Optional

def ensure_dir(path: str) -> Path:
    """Crée un dossier s'il n'existe pas."""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def get_output_path(subdir: str = "portfolio") -> Path:
    """Retourne le chemin du dossier de sortie."""
    from app.utils.config import settings
    output_dir = Path(settings.OUTPUT_DIR) / subdir
    ensure_dir(output_dir)
    return output_dir


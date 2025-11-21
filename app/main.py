from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.utils.config import settings
from app.database.database import init_db

# Créer l'application FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="AI Creative Studio - GenAI + RL for image generation"
)

# CORS (pour frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(router, prefix="/api/v1", tags=["generation"])

# Event handlers
@app.on_event("startup")
async def startup_event():
    """Actions au démarrage de l'API."""
    # Initialiser la base de données
    init_db()
    print(f"{settings.API_TITLE} v{settings.API_VERSION} starting...")
    print(f"Listening on {settings.API_HOST}:{settings.API_PORT}")
    print(f"Docs available at http://{settings.API_HOST}:{settings.API_PORT}/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Actions à l'arrêt de l'API."""
    print("👋 Shutting down AI Creative Studio...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True  # Development only
    )


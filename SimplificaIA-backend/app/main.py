from fastapi import FastAPI
from app.routes.simplify import router
from app.services.cache_service import get_cache_stats

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "API funcionando!"
    }

@app.get("/cache/stats")
def cache_stats():
    """Obter estatísticas do cache"""
    return get_cache_stats()
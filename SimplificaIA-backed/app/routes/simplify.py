from fastapi import APIRouter, HTTPException, Request
from app.models.request_models import SimplifyRequest
from app.services.gemini_service import simplify_text
from app.services.rate_limit_service import (
    check_limit,
    increment_usage,
    get_remaining_uses,
)
from app.services.cache_service import is_from_cache
import json

router = APIRouter()

@router.post("/simplify")
def simplify(data: SimplifyRequest, request: Request):
    # Obter IP do cliente
    client_ip = request.client.host
    
    # Verificar limite diário
    if not check_limit(client_ip):
        remaining = get_remaining_uses(client_ip)
        raise HTTPException(
            status_code=429,
            detail=f"Limite diário atingido (5 simplificações/dia). Tente novamente amanhã."
        )
    
    try:
        # Verificar se está em cache
        cached = is_from_cache(data.text, data.level)
        
        result = simplify_text(
            data.text,
            data.level
        )
        
        # Incrementar contador após sucesso
        increment_usage(client_ip)
        remaining = get_remaining_uses(client_ip)
        
        # Garantir que o resultado é uma string válida
        if not isinstance(result, str):
            result = str(result)
        
        # Retornar como JSON válido com info de limite e cache
        return {
            "result": result,
            "remaining_uses": remaining,
            "from_cache": cached
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao simplificar texto: {str(e)}"
        )
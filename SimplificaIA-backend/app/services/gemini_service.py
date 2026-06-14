from google import genai
from dotenv import load_dotenv
import os
import re
import json
from app.services.cache_service import get_cached_result, save_to_cache

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def simplify_text(text: str, level: str):
    # Verificar cache primeiro
    cached_result = get_cached_result(text, level)
    if cached_result:
        return cached_result
    
    # Adaptar prompt por nível
    level_instructions = {
        "fundamental": "Reescreva para crianças pequenas (6-9 anos). Use frases curtas, palavras simples, exemplos do dia a dia.",
        "medio": "Reescreva para adolescentes. Mantenha clareza, evite jargão técnico, seja direto e objetivo.",
        "tecnico": "Reescreva mantendo rigor técnico. Use terminologia apropriada, mantenha precisão científica."
    }
    
    level_instruction = level_instructions.get(level, level_instructions["fundamental"])
    
    prompt = f"""Você é um especialista em comunicação acessível e simplificação de textos.

Reescreva o texto abaixo com foco em clareza e compreensão:

Instruções:
- {level_instruction}
- Mantenha o significado original do texto
- Sem markdown, asteriscos ou formatação especial
- Retorne APENAS o texto reescrito, sem explicações
- Use linguagem natural e fluida

Texto original:
{text}

Texto simplificado:"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Obter texto da resposta
        result = response.text.strip() if response.text else ""
        
        # Limpar espaços em branco extras e quebras de linha desnecessárias
        result = re.sub(r'\s+', ' ', result)
        
        # Remover markdown se houver
        result = re.sub(r'\*\*|\*|__', '', result)
        result = re.sub(r'#+\s', '', result)
        
        # Remover caracteres problemáticos
        result = result.replace('|', '')
        
        # Garantir que é string válida UTF-8
        result = result.encode('utf-8', errors='ignore').decode('utf-8')
        
        # Salvar no cache
        save_to_cache(text, level, result)
        
        return result
    
    except Exception as e:
        return "O serviço de simplificação está temporariamente indisponível. Tente novamente mais tarde."



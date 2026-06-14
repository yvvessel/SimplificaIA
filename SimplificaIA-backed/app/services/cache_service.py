import sqlite3
import hashlib
from datetime import datetime, timedelta

CACHE_DB_PATH = "cache.db"
CACHE_TTL_DAYS = 30  # Cache válido por 30 dias

def init_cache_db():
    """Inicializar banco de cache"""
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS text_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_hash TEXT UNIQUE NOT NULL,
            original_text TEXT NOT NULL,
            level TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            hits INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def _hash_text(text: str, level: str) -> str:
    """Gerar hash do texto + nível para chave de cache"""
    combined = f"{text.strip()}|{level}"
    return hashlib.sha256(combined.encode()).hexdigest()

def get_cached_result(text: str, level: str) -> str | None:
    """Obter resultado do cache se existir e for válido"""
    init_cache_db()
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    
    text_hash = _hash_text(text, level)
    cutoff_date = datetime.now() - timedelta(days=CACHE_TTL_DAYS)
    
    cursor.execute("""
        SELECT result FROM text_cache
        WHERE text_hash = ? AND created_at > ?
    """, (text_hash, cutoff_date.isoformat()))
    
    result = cursor.fetchone()
    
    # Atualizar contador de hits
    if result:
        cursor.execute("""
            UPDATE text_cache 
            SET hits = hits + 1 
            WHERE text_hash = ?
        """, (text_hash,))
        conn.commit()
    
    conn.close()
    return result[0] if result else None

def is_from_cache(text: str, level: str) -> bool:
    """Verificar se resultado está em cache"""
    init_cache_db()
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    
    text_hash = _hash_text(text, level)
    cutoff_date = datetime.now() - timedelta(days=CACHE_TTL_DAYS)
    
    cursor.execute("""
        SELECT 1 FROM text_cache
        WHERE text_hash = ? AND created_at > ?
    """, (text_hash, cutoff_date.isoformat()))
    
    result = cursor.fetchone()
    conn.close()
    
    return result is not None

def save_to_cache(text: str, level: str, result: str) -> None:
    """Salvar resultado no cache"""
    init_cache_db()
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    
    text_hash = _hash_text(text, level)
    
    try:
        cursor.execute("""
            INSERT INTO text_cache (text_hash, original_text, level, result)
            VALUES (?, ?, ?, ?)
        """, (text_hash, text.strip(), level, result))
        conn.commit()
    except sqlite3.IntegrityError:
        # Já existe, apenas atualizar
        cursor.execute("""
            UPDATE text_cache 
            SET result = ? 
            WHERE text_hash = ?
        """, (result, text_hash))
        conn.commit()
    
    conn.close()

def get_cache_stats() -> dict:
    """Obter estatísticas do cache"""
    init_cache_db()
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM text_cache")
    total_entries = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(hits) FROM text_cache")
    total_hits = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        "total_cached_entries": total_entries,
        "total_hits": total_hits
    }

def clear_old_cache() -> None:
    """Limpar entradas expiradas do cache"""
    init_cache_db()
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    
    cutoff_date = datetime.now() - timedelta(days=CACHE_TTL_DAYS)
    cursor.execute("""
        DELETE FROM text_cache WHERE created_at < ?
    """, (cutoff_date.isoformat(),))
    
    conn.commit()
    conn.close()

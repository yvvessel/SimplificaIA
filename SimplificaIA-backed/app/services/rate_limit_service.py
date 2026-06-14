import sqlite3
from datetime import datetime, date
import os

DB_PATH = "usage.db"
DAILY_LIMIT = 5  # 5 simplificações por dia

def init_db():
    """Inicializar banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_ip TEXT NOT NULL,
            usage_date TEXT NOT NULL,
            count INTEGER DEFAULT 1,
            UNIQUE(client_ip, usage_date)
        )
    """)
    conn.commit()
    conn.close()

def get_daily_usage(client_ip: str) -> int:
    """Obter quantidade de usos hoje"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    today = str(date.today())
    cursor.execute(
        "SELECT count FROM daily_usage WHERE client_ip = ? AND usage_date = ?",
        (client_ip, today)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else 0

def check_limit(client_ip: str) -> bool:
    """Verificar se está dentro do limite"""
    return get_daily_usage(client_ip) < DAILY_LIMIT

def increment_usage(client_ip: str) -> int:
    """Incrementar contador de uso e retornar novo valor"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    today = str(date.today())
    
    cursor.execute(
        "SELECT count FROM daily_usage WHERE client_ip = ? AND usage_date = ?",
        (client_ip, today)
    )
    result = cursor.fetchone()
    
    if result:
        new_count = result[0] + 1
        cursor.execute(
            "UPDATE daily_usage SET count = ? WHERE client_ip = ? AND usage_date = ?",
            (new_count, client_ip, today)
        )
    else:
        new_count = 1
        cursor.execute(
            "INSERT INTO daily_usage (client_ip, usage_date, count) VALUES (?, ?, ?)",
            (client_ip, today, 1)
        )
    
    conn.commit()
    conn.close()
    
    return new_count

def get_remaining_uses(client_ip: str) -> int:
    """Obter quantidade de usos restantes"""
    current_usage = get_daily_usage(client_ip)
    return max(0, DAILY_LIMIT - current_usage)

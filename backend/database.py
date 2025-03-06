import sqlite3
import time

DB_FILE = "prices.db"

def create_tables():
    """ Crea la tabla si no existe """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skin_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skin_name TEXT,
        price REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_skin_price(skin_name, price):
    """ Guarda el precio de una skin en la base de datos """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO skin_prices (skin_name, price, timestamp) VALUES (?, ?, ?)",
                   (skin_name, price, time.strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()

def get_price_history(skin_name):
    """ Recupera el historial de precios de una skin """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp, price FROM skin_prices WHERE skin_name = ? ORDER BY timestamp DESC",
                   (skin_name,))

    data = cursor.fetchall()
    conn.close()

    return [{"date": row[0], "price": row[1]} for row in data]

# Crear la base de datos al iniciar el programa
create_tables()

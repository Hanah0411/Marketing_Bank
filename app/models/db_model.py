# =============================================
# 📁 Archivo: /app/models/db_model.py
# =============================================


import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        dbname=DB_CONFIG["dbname"],
        port=DB_CONFIG["port"]
    )



def find_client_by_features(data):
    """
    Busca un cliente existente en la tabla 'clients' basado en coincidencias simples.
    Retorna su id o None si no se encuentra.
    """
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """
        SELECT id FROM clients
        WHERE age = %s AND job = %s AND marital = %s AND education = %s
        ORDER BY created_at DESC LIMIT 1
    """
    values = (data["age"], data["job"], data["marital"], data["education"])
    cursor.execute(query, values)
    row = cursor.fetchone()
    conn.close()
    return row["id"] if row else None


def save_prediction(data, prediction, client_id=None):
    """
    Guarda una predicción en la tabla 'predictions', vinculada con client_id si existe.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO predictions (client_id, age, job, marital, education, balance, result, predicted_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        client_id,
        data.get("age"),
        data.get("job"),
        data.get("marital"),
        data.get("education"),
        data.get("balance"),
        prediction,
        datetime.now(),
    )

    cursor.execute(query, values)
    conn.commit()
    conn.close()
    print(f"💾 Predicción guardada (client_id={client_id}) resultado={prediction}")

# =============================================
# Archivo: /app/dashboards/db_utils.py
# =============================================
"""
Utilidades para consultar MySQL desde el dashboard.
Encapsula la conexión y retorna DataFrame con las predicciones.
"""

import psycopg2
from config import DB_CONFIG
import threading

# Almacenar conexiones activas
_active_connections = []
_connections_lock = threading.Lock()

def get_connection():
    """Obtiene una conexión y la registra para poder cerrarla después"""
    conn = psycopg2.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        dbname=DB_CONFIG["dbname"],
        port=DB_CONFIG["port"]
    )
    with _connections_lock:
        _active_connections.append(conn)
    return conn

def close_all_connections():
    """Cierra todas las conexiones activas"""
    with _connections_lock:
        while _active_connections:
            conn = _active_connections.pop()
            try:
                if not conn.closed:
                    conn.close()
            except:
                pass
import pandas as pd


def fetch_predictions(limit: int = None) -> pd.DataFrame:
    """
    Trae las predicciones desde la tabla 'predictions' y retorna un DataFrame.
    :param limit: si es None trae todo, sino los últimos N registros.
    """
    try:
        conn = get_connection()
    except Exception as e:
        # Retorna DataFrame vacío en caso de error de conexión
        print(f"⚠️ Error conexión BD en fetch_predictions: {e}")
        return pd.DataFrame()

    try:
        query = "SELECT id, age, job, marital, education, balance, result, predicted_at FROM predictions ORDER BY predicted_at DESC"
        if isinstance(limit, int):
            query = query + f" LIMIT {limit}"

        df = pd.read_sql(query, conn)
        conn.close()

        # Asegurar tipos
        if not df.empty:
            df["predicted_at"] = pd.to_datetime(df["predicted_at"], format="%Y-%m-%d %H:%M:%S.%f")
        return df

    except Exception as e:
        print(f"⚠️ Error ejecutando query en fetch_predictions: {e}")
        try:
            conn.close()
        except:
            pass
        return pd.DataFrame()


def fetch_with_truth() -> pd.DataFrame:
    """
    Une predicciones con la tabla de clientes para obtener el valor real
    :return: DataFrame con columnas ['predicted', 'actual'] donde ambas son 0/1
    """
    try:
        conn = get_connection()
    except Exception as e:
        print(f"⚠️ Error conexión BD en fetch_with_truth: {e}")
        return pd.DataFrame()

    try:
        query = (
            "SELECT p.result AS predicted, c.deposit AS actual "
            "FROM predictions p JOIN clients c ON p.client_id = c.id"
        )
        df = pd.read_sql(query, conn)
        conn.close()

        if not df.empty:
            # Normalizar a 0/1
            df['actual'] = df['actual'].map({'yes': 1, 'no': 0})
            df['predicted'] = df['predicted'].astype(int)
        return df

    except Exception as e:
        print(f"⚠️ Error ejecutando query en fetch_with_truth: {e}")
        try:
            conn.close()
        except:
            pass
        return pd.DataFrame()


# =============================================
# 📁 Archivo: /tests/test_db_connection.py
# =============================================

from app.models.db_model import get_connection

def test_connection():
    """
    Prueba la conexión a la base de datos e imprime el estado.
    """
    conn = get_connection()
    if conn:
        print("🔗 Conexión establecida correctamente.")
        conn.close()
    else:
        print("⚠️ No se pudo establecer la conexión.")

if __name__ == "__main__":
    test_connection()

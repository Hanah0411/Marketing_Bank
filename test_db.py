import psycopg2
from config import DB_CONFIG

def test_connection():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            dbname=DB_CONFIG["dbname"],
            port=DB_CONFIG["port"]
        )
        print("✅ Conexión exitosa a la base de datos")
        
        # Intentar crear las tablas si no existen
        cur = conn.cursor()
        with open('app/database/bank_marketing_schema.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
            # Eliminar el comando \c que no funciona en psycopg2
            sql = '\n'.join([line for line in sql.split('\n') if not line.strip().startswith('\\c')])
            cur.execute(sql)
        conn.commit()
        print("✅ Schema creado/verificado correctamente")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")

if __name__ == "__main__":
    test_connection()
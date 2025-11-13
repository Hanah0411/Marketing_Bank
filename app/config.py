# app/config.py
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Si no tienes DATABASE_URL (por si usas otro hosting), usa esto como fallback:
if not DATABASE_URL:
    DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}"

# Esto es lo que antes estaba en config.py
DB_CONFIG = {
    "database_url": DATABASE_URL
}
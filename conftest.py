import os
import sys

# Asegura que la raíz del proyecto esté en sys.path para que imports relativos
# como `from app.models.db_model import ...` funcionen cuando pytest
# recolecta tests que están dentro de paquetes (por ejemplo, app/tests).
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

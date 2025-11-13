# =============================================
#  Archivo: /app/main.py
# =============================================

"""
Archivo principal del proyecto FastAPI.
Monta las rutas y lanza la aplicación.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.predict_routes import router as predict_router
from app.routes.dashboard_routes import router as dashboard_router


# Crear aplicación FastAPI con metadatos
app = FastAPI(
    title="Bank Marketing Predictor (Local)",
    description=(
        "API local para predecir la aceptación de campañas bancarias.\n"
        "Documentación interactiva disponible en /docs"
    ),
    version="1.0.0",
    contact={"name": "Equipo de ML", "url": "https://github.com/yourusername/bank_marketing_local"},
)

# Orígenes permitidos para CORS (ej. Dash en 8050)
origins = [
    "http://localhost:8050",
    "http://127.0.0.1:8050",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(predict_router)
app.include_router(dashboard_router)


@app.get("/", tags=["Inicio"], summary="Endpoint de bienvenida")
def home():
    """Endpoint de bienvenida que confirma que la API está activa."""
    return {
        "message": "API de predicciones bancarias funcionando ",
        "docs": "Visita /docs para la documentación interactiva",
        "status": "ok",
    }

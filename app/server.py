# Lightweight ASGI server module for running the API separately from main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.predict_routes import router as predict_router
from app.routes.dashboard_routes import router as dashboard_router

# Crear aplicación FastAPI
app = FastAPI(
    title="Bank Marketing Predictor (Local)",
    description=(
        "API local para predecir la aceptación de campañas bancarias.\n"
        "Documentación interactiva disponible en /docs"
    ),
    version="1.0.0",
    contact={"name": "Equipo de ML", "url": "https://github.com/yourusername/bank_marketing_local"},
)

# Configurar CORS para Dash
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
    return {
        "message": "API de predicciones bancarias funcionando 🚀",
        "docs": "Visita /docs para la documentación interactiva",
        "health": "OK",
    }

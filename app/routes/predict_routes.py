# =============================================
# 📁 Archivo: /app/routes/predict_routes.py
# =============================================
"""
Define las rutas (endpoints) de la API para las predicciones.
"""
from fastapi import APIRouter, HTTPException
from app.controllers.predict_controller import make_prediction
from app.models.schemas import PredictionRequest, PredictionResponse

router = APIRouter(
    prefix="/api",
    tags=["predicción"],
    responses={404: {"description": "No encontrado"}},
)

@router.post("/predict", 
    response_model=PredictionResponse,
    summary="Predice si un cliente aceptará un depósito a plazo",
    description="""
    Predice la probabilidad de que un cliente acepte un depósito a plazo basado en sus características
    y el historial de contactos previos. Los datos son validados y preprocesados antes de la predicción.
    
    - Si el cliente existe en la base de datos, se vincula la predicción con su ID
    - Valores categóricos inválidos son rechazados con 422 Unprocessable Entity
    - Errores del modelo devuelven 500 Internal Server Error
    """,
    response_description="Predicción y mensaje explicativo"
)
async def predict(data: PredictionRequest) -> PredictionResponse:
    """
    Endpoint de predicción que valida datos de entrada usando Pydantic.
    
    Args:
        data: Datos del cliente y contacto actual validados por PredictionRequest
        
    Returns:
        PredictionResponse con predicción, mensaje y cliente vinculado si existe
        
    Raises:
        HTTPException: Si hay error al predecir o procesar datos
    """
    try:
        # PredictionRequest ya validó tipos/rangos; convertir a dict para procesar
        result = make_prediction(data.model_dump())
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar predicción: {str(e)}"
        )

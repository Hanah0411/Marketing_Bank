# =============================================
# 📁 Archivo: /app/routes/dashboard_routes.py
# =============================================
"""
Define las rutas (endpoints) de la API para el dashboard.
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import pandas as pd
from app.dashboards.db_utils import fetch_predictions, fetch_with_truth
from app.models.dashboard_schemas import DashboardMetrics, PredictionsList

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "No encontrado"}},
)

@router.get("/metrics", 
    response_model=DashboardMetrics,
    summary="Obtiene métricas generales del dashboard",
    description="Retorna métricas como total de predicciones, tasa de positivos y última actualización"
)
async def get_metrics() -> DashboardMetrics:
    try:
        df = fetch_predictions()
        total = int(df.shape[0]) if not df.empty else 0
        positive = int(df["result"].sum()) if not df.empty else 0
        positive_rate = round((positive / total) * 100, 2) if total > 0 else 0.0
        last_update = df["predicted_at"].max() if not df.empty else None
        
        # Calcular accuracy
        df_truth = fetch_with_truth()
        accuracy = 0
        if not df_truth.empty:
            accuracy = round((df_truth["predicted"] == df_truth["actual"]).mean() * 100, 2)
        
        return {
            "total": total,
            "positive": positive,
            "positive_rate": positive_rate,
            "accuracy": accuracy,
            "last_update": last_update
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener métricas: {str(e)}"
        )

@router.get("/predictions", 
    response_model=PredictionsList,
    summary="Obtiene lista de predicciones",
    description="Retorna las últimas predicciones realizadas con sus detalles"
)
async def get_predictions(limit: int = None) -> PredictionsList:
    try:
        df = fetch_predictions(limit)
        predictions = df.to_dict('records') if not df.empty else []
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener predicciones: {str(e)}"
        )

@router.get("/confusion-matrix",
    summary="Obtiene datos para la matriz de confusión",
    description="Retorna los datos necesarios para generar la matriz de confusión"
)
async def get_confusion_matrix():
    try:
        df_truth = fetch_with_truth()
        if df_truth.empty:
            return {"matrix": [[0, 0], [0, 0]]}
            
        confusion_data = pd.crosstab(
            df_truth["actual"], 
            df_truth["predicted"],
            rownames=["Actual"],
            colnames=["Predicho"]
        ).values.tolist()
        
        return {"matrix": confusion_data}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener matriz de confusión: {str(e)}"
        )
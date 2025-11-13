from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class DashboardMetrics(BaseModel):
    """Métricas generales para el dashboard"""
    total: int
    positive: int
    positive_rate: float
    accuracy: float
    last_update: Optional[datetime] = None

class PredictionRecord(BaseModel):
    """Registro individual de predicción para el dashboard"""
    id: int
    age: int
    job: str
    marital: str
    education: str
    balance: float
    result: int
    predicted_at: datetime

class PredictionsList(BaseModel):
    """Lista de predicciones para el dashboard"""
    predictions: List[PredictionRecord]
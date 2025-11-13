# =============================================
# Archivo: /app/dashboards/api_client.py
# =============================================
"""
Cliente para consumir la API desde el dashboard.
"""

import os
import requests
import pandas as pd
from typing import Dict, Any, Optional

class APIClient:
    def __init__(self):
        # En producción, esto vendría de variables de entorno
        self.base_url = "http://localhost:8000"
        
    def _get(self, endpoint: str) -> Dict[str, Any]:
        """Realiza una petición GET a la API."""
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error en petición API: {e}")
            return {}

    def get_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas generales del dashboard."""
        return self._get("/api/dashboard/metrics")

    def get_predictions(self, limit: Optional[int] = None) -> pd.DataFrame:
        """Obtiene predicciones y las convierte a DataFrame."""
        endpoint = "/api/dashboard/predictions"
        if limit:
            endpoint += f"?limit={limit}"
            
        data = self._get(endpoint)
        if not data or "predictions" not in data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data["predictions"])
        if not df.empty:
            df["predicted_at"] = pd.to_datetime(df["predicted_at"])
        return df

    def get_confusion_matrix(self) -> Dict[str, Any]:
        """Obtiene datos para la matriz de confusión."""
        return self._get("/api/dashboard/confusion-matrix")
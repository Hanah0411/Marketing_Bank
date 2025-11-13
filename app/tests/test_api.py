# =============================================
# 📁 Archivo: /tests/test_api.py
# =============================================
"""
Script de pruebas del endpoint /api/predict
Verifica validación de datos y predicciones.
"""

import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any

from app.main import app

# Crear el cliente de pruebas
client = TestClient(app)

# Fixture para datos válidos de prueba
@pytest.fixture
def valid_data() -> Dict[str, Any]:
    return {
        "age": 45,
        "job": "management",
        "marital": "married",
        "education": "tertiary",
        "default": "no",
        "balance": 1200.0,
        "housing": "yes",
        "loan": "no",
        "contact": "cellular",
        "day": 12,
        "month": "may",
        "duration": 300,
        "campaign": 2,
        "pdays": -1,
        "previous": 0,
        "poutcome": "unknown"
    }

# Casos de prueba para datos inválidos
invalid_test_cases = [
    ("edad_negativa", {"age": -1}, "Input should be greater than or equal to 18"),
    ("trabajo_invalido", {"job": "invalid_job"}, "Input should be 'admin.', 'blue-collar', 'entrepreneur'"),
    ("balance_muy_alto", {"balance": 2000000}, "Input should be less than or equal to 1000000"),
    ("dia_invalido", {"day": 32}, "Input should be less than or equal to 31"),
]

@pytest.mark.api
def test_api_health():
    """Verifica que la API esté funcionando."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.api
def test_valid_prediction(valid_data):
    """Prueba una predicción con datos válidos."""
    response = client.post("/api/predict", json=valid_data)
    assert response.status_code == 200
    result = response.json()
    assert "prediction" in result
    assert "probability" in result
    assert isinstance(result["prediction"], str)
    assert isinstance(result["probability"], float)

@pytest.mark.api
@pytest.mark.parametrize("case_name, invalid_value, expected_error", invalid_test_cases)
def test_invalid_predictions(valid_data, case_name, invalid_value, expected_error):
    """Prueba casos inválidos para verificar la validación."""
    # Crear una copia de los datos válidos y modificar el campo específico
    test_data = valid_data.copy()
    for key, value in invalid_value.items():
        test_data[key] = value
    
    response = client.post("/api/predict", json=test_data)
    assert response.status_code == 422  # Unprocessable Entity
    error_detail = response.json().get("detail", "")
    assert expected_error in str(error_detail), f"Error esperado no encontrado en la respuesta"

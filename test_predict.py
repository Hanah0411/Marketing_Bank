import requests
import json

# Datos de prueba
data = {
    "age": 35,
    "job": "entrepreneur",
    "marital": "married",
    "education": "tertiary",
    "default": "no",
    "balance": 5000,
    "housing": "yes",
    "loan": "no",
    "contact": "cellular",
    "day": 15,
    "month": "may",
    "duration": 250,
    "campaign": 1,
    "pdays": -1,
    "previous": 0,
    "poutcome": "unknown"
}

# Hacer la predicción
response = requests.post("http://localhost:8000/api/predict", json=data)
print("\n📊 Respuesta del servidor:")
print(json.dumps(response.json(), indent=2))
# =============================================
# 📁 Archivo: /app/tests/test_api_simple.py
# =============================================
"""
Script de prueba básica del endpoint /api/predict
"""

import requests
import json
import time

URL = "http://127.0.0.1:8000/api/predict"

# Caso de prueba válido con todos los campos requeridos
test_data = {
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

if __name__ == "__main__":
    print("🚀 Probando endpoint de predicción...")
    print("⏳ Esperando 3 segundos para que el servidor esté listo...")
    time.sleep(3)
    try:
        response = requests.post(URL, json=test_data)
        print(f"\n📊 Estado: {response.status_code}")
        print(f"📋 Respuesta:\n{json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ Test exitoso")
        else:
            print("\n❌ Test fallido")
            
    except Exception as e:
        print(f"\n❌ Error al ejecutar test: {str(e)}")
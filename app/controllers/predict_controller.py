# =============================================
# 📁 Archivo: /app/controllers/predict_controller.py
# =============================================

import pickle
import pandas as pd
from fastapi import HTTPException
from app.models.db_model import save_prediction, find_client_by_features
from app.services.data_preprocessing import ENCODERS_PATH, COLUMNS_PATH, DEFAULT_VALUES

MODEL_PATH = "app/models/model_dt.pkl"

# Cargar artefactos de preprocesamiento
try:
    with open("app/models/encoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)
    with open("app/models/feature_names.pkl", "rb") as f:
        feature_names = pickle.load(f)
    print("✅ Artefactos de preprocesamiento cargados")
except Exception as e:
    print("⚠️ Error al cargar artefactos de preprocesamiento:", e)
    label_encoders = None
    feature_names = None

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ Modelo cargado exitosamente desde", MODEL_PATH)
except Exception as e:
    print("❌ Error al cargar el modelo:", e)
    model = None

# Cargar artefactos de preprocesado (si existen)
try:
    with open("app/models/encoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)
except Exception:
    label_encoders = None

try:
    with open("app/models/default_values.pkl", "rb") as f:
        default_values = pickle.load(f)
except Exception:
    default_values = {}

try:
    with open("app/models/feature_names.pkl", "rb") as f:
        feature_names = pickle.load(f)
except Exception:
    feature_names = None


def make_prediction(data: dict):
    print("📥 Iniciando predicción con datos:", data)
    if model is None:
        print("❌ Error: Modelo no cargado")
        raise HTTPException(status_code=500, detail="Modelo no cargado o inválido.")
    if label_encoders is None or feature_names is None:
        print("❌ Error: Artefactos faltantes:", 
              f"label_encoders={'✓' if label_encoders else '❌'}, "
              f"feature_names={'✓' if feature_names else '❌'}")
        raise HTTPException(status_code=500, detail="Artefactos de preprocesamiento no disponibles.")

    try:
        # Convertir enums a strings
        processed_data = {}
        for key, value in data.items():
            processed_data[key] = str(value.value) if hasattr(value, 'value') else value
        # Completar valores faltantes con defaults
        for col in DEFAULT_VALUES:
            if col not in processed_data or processed_data[col] is None:
                processed_data[col] = DEFAULT_VALUES[col]

        # Crear DataFrame y aplicar transformaciones
        df = pd.DataFrame([processed_data])
        
        # Codificar variables categóricas usando los mismos encoders del entrenamiento
        for col in df.select_dtypes(include=["object"]).columns:
            if col in label_encoders:
                try:
                    df[col] = label_encoders[col].transform(df[col].astype(str))
                except ValueError as e:
                    # Si hay una categoría nueva, usar el valor por defecto
                    print(f"⚠️ Valor desconocido en columna {col}: {df[col].iloc[0]}")
                    df[col] = 0

        # Asegurar mismo orden de columnas que en entrenamiento, excluyendo 'deposit'
        feature_cols = [col for col in feature_names if col != 'deposit']
        df = df.reindex(columns=feature_cols, fill_value=0)
        
        # Predecir
        print("📊 DataFrame preparado:", df.head())
        print("🔍 Columnas disponibles:", df.columns.tolist())
        
        prediction_num = int(model.predict(df)[0])
        print("🎯 Predicción numérica:", prediction_num)
        prediction_str = "yes" if prediction_num == 1 else "no"
        
        # Intentar obtener probabilidades si el modelo lo soporta
        try:
            probability = float(model.predict_proba(df)[0][1])  # Probabilidad de clase positiva
            print("📈 Probabilidad:", probability)
        except (AttributeError, NotImplementedError) as e:
            print("⚠️ Modelo no soporta probabilidades:", str(e))
            # Si el modelo no soporta probabilidades, usar un valor por defecto
            probability = 1.0 if prediction_num == 1 else 0.0

        # Buscar cliente (si existe en tabla clients)
        client_id = find_client_by_features(data)

        save_prediction(data, prediction_num, client_id)

        msg = (
            "Cliente propenso a aceptar la campaña."
            if prediction_num == 1
            else "Cliente no propenso a aceptar la campaña."
        )
        
        try:
            return {
                "prediction": prediction_str,
                "probability": probability,
                "message": msg,
                "linked_client_id": client_id,
            }
        except Exception as e:
            print("❌ Error al construir respuesta:", str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Error al construir respuesta: {str(e)}"
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en predicción: {str(e)}")

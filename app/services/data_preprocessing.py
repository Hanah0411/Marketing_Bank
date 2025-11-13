# =============================================
# 📁 Archivo: /app/services/data_preprocessing.py
# =============================================
"""
Módulo de preprocesamiento del dataset Bank Marketing.
Encargado de limpiar, transformar y preparar los datos
para el modelo de Machine Learning.

También provee funciones para guardar/cargar artefactos
de preprocesamiento (encoders, valores por defecto, etc.)
para asegurar consistencia entre entrenamiento y predicción.
"""

import pandas as pd
import pickle
import os
from sklearn.preprocessing import LabelEncoder

# Valores por defecto para campos faltantes
DEFAULT_VALUES = {
    "age": 40,
    "job": "unknown",
    "marital": "unknown",
    "education": "unknown",
    "default": "no",
    "balance": 0,
    "housing": "no",
    "loan": "no",
    "contact": "unknown",
    "day": 15,
    "month": "may",
    "duration": 0,
    "campaign": 1,
    "pdays": -1,
    "previous": 0,
    "poutcome": "unknown"
}

# Rutas para artefactos de preprocesamiento
ARTIFACTS_PATH = "app/models/preprocessing"
ENCODERS_PATH = os.path.join(ARTIFACTS_PATH, "label_encoders.pkl")
COLUMNS_PATH = os.path.join(ARTIFACTS_PATH, "feature_columns.pkl")

def load_dataset(path: str) -> pd.DataFrame:
    """
    Carga el dataset CSV en un DataFrame de pandas.
    :param path: ruta al archivo CSV (ej. data/raw/bank.csv)
    :return: DataFrame con los datos cargados.
    """
    # Dejar que pandas detecte el separador por defecto (coma) en lugar de forzar '|'.
    # Algunos CSV vienen con comas, otros con punto y coma; si quieres detección automática
    # más robusta, podríamos usar sep=None y engine='python', pero por simplicidad
    # usamos el comportamiento por defecto (coma).
    df = pd.read_csv(path)
    print(f"✅ Dataset cargado correctamente: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpieza básica: elimina valores nulos, normaliza tipos de datos.
    """
    df = df.copy()
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(f"🧹 Limpieza completa. Registros restantes: {len(df)}")
    return df


def encode_categorical(df: pd.DataFrame):
    """
    Codifica variables categóricas usando LabelEncoder.

    Retorna:
      - df transformado
      - label_encoders: dict de LabelEncoder por columna
      - default_values: dict con el valor codificado más frecuente por columna (usado en inferencia para valores desconocidos)
    """
    df = df.copy()
    label_encoders = {}
    default_values = {}

    for col in df.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        # obtener valor más frecuente (raw) antes de transformar
        mode_raw = df[col].mode()[0] if not df[col].mode().empty else None
        le.fit(df[col].astype(str))
        df[col] = le.transform(df[col].astype(str))
        label_encoders[col] = le
        # calcular valor codificado por defecto (si mode_raw es None, usar 0)
        if mode_raw is not None:
            try:
                default_values[col] = int(le.transform([str(mode_raw)])[0])
            except Exception:
                default_values[col] = 0
        else:
            default_values[col] = 0

    print(f"🔢 Variables categóricas codificadas: {len(label_encoders)} columnas")
    return df, label_encoders, default_values


def preprocess_data(path: str):
    """
    Carga, limpia y transforma los datos del CSV.
    Retorna el dataset listo para entrenamiento.
    """
    df = load_dataset(path)
    df = clean_data(df)
    df, label_encoders, default_values = encode_categorical(df)
    feature_names = list(df.columns)
    return df, label_encoders, default_values, feature_names

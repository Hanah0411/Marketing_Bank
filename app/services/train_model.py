# =============================================
# 📁 Archivo: /app/services/train_model.py
# =============================================
"""
Entrenamiento del modelo de Árbol de Decisión.
Incluye división del dataset, evaluación y guardado del modelo.
"""

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datetime import datetime
import os

from app.services.data_preprocessing import preprocess_data

LOG_PATH = "logs/training.log"
MODEL_PATH = "app/models/model_dt.pkl"


def train_and_evaluate(df: pd.DataFrame):
    """
    Entrena y evalúa un modelo de Árbol de Decisión.
    Guarda el modelo y registra métricas.
    """
    # Separar características (X) y etiqueta (y)
    X = df.drop("deposit", axis=1)
    y = df["deposit"]

    # División en train y test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inicialización del modelo
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    # Predicciones
    y_pred = model.predict(X_test)

    # Métricas de rendimiento
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted")
    rec = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")

    # Registro en log
    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as log:
        log.write(f"\n==== Entrenamiento {datetime.now()} ====\n")
        log.write(f"Registros totales: {len(df)}\n")
        log.write(f"Accuracy: {acc:.4f}\nPrecision: {prec:.4f}\nRecall: {rec:.4f}\nF1: {f1:.4f}\n")

    # Guardar modelo entrenado
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("✅ Modelo entrenado y guardado en:", MODEL_PATH)
    print(f"📊 Métricas -> Accuracy: {acc:.3f} | Precision: {prec:.3f} | Recall: {rec:.3f} | F1: {f1:.3f}")


if __name__ == "__main__":
    # Determinar ruta del dataset (orden de prioridad):
    # 1) argumento de línea de comandos
    # 2) variable de entorno DATA_PATH
    # 3) valor por defecto 'data/raw/bank.csv'
    import sys

    cli_path = sys.argv[1] if len(sys.argv) > 1 else None
    env_path = os.environ.get("DATA_PATH")
    data_path = cli_path or env_path or "app/data/raw/bank.csv"

    print("🚀 Iniciando entrenamiento del modelo...")

    # Comprobar existencia del fichero y dar mensaje claro si falta
    if not os.path.exists(data_path):
        print("❌ Archivo de datos no encontrado:", data_path)
        print("Por favor coloca el CSV en esa ruta, o configura la variable de entorno DATA_PATH, o pasa la ruta como primer argumento.")
        print("Ejemplo (PowerShell):")
        print("  $env:DATA_PATH = 'C:\\ruta\\a\\bank.csv'; python -m app.services.train_model")
        print("  python -m app.services.train_model data/raw/bank.csv")
        sys.exit(1)

    df, label_encoders, default_values, feature_names = preprocess_data(data_path)
    # Guardar artefactos de preprocesado para inferencia
    try:
        import pickle
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        with open("app/models/encoders.pkl", "wb") as f:
            pickle.dump(label_encoders, f)
        with open("app/models/default_values.pkl", "wb") as f:
            pickle.dump(default_values, f)
        with open("app/models/feature_names.pkl", "wb") as f:
            pickle.dump(feature_names, f)
        print("✅ Artefactos de preprocesado guardados en app/models/")
    except Exception as e:
        print("❌ No se pudieron guardar artefactos de preprocesado:", e)

    train_and_evaluate(df)

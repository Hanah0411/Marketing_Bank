# =============================================
# Archivo: /app/dashboards/dashboard.py
# =============================================
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score
from app.dashboards.db_utils import get_connection, fetch_predictions
import requests  # Agregado para llamadas a la API

app = dash.Dash(__name__, title="Dashboard Bank Marketing", assets_folder="../../app/static")
server = app.server

def compute_metrics(df):
    total = int(df.shape[0]) if not df.empty else 0
    positive = int(df["result"].sum()) if not df.empty else 0
    positive_rate = round((positive / total) * 100, 2) if total > 0 else 0.0
    last_update = df["predicted_at"].max() if not df.empty else None
    return {"total": total, "positive": positive, "positive_rate": positive_rate, "last_update": last_update}

def fetch_with_truth():
    """Une predictions con clients para calcular accuracy."""
    conn = get_connection()
    query = """
        SELECT p.result AS predicted, c.deposit AS actual
        FROM predictions p
        JOIN clients c ON p.client_id = c.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    if not df.empty:
        df["actual"] = df["actual"].map({"yes": 1, "no": 0})
    return df

# Opciones para dropdowns basadas en el dataset UCI Bank Marketing
# === OPCIONES CORREGIDAS PARA EL MODELO ===
job_options = [
    {'label': 'Administrativo', 'value': 'admin.'},
    {'label': 'Obrero', 'value': 'blue-collar'},
    {'label': 'Empresario', 'value': 'entrepreneur'},
    {'label': 'Empleada doméstica', 'value': 'housemaid'},
    {'label': 'Gerencia', 'value': 'management'},
    {'label': 'Jubilado', 'value': 'retired'},
    {'label': 'Autónomo', 'value': 'self-employed'},
    {'label': 'Servicios', 'value': 'services'},
    {'label': 'Estudiante', 'value': 'student'},
    {'label': 'Técnico', 'value': 'technician'},
    {'label': 'Desempleado', 'value': 'unemployed'},
    {'label': 'Desconocido', 'value': 'unknown'}
]

marital_options = [
    {'label': 'Soltero/a', 'value': 'single'},
    {'label': 'Casado/a', 'value': 'married'},
    {'label': 'Divorciado/a', 'value': 'divorced'},
    {'label': 'Desconocido', 'value': 'unknown'}
]

education_options = [
    {'label': 'Primaria', 'value': 'primary'},
    {'label': 'Secundaria', 'value': 'secondary'},
    {'label': 'Terciaria / Universidad', 'value': 'tertiary'},
    {'label': 'Desconocido', 'value': 'unknown'}
]

yes_no_unknown = [
    {'label': 'Sí', 'value': 'yes'},
    {'label': 'No', 'value': 'no'},
    {'label': 'Desconocido', 'value': 'unknown'}
]

contact_options = [
    {'label': 'Celular', 'value': 'cellular'},
    {'label': 'Teléfono fijo', 'value': 'telephone'},
    {'label': 'Desconocido', 'value': 'unknown'}
]

month_options = [
    {'label': 'Enero', 'value': 'jan'}, {'label': 'Febrero', 'value': 'feb'},
    {'label': 'Marzo', 'value': 'mar'}, {'label': 'Abril', 'value': 'apr'},
    {'label': 'Mayo', 'value': 'may'}, {'label': 'Junio', 'value': 'jun'},
    {'label': 'Julio', 'value': 'jul'}, {'label': 'Agosto', 'value': 'aug'},
    {'label': 'Septiembre', 'value': 'sep'}, {'label': 'Octubre', 'value': 'oct'},
    {'label': 'Noviembre', 'value': 'nov'}, {'label': 'Diciembre', 'value': 'dec'}
]

poutcome_options = [
    {'label': 'Desconocido', 'value': 'unknown'},
    {'label': 'Otro', 'value': 'other'},
    {'label': 'Fracaso', 'value': 'failure'},
    {'label': 'Éxito', 'value': 'success'}
]

app.layout = html.Div([
    html.H1("📊 Dashboard: Predicciones y Rendimiento del Modelo"),
    html.Div([
        html.Div(id="card-total", style={"display": "inline-block", "width": "24%", "padding": "10px"}),
        html.Div(id="card-positive", style={"display": "inline-block", "width": "24%", "padding": "10px"}),
        html.Div(id="card-accuracy", style={"display": "inline-block", "width": "24%", "padding": "10px"}),
        html.Div(id="card-update", style={"display": "inline-block", "width": "24%", "padding": "10px"}),
    ]),
    html.Div([
        dcc.Graph(id="conf-matrix", style={"width": "48%", "display": "inline-block"}),
        dcc.Graph(id="hist-age", style={"width": "48%", "display": "inline-block"}),
    ]),
    html.Div([
        dcc.Graph(id="ts-predictions"),
    ]),
    html.Div([
        html.H3("Últimas predicciones"),
        dash_table.DataTable(id="table", page_size=8, style_table={"overflowX": "auto"})
    ]),
    # Nueva sección para inputs de UI
    html.Div([
        html.H3("Hacer una Nueva Predicción"),
        html.Div([
            html.Label("Edad (age):"),
            dcc.Input(id="input-age", type="number", value=30),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Trabajo (job):"),
            dcc.Dropdown(id="input-job", options=job_options, value="unknown"),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Estado civil (marital):"),
            dcc.Dropdown(id="input-marital", options=marital_options, value="single"),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Educación (education):"),
            dcc.Dropdown(id="input-education", options=education_options, value="unknown"),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Crédito en default (default):"),
            dcc.Dropdown(id="input-default", options=yes_no_unknown, value="no"),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Balance anual promedio (balance):"),
            dcc.Input(id="input-balance", type="number", value=0),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Préstamo de vivienda (housing):"),
            dcc.Dropdown(id="input-housing", options=yes_no_unknown, value="no"),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Préstamo personal (loan):"),
            dcc.Dropdown(id="input-loan", options=yes_no_unknown, value="no"),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Tipo de contacto (contact):"),
            dcc.Dropdown(id="input-contact", options=contact_options, value="unknown"),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Día del mes (day):"),
            dcc.Input(id="input-day", type="number", value=1, min=1, max=31),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Mes (month):"),
            dcc.Dropdown(id="input-month", options=month_options, value="may"),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Duración del contacto (duration, en segundos):"),
            dcc.Input(id="input-duration", type="number", value=0),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Contactos en esta campaña (campaign):"),
            dcc.Input(id="input-campaign", type="number", value=1),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Días desde último contacto anterior (pdays, -1 si no hubo):"),
            dcc.Input(id="input-pdays", type="number", value=-1),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Contactos previos (previous):"),
            dcc.Input(id="input-previous", type="number", value=0),
        ], style={"margin": "10px"}),
        html.Div([
            html.Label("Resultado de campaña anterior (poutcome):"),
            dcc.Dropdown(id="input-poutcome", options=poutcome_options, value="unknown"),
        ], style={"margin": "10px"}),
        html.Button("Predecir", id="predict-button", n_clicks=0, style={"margin": "10px"}),
        html.Div(id="prediction-output", style={"font-weight": "bold", "margin": "10px"}),
    ], style={"border": "1px solid #ccc", "padding": "20px", "margin-top": "20px"}),
    dcc.Interval(id="interval", interval=10000, n_intervals=0)  # Actualizar cada 30 segundos
])

@app.callback(
    [
        Output("card-total", "children"),
        Output("card-positive", "children"),
        Output("card-accuracy", "children"),
        Output("card-update", "children"),
        Output("conf-matrix", "figure"),
        Output("hist-age", "figure"),
        Output("ts-predictions", "figure"),
        Output("table", "data")
    ],
    [Input("interval", "n_intervals")]
)
def update_dashboard(n):
    try:
        df = fetch_predictions()
        metrics = compute_metrics(df)
        total_card = [html.H4("Total"), html.H2(metrics["total"])]
        pos_card = [html.H4("Positivos"), html.H2(metrics["positive"])]
        update_card = [html.H4("Última actualización"), html.P(str(metrics["last_update"]))]
        # Accuracy
        df_truth = fetch_with_truth()
        if not df_truth.empty:
            acc = round(accuracy_score(df_truth["actual"], df_truth["predicted"]) * 100, 2)
            cm = confusion_matrix(df_truth["actual"], df_truth["predicted"])
            cm_df = pd.DataFrame(cm, index=["No", "Sí"], columns=["Pred. No", "Pred. Sí"])
            cm_fig = px.imshow(cm_df, text_auto=True, color_continuous_scale="Blues", title="Matriz de confusión")
        else:
            acc = 0
            cm_fig = px.imshow([[0, 0], [0, 0]], text_auto=True, title="Sin datos")
        acc_card = [html.H4("Exactitud del modelo"), html.H2(f"{acc}%")]
        # Otras gráficas
        age_fig = px.histogram(df, x="age", nbins=20, title="Distribución de edades")
        ts_fig = px.line(df, x="predicted_at", y="result", title="Histórico de predicciones")
        table_data = df.sort_values("predicted_at", ascending=False).head(20).to_dict("records")
        return total_card, pos_card, acc_card, update_card, cm_fig, age_fig, ts_fig, table_data
    except Exception as e:
        print(f"Error en update_dashboard: {str(e)}")
        # Valores por defecto en caso de error
        total_card = [html.H4("Total"), html.H2("--")]
        pos_card = [html.H4("Positivos"), html.H2("--")]
        update_card = [html.H4("Última actualización"), html.P("Error de conexión")]
        acc = 0
        acc_card = [html.H4("Exactitud del modelo"), html.H2(f"{acc}%")]
        cm_fig = px.imshow([[0, 0], [0, 0]], text_auto=True, title="Error de conexión")
        age_fig = px.histogram([], title="Distribución de edades")
        ts_fig = px.line([], title="Histórico de predicciones")
        table_data = []
        return total_card, pos_card, acc_card, update_card, cm_fig, age_fig, ts_fig, table_data

# Nuevo callback para la predicción
@app.callback(
    Output("prediction-output", "children"),
    Input("predict-button", "n_clicks"),
    [
        State("input-age", "value"),
        State("input-job", "value"),
        State("input-marital", "value"),
        State("input-education", "value"),
        State("input-default", "value"),
        State("input-balance", "value"),
        State("input-housing", "value"),
        State("input-loan", "value"),
        State("input-contact", "value"),
        State("input-day", "value"),
        State("input-month", "value"),
        State("input-duration", "value"),
        State("input-campaign", "value"),
        State("input-pdays", "value"),
        State("input-previous", "value"),
        State("input-poutcome", "value"),
    ]
)
def make_prediction(n_clicks, age, job, marital, education, default, balance, housing, loan, contact, day, month, duration, campaign, pdays, previous, poutcome):
    if n_clicks < 1:
        return ""
    
    # Validar que todos los campos estén llenos
    if any(v is None for v in [age, job, marital, education, default, balance, housing, loan, contact, day, month, duration, campaign, pdays, previous, poutcome]):
        return "Por favor, completa todos los campos."
    
    data = {
        "age": age,
        "job": job,
        "marital": marital,
        "education": education,
        "default": default,
        "balance": balance,
        "housing": housing,
        "loan": loan,
        "contact": contact,
        "day": day,
        "month": month,
        "duration": duration,
        "campaign": campaign,
        "pdays": pdays,
        "previous": previous,
        "poutcome": poutcome,
    }
    
    try:
        # Ajusta la URL si el endpoint o puerto es diferente
        response = requests.post("http://localhost:8000/api/predict", json=data)
        if response.status_code == 200:
            result = response.json()
            # Asume que la respuesta tiene un campo 'prediction' o 'result' con 0/1
            prediction = result.get("prediction") or result.get("result")
            return f"Predicción: {'Sí (aceptará el depósito)' if prediction == 1 else 'No (no aceptará el depósito)'}"
        else:
            return f"Error en la predicción: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def cleanup():
    """Limpia las conexiones al cerrar"""
    print("\n🔄 Cerrando conexiones...")
    try:
        # Cerrar cualquier conexión pendiente
        from app.dashboards.db_utils import close_all_connections
        close_all_connections()
    except:
        pass
    print("✅ Conexiones cerradas")

if __name__ == "__main__":
    import signal
    import sys
    def signal_handler(sig, frame):
        print("\n⚡ Señal de interrupción recibida")
        cleanup()
        sys.exit(0)
    # Registrar el manejador para SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
   
    try:
        print("🚀 Iniciando dashboard... (Presiona Ctrl+C para detener)")
        app.run(debug=True, port=8050)
    except KeyboardInterrupt:
        print("\n⚡ Interrupción de teclado detectada")
        cleanup()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        cleanup()
    finally:
        print("👋 Dashboard detenido")
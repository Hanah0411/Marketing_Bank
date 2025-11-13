# =============================================
# 📁 Archivo: /app/dashboards/components/distribution_plots.py
# =============================================
"""
Componente de gráficos de distribución para el dashboard
"""

import plotly.express as px
from dash import html, dcc

def create_balance_distribution(df):
    """Crea histograma de distribución de balance"""
    fig = px.histogram(
        df, 
        x="balance",
        nbins=30,
        title="Distribución de Balance Económico",
        labels={"balance": "Balance (€)", "count": "Frecuencia"}
    )
    return fig

def create_duration_distribution(df):
    """Crea histograma de duración de llamadas"""
    fig = px.histogram(
        df,
        x="duration",
        nbins=30,
        title="Distribución de Duración de Llamadas",
        labels={"duration": "Duración (segundos)", "count": "Frecuencia"}
    )
    return fig

def create_job_distribution(df):
    """Crea gráfico circular de distribución por trabajo"""
    job_counts = df["job"].value_counts()
    fig = px.pie(
        values=job_counts.values,
        names=job_counts.index,
        title="Distribución por Tipo de Trabajo"
    )
    return fig

def create_education_distribution(df):
    """Crea gráfico circular de distribución por educación"""
    education_counts = df["education"].value_counts()
    fig = px.pie(
        values=education_counts.values,
        names=education_counts.index,
        title="Distribución por Nivel Educativo"
    )
    return fig

def add_distribution_plots():
    """Agrega gráficos de distribución al dashboard"""
    return html.Div([
        html.H3("Análisis de Distribuciones", className="dashboard-title"),
        html.Div([
            # Distribución de Balance
            html.Div([
                dcc.Graph(id='balance-dist')
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            # Distribución de Duración
            html.Div([
                dcc.Graph(id='duration-dist')
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            # Distribución por Trabajo
            html.Div([
                dcc.Graph(id='job-dist')
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            # Distribución por Educación
            html.Div([
                dcc.Graph(id='education-dist')
            ], style={'width': '48%', 'display': 'inline-block'})
        ])
    ])
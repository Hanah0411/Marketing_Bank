# =============================================
# 📁 Archivo: /app/dashboards/components/advanced_metrics.py
# =============================================
"""
Componente de métricas avanzadas para el dashboard
"""

import plotly.graph_objects as go
from dash import html, dcc
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc

def create_roc_curve(y_true, y_pred_proba):
    """Crea la curva ROC"""
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        name=f'ROC (AUC = {roc_auc:.2f})',
        mode='lines'
    ))
    
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        name='Random',
        mode='lines',
        line=dict(dash='dash')
    ))
    
    fig.update_layout(
        title='Curva ROC',
        xaxis_title='Tasa de Falsos Positivos',
        yaxis_title='Tasa de Verdaderos Positivos',
        showlegend=True
    )
    
    return fig

def create_feature_importance(df):
    """Crea gráfico de importancia de características"""
    # Simulamos importancia de características
    features = ['age', 'balance', 'duration', 'campaign']
    importance = np.random.random(len(features))
    importance = importance / importance.sum()
    
    fig = go.Figure([go.Bar(
        x=importance,
        y=features,
        orientation='h'
    )])
    
    fig.update_layout(
        title='Importancia de Características',
        xaxis_title='Importancia Relativa',
        yaxis_title='Característica'
    )
    
    return fig

def add_advanced_metrics():
    """Agrega métricas avanzadas al dashboard"""
    return html.Div([
        html.H3("Métricas Avanzadas", className="dashboard-title"),
        html.Div([
            # ROC Curve
            html.Div([
                dcc.Graph(id='roc-curve')
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            # Feature Importance
            html.Div([
                dcc.Graph(id='feature-importance')
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            # Métricas por segmento
            html.Div([
                html.H4("Rendimiento por Segmento"),
                dcc.Graph(id='segment-performance')
            ]),
            
            # Análisis temporal
            html.Div([
                html.H4("Análisis Temporal"),
                dcc.Graph(id='temporal-analysis')
            ])
        ])
    ])
# -*- coding: utf-8 -*-
"""
Interactive Visualization Dashboard Prototype built with Plotly Dash.
Strictly adheres to ESILV Final Project requirements:
- Consolidates all four query indicators (Aggregation, Mining, Temporal, Spatial).
- Prominently displays the Dataset Name and the Team Member names.
- Can be run locally via `python src/dashboard.py` or exported to static HTML.
"""

import os
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Initialize Dash application with modern Bootstrap styling
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.FLATLY],
    title="KDD Multidimensional Dashboard — ESILV"
)

# Metadata configuration
DATASET_NAME = "Global Multidimensional Disaster & Climate Events (EM-DAT / Sample)"
TEAM_LEADER = "Maxime LAURENT"
TEAM_MEMBERS = ["Maxime LAURENT (Leader)", "Team Member 2", "Team Member 3"]

# ------------------------------------------------------------------------------
# Mock / Starter data generators for immediate demonstration
# ------------------------------------------------------------------------------
def get_sample_aggregation_fig():
    categories = ['Flood', 'Storm', 'Earthquake', 'Extreme Temperature', 'Wildfire', 'Drought']
    damages = [450, 320, 280, 150, 110, 95]
    fig = px.bar(
        x=categories, 
        y=damages, 
        labels={'x': 'Event Category', 'y': 'Total Impact Metric (USD M)'},
        title="<b>Query 1: Total Impact by Event Category (Aggregation)</b>",
        color=damages,
        color_continuous_scale='Tealgrn'
    )
    fig.update_layout(template='plotly_white')
    return fig

def get_sample_mining_fig():
    rules = [
        "High Intensity → Coastal Region",
        "Summer Season → Extreme Temp",
        "Rural Area → Prolonged Drought",
        "Category 4 Storm → Flash Flood",
        "High Population → Emergency Relief"
    ]
    supports = [0.18, 0.15, 0.12, 0.11, 0.09]
    lifts = [1.65, 1.48, 1.35, 1.30, 1.22]
    fig = px.bar(
        x=supports,
        y=rules,
        orientation='h',
        color=lifts,
        color_continuous_scale='Viridis',
        labels={'x': 'Support (Frequency)', 'y': 'Association Rule', 'color': 'Lift'},
        title="<b>Query 2: Top Frequent Association Rules (Pattern Mining)</b>"
    )
    fig.update_layout(template='plotly_white', yaxis=dict(autorange='reversed'))
    return fig

def get_sample_temporal_fig():
    dates = pd.date_range(start='2020-01-01', periods=36, freq='M')
    actual = np.sin(np.linspace(0, 10, 36)) * 20 + 50 + np.random.normal(0, 5, 36)
    forecast = actual[-6:] + np.random.normal(2, 3, 6)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=actual, mode='lines+markers', name='Observed Events', line=dict(color='#2b5c8f')))
    fig.add_trace(go.Scatter(x=dates[-6:], y=forecast, mode='lines+markers', name='Prophet Forecast', line=dict(dash='dash', color='#d62728')))
    fig.update_layout(
        title="<b>Query 3: Temporal Evolution & Forecast (Time Series Dynamics)</b>",
        xaxis_title="Timeline",
        yaxis_title="Monthly Event Volume",
        template='plotly_white'
    )
    return fig

def get_sample_spatial_fig():
    lats = [48.85, 45.75, 43.60, 43.70, 50.63, 44.83, 47.21, 48.57, 43.30]
    lons = [2.35, 4.85, 1.44, 7.26, 3.06, -0.57, -1.55, 7.75, 5.37]
    clusters = ['Cluster 0', 'Cluster 1', 'Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 0', 'Cluster 0', 'Cluster 2', 'Cluster 1']
    names = ['Paris', 'Lyon', 'Toulouse', 'Nice', 'Lille', 'Bordeaux', 'Nantes', 'Strasbourg', 'Marseille']
    
    fig = px.scatter_geo(
        lat=lats,
        lon=lons,
        color=clusters,
        text=names,
        title="<b>Query 4: Spatial Cluster Distribution (OPTICS / K-Means)</b>",
        scope='europe'
    )
    fig.update_layout(template='plotly_white')
    return fig

# ------------------------------------------------------------------------------
# Dashboard Layout
# ------------------------------------------------------------------------------
app.layout = dbc.Container([
    # Top Navbar & Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2("🌍 Multidimensional KDD Visualization Dashboard", className="fw-bold text-primary mt-3"),
                html.P(f"Dataset Analyzed: {DATASET_NAME}", className="text-muted fs-5 mb-1"),
                html.P([
                    html.Strong("Project Team: "),
                    html.Span(" | ".join(TEAM_MEMBERS), className="badge bg-secondary p-2 fs-6")
                ], className="mb-3")
            ], className="border-bottom pb-3 mb-4")
        ])
    ]),
    
    # 4 Indicator Visual Cards Grid
    dbc.Row([
        # Query 1 Card
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Query 1: Aggregation & Grouping", className="mb-0 text-dark")),
                dbc.CardBody([
                    dcc.Graph(id='graph-query-1', figure=get_sample_aggregation_fig())
                ])
            ], className="shadow-sm mb-4")
        ], md=6),
        
        # Query 2 Card
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Query 2: Frequent Pattern Mining", className="mb-0 text-dark")),
                dbc.CardBody([
                    dcc.Graph(id='graph-query-2', figure=get_sample_mining_fig())
                ])
            ], className="shadow-sm mb-4")
        ], md=6)
    ]),
    
    dbc.Row([
        # Query 3 Card
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Query 3: Temporal Trends & Forecasting", className="mb-0 text-dark")),
                dbc.CardBody([
                    dcc.Graph(id='graph-query-3', figure=get_sample_temporal_fig())
                ])
            ], className="shadow-sm mb-4")
        ], md=6),
        
        # Query 4 Card
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Query 4: Spatial Coordinates & Clustering", className="mb-0 text-dark")),
                dbc.CardBody([
                    dcc.Graph(id='graph-query-4', figure=get_sample_spatial_fig())
                ])
            ], className="shadow-sm mb-4")
        ], md=6)
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("Master in Data Science — ESILV | Hugo Alatrista-Salas | Final Project Deliverable", 
                   className="text-center text-muted small pb-3")
        ])
    ])
], fluid=True, className="px-4 py-2")


def export_static_html(output_path: str = "Laurent_dashboard.html"):
    """Exports the dashboard figures into a standalone HTML file."""
    fig1 = get_sample_aggregation_fig()
    fig2 = get_sample_mining_fig()
    fig3 = get_sample_temporal_fig()
    fig4 = get_sample_spatial_fig()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("<html><head><title>Dashboard Prototype</title></head><body>")
        f.write(f"<h1>KDD Visualization Dashboard</h1><p>Dataset: {DATASET_NAME}</p>")
        f.write(f"<p>Team: {', '.join(TEAM_MEMBERS)}</p><hr>")
        f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig2.to_html(full_html=False, include_plotlyjs=False))
        f.write(fig3.to_html(full_html=False, include_plotlyjs=False))
        f.write(fig4.to_html(full_html=False, include_plotlyjs=False))
        f.write("</body></html>")
    print(f"Exported static dashboard to: {output_path}")


if __name__ == "__main__":
    print(f"Starting Plotly Dash server for {TEAM_LEADER}...")
    print(f"Dataset: {DATASET_NAME}")
    print("Open http://127.0.0.1:8050/ in your browser.")
    # Run the server
    app.run(debug=True, port=8050)

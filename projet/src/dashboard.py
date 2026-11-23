# Interactive Plotly Dash dashboard prototype for the Final Project
# Owner: Louis Le Forestier
# Displays all 4 analytical queries + External Tourism Bonus, team members, and dataset titles

import os
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# Project metadata (mandatory on the dashboard per Final_project.pdf)
PROJECT_TITLE = "Global Shark Attacks Analysis & International Tourism Risk"
DATASET_NAMES = (
    "Primary: Global Shark Attack (GSAF - Kaggle mexwell) | "
    "External Bonus: International Tourism Arrivals (World Bank ST.INT.ARVL)"
)
TEAM_MEMBERS = [
    "Maxime Laurent (Team Leader)",
    "Louis Le Forestier",
    "Baptiste Noailhac",
    "Romain Thepaut",
]


# Function for creating a placeholder Plotly figure while queries are still TODO
# Input: title (str) - placeholder chart title
# Output: Plotly Figure displaying a clean TODO message
def create_placeholder_figure(title):
    fig = go.Figure()
    fig.add_annotation(
        text=f"TODO: connect finalized chart for '{title}'",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=15, color="#334155"),
    )
    fig.update_layout(
        title=title,
        template="plotly_white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=380,
    )
    return fig


# Function for building the interactive Python Dash application
# Input: figures_dict (dict) - dictionary of Plotly figures from indicators.py
# Output: configured Dash app instance
def create_dash_app(figures_dict=None):
    if figures_dict is None:
        figures_dict = {}

    # Retrieve figures or fall back to clean TODO placeholders
    fig_q1 = figures_dict.get("query1_grouping", create_placeholder_figure("Query 1: Grouping & Fatality Rates"))
    fig_q2 = figures_dict.get("query2_apriori", create_placeholder_figure("Query 2: Frequent Pattern Mining (Apriori)"))
    fig_q3 = figures_dict.get("query3_forecast", create_placeholder_figure("Query 3: Temporal Seasonality & Prophet Forecast"))
    fig_q4 = figures_dict.get("query4_spatial", create_placeholder_figure("Query 4: Spatial Hotspot Clustering"))
    fig_bonus = figures_dict.get("bonus_tourism", create_placeholder_figure("Bonus: Shark Attacks vs. International Tourism"))

    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.FLATLY],
        title="Global Shark Attacks KDD Dashboard - ESILV",
    )

    # TODO (Louis): add interactive filters (year range slider, country dropdown, activity filter)
    # and register Dash @app.callback functions once indicators.py is finalized
    app.layout = dbc.Container(
        [
            # Mandatory Header: Project title, Team Members, and Dataset Names
            dbc.Row(
                dbc.Col(
                    html.Div(
                        [
                            html.H2(PROJECT_TITLE, className="mb-1"),
                            html.P(DATASET_NAMES, className="text-muted mb-1"),
                            html.Small(
                                "Team Members: " + " | ".join(TEAM_MEMBERS),
                                className="fw-bold text-secondary",
                            ),
                        ],
                        className="p-3 my-3 bg-light border rounded",
                    )
                )
            ),
            # 5 Tabs organizing the 4 queries + External Bonus Dataset
            dcc.Tabs(
                [
                    dcc.Tab(label="1. Grouping & Fatality Rates", children=[dcc.Graph(figure=fig_q1)]),
                    dcc.Tab(label="2. Frequent Patterns (Apriori)", children=[dcc.Graph(figure=fig_q2)]),
                    dcc.Tab(label="3. Temporal & Prophet Forecast", children=[dcc.Graph(figure=fig_q3)]),
                    dcc.Tab(label="4. Spatial Hotspots", children=[dcc.Graph(figure=fig_q4)]),
                    dcc.Tab(label="5. Tourism Bonus (+1 pt)", children=[dcc.Graph(figure=fig_bonus)]),
                ]
            ),
        ],
        fluid=True,
    )
    return app


# Function for exporting all dashboard figures to a standalone offline HTML proof file
# Input: figures_dict (dict), output_path (str) - path to rendu/Laurent_dashboard.html
# Output: output_path (str) of the written HTML file
def export_dashboard_html(figures_dict, output_path):
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # TODO (Louis): enhance HTML layout with KPI cards and Markdown summaries
    sections = []
    for key, fig in figures_dict.items():
        sections.append(f"<section style='margin-bottom:32px;'>{fig.to_html(full_html=False, include_plotlyjs='cdn')}</section>")

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{PROJECT_TITLE}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 24px; color: #0F172A; }}
        header {{ background: #F8FAFC; border: 1px solid #CBD5E1; padding: 16px; border-radius: 6px; margin-bottom: 24px; }}
    </style>
</head>
<body>
    <header>
        <h1>{PROJECT_TITLE}</h1>
        <p><strong>Datasets:</strong> {DATASET_NAMES}</p>
        <p><strong>Team:</strong> {" | ".join(TEAM_MEMBERS)}</p>
    </header>
    {''.join(sections)}
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
    return output_path


if __name__ == "__main__":
    import sys
    src_dir = os.path.dirname(os.path.abspath(__file__))
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    from data_loader import load_shark_data, load_tourism_data, clean_shark_data, clean_and_merge_tourism
    from indicators import (
        query_grouping_analysis,
        query_frequent_patterns,
        query_temporal_forecast,
        query_spatial_clustering,
        query_tourism_enrichment
    )
    import pandas as pd

    shark_path = os.path.join(src_dir, "../data/attacks.csv")
    tourism_path = os.path.join(src_dir, "../data/tourism_arrivals.csv")
    geo_path = os.path.join(src_dir, "../data/locations_geocoded.csv")

    figures = {}
    if os.path.exists(shark_path):
        print("Loading and cleaning datasets for dashboard...")
        shark = clean_shark_data(load_shark_data(shark_path))
        print("Computing Query 1...")
        r1 = query_grouping_analysis(shark)
        print("Computing Query 2...")
        r2 = query_frequent_patterns(shark)
        print("Computing Query 3...")
        r3 = query_temporal_forecast(shark)
        figures["query1_grouping"] = r1["fig_countries"]
        figures["query2_apriori"] = r2["fig_rules"]
        figures["query3_forecast"] = r3["fig_forecast"]

        if os.path.exists(geo_path):
            print("Computing Query 4...")
            geo = pd.read_csv(geo_path)
            r4 = query_spatial_clustering(shark, geo)
            figures["query4_spatial"] = r4["fig_map"]

        if os.path.exists(tourism_path):
            print("Computing Bonus Query...")
            tourism = load_tourism_data(tourism_path)
            merged = clean_and_merge_tourism(shark, tourism)
            r5 = query_tourism_enrichment(merged)
            figures["bonus_tourism"] = r5["fig_trends"]

    # Export static proof to protect against -2 pts penalty
    proof_path = os.path.join(src_dir, "../../rendu/Laurent_dashboard.html")
    export_dashboard_html(figures, proof_path)
    print(f"Exported static dashboard proof to: {proof_path}")

    app = create_dash_app(figures)
    print("Starting Dash server at http://127.0.0.1:8050/")
    app.run(debug=False, port=8050)

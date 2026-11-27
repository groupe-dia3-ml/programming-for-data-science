# Interactive Plotly Dash dashboard prototype for the Final Project
# Owner: Louis Le Forestier
# Displays all 4 analytical queries + External Tourism Bonus, dynamic KPIs, interactive filters, team members, and dataset titles

import base64
import os
from pathlib import Path
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import requests


# Project metadata (mandatory on the dashboard per Final_project.pdf)
PROJECT_TITLE = "Reported Shark Incidents and International Tourism"
DATASET_NAMES = (
    "Primary: Global Shark Attack (GSAF - Kaggle / sharkattackfile.net) | "
    "External Bonus: International Tourism Arrivals (World Bank ST.INT.ARVL)"
)
TEAM_MEMBERS = [
    "Maxime Laurent (Team Leader)",
    "Louis Le Forestier",
    "Baptiste Noailhac",
    "Romain Thepaut",
]


# Function for dynamically computing headline KPI metrics from cleaned data and bonus results
# Input: clean_sharks (pd.DataFrame), bonus_results (dict)
# Output: dictionary of formatted KPI values and subtitles
def compute_dashboard_kpis(clean_sharks, bonus_results):
    total_incidents = int(len(clean_sharks))
    fatal_count = int((clean_sharks["Fatal_clean"] == "Y").sum())
    fatality_rate = round((fatal_count / total_incidents) * 100, 1) if total_incidents > 0 else 0.0
    min_year = int(clean_sharks["Year"].min())
    max_year = int(clean_sharks["Year"].max())

    top_country = clean_sharks["Country_clean"].value_counts().index[0]
    top_country_count = int(clean_sharks["Country_clean"].value_counts().iloc[0])
    top_country_share = round((top_country_count / total_incidents) * 100, 1)

    comp = bonus_results["country_comparison"].sort_values("attacks_per_1M_tourists", ascending=False)
    highest_risk_country = str(comp.iloc[0]["Country_clean"])
    highest_risk_rate = float(comp.iloc[0]["attacks_per_1M_tourists"])
    us_rows = comp[comp["Country_clean"] == "United States"]
    us_rate = float(us_rows.iloc[0]["attacks_per_1M_tourists"]) if len(us_rows) > 0 else 0.0

    return {
        "total_incidents": f"{total_incidents:,}",
        "year_window": f"Modern window: {min_year} - {max_year}",
        "fatality_rate": f"{fatality_rate} %",
        "fatal_subtitle": f"{fatal_count:,} fatal outcomes documented",
        "top_country": top_country,
        "top_country_subtitle": f"{top_country_count:,} attacks ({top_country_share} % of total)",
        "highest_risk_label": f"{highest_risk_country} ({highest_risk_rate:.2f})",
        "highest_risk_subtitle": f"Reports / 1M arrivals (US {us_rate:.2f})",
        "pearson_r": round(float(bonus_results["pearson_corr"]), 4),
    }


# Function for building the interactive Python Dash application with dynamic KPIs and filter callbacks
# Input: figures_dict (dict), kpis (dict), clean_sharks (pd.DataFrame or None), geo_df (pd.DataFrame or None)
# Output: configured Dash app instance
def create_dash_app(figures_dict=None, kpis=None, clean_sharks=None, geo_df=None):
    if figures_dict is None:
        figures_dict = {}
    if kpis is None:
        kpis = {
            "total_incidents": "N/A",
            "year_window": "Load dataset",
            "fatality_rate": "N/A",
            "fatal_subtitle": "",
            "top_country": "N/A",
            "top_country_subtitle": "",
            "highest_risk_label": "N/A",
            "highest_risk_subtitle": "",
            "pearson_r": 0.0,
        }

    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.FLATLY],
        title="Global Shark Attacks KDD Dashboard - ESILV",
    )

    # Filter options derived dynamically from clean_sharks if provided
    if clean_sharks is not None and len(clean_sharks) > 0:
        min_yr = int(clean_sharks["Year"].min())
        max_yr = int(clean_sharks["Year"].max())
        top_countries = clean_sharks["Country_clean"].value_counts().head(15).index.tolist()
        activities = sorted(clean_sharks["Activity_group"].dropna().unique().tolist())
    else:
        min_yr, max_yr = 1960, 2018
        top_countries = ["United States", "Australia", "South Africa"]
        activities = ["Surfing", "Swimming", "Diving/Snorkeling"]

    # Mandatory Header Card (Dataset names + all 4 team members)
    header = dbc.Row(
        dbc.Col(
            html.Div(
                [
                    html.H2(PROJECT_TITLE, className="text-dark fw-bold mb-2"),
                    html.P(DATASET_NAMES, className="text-muted mb-2"),
                    html.Div(
                        [
                            html.Span("Team Members: ", className="fw-bold text-secondary me-2"),
                            html.Span(" | ".join(TEAM_MEMBERS), className="badge bg-secondary fs-6 text-wrap"),
                        ]
                    ),
                ],
                className="p-4 my-3 bg-light border rounded shadow-sm",
            )
        )
    )

    # Dynamic KPI summary cards
    kpi_cards = dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Total Analyzed Incidents", className="text-muted"),
                            html.H3(kpis["total_incidents"], className="text-primary fw-bold"),
                            html.Small(kpis["year_window"], className="text-muted"),
                        ]
                    ),
                    className="shadow-sm mb-3",
                ),
                width=3,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Reports Recorded as Fatal", className="text-muted"),
                            html.H3(kpis["fatality_rate"], className="text-danger fw-bold"),
                            html.Small(kpis["fatal_subtitle"], className="text-muted"),
                        ]
                    ),
                    className="shadow-sm mb-3",
                ),
                width=3,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Top Incident Country", className="text-muted"),
                            html.H3(kpis["top_country"], className="text-success fw-bold"),
                            html.Small(kpis["top_country_subtitle"], className="text-muted"),
                        ]
                    ),
                    className="shadow-sm mb-3",
                ),
                width=3,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Highest Report Ratio Among Top 8", className="text-muted"),
                            html.H3(kpis["highest_risk_label"], className="text-warning fw-bold"),
                            html.Small(kpis["highest_risk_subtitle"], className="text-muted"),
                        ]
                    ),
                    className="shadow-sm mb-3",
                ),
                width=3,
            ),
        ],
        className="mb-2",
    )

    # Interactive Filter Bar (drives live callback on Tab 1 & Tab 4)
    filter_bar = dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Year Range Filter", className="fw-bold small text-secondary"),
                            dcc.RangeSlider(
                                id="year-range-slider",
                                min=min_yr,
                                max=max_yr,
                                step=1,
                                value=[min_yr, max_yr],
                                marks={y: str(y) for y in range(min_yr, max_yr + 1, 10)},
                                tooltip={"placement": "bottom", "always_visible": False},
                            ),
                        ],
                        width=5,
                    ),
                    dbc.Col(
                        [
                            html.Label("Filter by Country (Top 15)", className="fw-bold small text-secondary"),
                            dcc.Dropdown(
                                id="country-filter",
                                options=[{"label": c, "value": c} for c in top_countries],
                                multi=True,
                                placeholder="All countries",
                            ),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            html.Label("Filter by Activity", className="fw-bold small text-secondary"),
                            dcc.Dropdown(
                                id="activity-filter",
                                options=[{"label": a, "value": a} for a in activities],
                                multi=True,
                                placeholder="All activities",
                            ),
                        ],
                        width=3,
                    ),
                ]
            )
        ),
        className="mb-3 shadow-sm",
    )

    # 5 Organized Tabs matching Queries 1-4 + External Tourism Bonus
    tabs = dcc.Tabs(
        [
            dcc.Tab(
                label="1. Grouping & Fatality Rates",
                children=[
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Query 1: Incident Distribution & Fatality Rates", className="card-title"),
                                html.P(
                                    "Use the filters above to dynamically slice attacks by period, country, and activity group.",
                                    className="text-muted",
                                ),
                                dcc.Graph(id="live-countries-graph", figure=figures_dict.get("fig_countries", go.Figure())),
                                html.Hr(),
                                dcc.Graph(id="live-activities-graph", figure=figures_dict.get("fig_activities", go.Figure())),
                                html.Hr(),
                                dcc.Graph(figure=figures_dict.get("fig_species", go.Figure())),
                            ]
                        ),
                        className="mt-3 border-0 shadow-sm",
                    )
                ],
            ),
            dcc.Tab(
                label="2. Frequent Patterns (Apriori)",
                children=[
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Query 2: Association Rule Mining (Apriori)", className="card-title"),
                                html.P(
                                    "Discrete co-occurrences of Country, Activity, Type, Season, Time of Day, and Fatality (Lab 9 methodology).",
                                    className="text-muted",
                                ),
                                dcc.Graph(figure=figures_dict.get("fig_sensitivity", go.Figure())),
                                html.Hr(),
                                dcc.Graph(figure=figures_dict.get("fig_rules", go.Figure())),
                            ]
                        ),
                        className="mt-3 border-0 shadow-sm",
                    )
                ],
            ),
            dcc.Tab(
                label="3. Temporal & Prophet Forecast",
                children=[
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Query 3: Hemisphere Seasonality & Prophet Forecasting", className="card-title"),
                                html.P(
                                    "Inverted monthly summer peaks between Northern and Southern hemispheres, 5-year Prophet forecast (95% CI), and monthly decomposition.",
                                    className="text-muted",
                                ),
                                dcc.Graph(figure=figures_dict.get("fig_seasonality", go.Figure())),
                                html.Hr(),
                                dcc.Graph(figure=figures_dict.get("fig_forecast", go.Figure())),
                                html.Hr(),
                                dcc.Graph(figure=figures_dict.get("fig_components", go.Figure())),
                            ]
                        ),
                        className="mt-3 border-0 shadow-sm",
                    )
                ],
            ),
            dcc.Tab(
                label="4. Spatial Hotspots (GeoPandas + K-Means / OPTICS)",
                children=[
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Query 4: Coastal Spatial Hotspots", className="card-title"),
                                html.P(
                                    "GeoPandas spatial join with Natural Earth country polygons combined with K-Means basin partitioning and OPTICS density clustering (Lab 8).",
                                    className="text-muted",
                                ),
                                dcc.Graph(id="live-spatial-map", figure=figures_dict.get("fig_map", go.Figure())),
                                html.Hr(),
                                dcc.Graph(figure=figures_dict.get("fig_optics_map", go.Figure())),
                            ]
                        ),
                        className="mt-3 border-0 shadow-sm",
                    )
                ],
            ),
            dcc.Tab(
                label="5. Tourism Bonus (+1 Extra Point)",
                children=[
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("External Dataset Bonus: World Bank Tourism Correlation", className="card-title"),
                                html.P(
                                    f"Correlating annual attacks with inbound international tourists (Pearson r = {kpis['pearson_r']}) distinguishes raw exposure volume from relative coastal risk.",
                                    className="text-muted",
                                ),
                                dcc.Graph(figure=figures_dict.get("fig_comparison", go.Figure())),
                                html.Hr(),
                                dcc.Graph(figure=figures_dict.get("fig_dual_axis", go.Figure())),
                            ]
                        ),
                        className="mt-3 border-0 shadow-sm",
                    )
                ],
            ),
        ]
    )

    app.layout = dbc.Container([header, kpi_cards, filter_bar, tabs], fluid=True, className="pb-5")

    # Register live interactive callback when cleaned DataFrames are available
    if clean_sharks is not None:
        @app.callback(
            [
                Output("live-countries-graph", "figure"),
                Output("live-activities-graph", "figure"),
                Output("live-spatial-map", "figure"),
            ],
            [
                Input("year-range-slider", "value"),
                Input("country-filter", "value"),
                Input("activity-filter", "value"),
            ],
        )
        # Function for filtering dashboard charts interactively based on user controls
        # Input: year_range (list), selected_countries (list or None), selected_activities (list or None)
        # Output: tuple of 3 updated Plotly figures (countries, activities, spatial map)
        def update_filtered_charts(year_range, selected_countries, selected_activities):
            df_f = clean_sharks[
                (clean_sharks["Year"] >= year_range[0]) & (clean_sharks["Year"] <= year_range[1])
            ].copy()
            if selected_countries:
                df_f = df_f[df_f["Country_clean"].isin(selected_countries)]
            if selected_activities:
                df_f = df_f[df_f["Activity_group"].isin(selected_activities)]

            if len(df_f) == 0:
                empty = go.Figure().update_layout(title="No incidents match current filters", template="plotly_white")
                return empty, empty, empty

            # Updated Countries Bar
            c_stats = df_f.groupby("Country_clean").agg(
                Total_Attacks=("Case Number", "count"),
                Fatal_Attacks=("Fatal_clean", lambda s: (s == "Y").sum()),
            ).reset_index()
            c_stats["Fatality_Rate_Pct"] = ((c_stats["Fatal_Attacks"] / c_stats["Total_Attacks"]) * 100).round(2)
            c_stats = c_stats.sort_values("Total_Attacks", ascending=False).head(10)
            fig_c = px.bar(
                c_stats,
                x="Total_Attacks",
                y="Country_clean",
                orientation="h",
                color="Fatality_Rate_Pct",
                color_continuous_scale="Tealgrn",
                title=f"Top Countries ({year_range[0]}-{year_range[1]}) & Fatality Rate (%)",
            ).update_layout(yaxis={"autorange": "reversed"}, template="plotly_white")

            # Updated Activities Bar
            a_stats = df_f.groupby("Activity_group").agg(
                Total_Attacks=("Case Number", "count"),
                Fatal_Attacks=("Fatal_clean", lambda s: (s == "Y").sum()),
            ).reset_index()
            a_stats["Fatality_Rate_Pct"] = ((a_stats["Fatal_Attacks"] / a_stats["Total_Attacks"]) * 100).round(2)
            a_stats = a_stats.sort_values("Total_Attacks", ascending=False)
            fig_a = px.bar(
                a_stats,
                x="Activity_group",
                y="Total_Attacks",
                color="Fatality_Rate_Pct",
                color_continuous_scale="Reds",
                title=f"Activity Distribution ({year_range[0]}-{year_range[1]}) & Fatality Rate (%)",
            ).update_layout(template="plotly_white")

            # Updated Spatial Map
            if geo_df is not None:
                gdf_f = geo_df[
                    (geo_df["Year"] >= year_range[0]) & (geo_df["Year"] <= year_range[1])
                ].copy()
                if selected_countries:
                    gdf_f = gdf_f[gdf_f["Country_clean"].isin(selected_countries)]
                if selected_activities:
                    gdf_f = gdf_f[gdf_f["Activity_group"].isin(selected_activities)]
                if len(gdf_f) > 0:
                    pts = gdf_f.groupby(["Country_clean", "Area_clean", "latitude", "longitude", "Cluster_Name"]).agg(
                        Incidents=("Case Number", "count")
                    ).reset_index()
                    fig_m = px.scatter_geo(
                        pts,
                        lat="latitude",
                        lon="longitude",
                        size="Incidents",
                        size_max=30,
                        color="Cluster_Name",
                        hover_name="Area_clean",
                        title=f"Filtered Coastal Hotspots ({year_range[0]}-{year_range[1]})",
                        projection="natural earth",
                    )
                    fig_m.update_geos(showcoastlines=True, coastlinecolor="#94A3B8", showland=True, landcolor="#F1F5F9")
                    fig_m.update_layout(template="plotly_white", legend=dict(orientation="h", yanchor="bottom", y=-0.25))
                else:
                    fig_m = go.Figure().update_layout(title="No geocoded incidents match filters", template="plotly_white")
            else:
                fig_m = figures_dict.get("fig_map", go.Figure())

            return fig_c, fig_a, fig_m

    return app


# Function for embedding the world basemap used by the exported geographic figures
# Input: local project assets or the Plotly world 110m basemap URL
# Output: a data URL containing the TopoJSON without a runtime network dependency
def offline_world_basemap_url():
    relative_asset = Path("projet/src/assets/world_110m.json")
    candidates = [relative_asset, Path("..") / relative_asset, Path("data/world_110m.json")]
    if "__file__" in globals():
        candidates.insert(0, Path(__file__).resolve().parent / "assets/world_110m.json")
    for candidate in candidates:
        if candidate.is_file():
            topojson = candidate.read_bytes()
            break
    else:
        response = requests.get("https://cdn.plot.ly/un/world_110m.json", timeout=30)
        response.raise_for_status()
        topojson = response.content
    encoded = base64.b64encode(topojson).decode("ascii")
    # Plotly appends a filename to the base URL. Keep it in the ignored fragment.
    return f"data:application/json;base64,{encoded}#"


# Function for exporting all dashboard figures and dynamic KPIs to a standalone offline HTML proof file
# Input: figures_dict (dict), kpis (dict), output_path (str)
# Output: output_path (str) of the written HTML file
def export_dashboard_html(figures_dict, kpis, output_path):
    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    titles = [
        ("Query 1: Top 10 Countries & Fatality Rate", "fig_countries"),
        ("Query 1: Activity Group Distribution & Fatality Rate", "fig_activities"),
        ("Query 1: Identified Shark Species & Fatality Rate", "fig_species"),
        ("Query 2: Apriori Support Sensitivity Curve", "fig_sensitivity"),
        ("Query 2: Association Rules (Support vs. Confidence, Lift)", "fig_rules"),
        ("Query 3: Northern vs. Southern Hemisphere Seasonality", "fig_seasonality"),
        ("Query 3: Annual Prophet 5-Year Forecast (95% CI)", "fig_forecast"),
        ("Query 3: Prophet Monthly Decomposition (Trend & Seasonality)", "fig_components"),
        ("Query 4: Global Coastal Hotspots (K-Means + GeoPandas)", "fig_map"),
        ("Query 4: Density-Based Hotspots (OPTICS Comparison)", "fig_optics_map"),
        ("Bonus (+1 pt): Reported Incidents per Million Arrivals", "fig_comparison"),
        ("Bonus (+1 pt): US Dual-Axis Attacks vs. Tourism Arrivals", "fig_dual_axis"),
    ]

    figs_html = []
    basemap_url = None
    for title, key in titles:
        fig = figures_dict.get(key)
        if fig is not None:
            config = {}
            if any(trace.type == "scattergeo" for trace in fig.data):
                if basemap_url is None:
                    basemap_url = offline_world_basemap_url()
                fig = go.Figure(fig)
                fig.update_geos(scope="world", resolution=110)
                config["topojsonURL"] = basemap_url
            figure_html = fig.to_html(
                full_html=False, include_plotlyjs=not figs_html, config=config
            )
            figs_html.append(
                f"""
            <div style="background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <h3 style="margin-top:0; color:#0F172A; font-size:18px;">{title}</h3>
                {figure_html}
            </div>
            """
            )

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{PROJECT_TITLE} - Dashboard Evidence</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #F8FAFC; margin: 0; padding: 24px; color: #0F172A; }}
        header {{ background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .badge {{ background: #334155; color: white; padding: 6px 12px; border-radius: 4px; font-size: 13px; font-weight: 600; display: inline-block; margin-top: 8px; }}
        .kpi-container {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
        .kpi-card {{ flex: 1; min-width: 200px; background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .kpi-title {{ font-size: 12px; color: #64748B; margin: 0 0 6px 0; text-transform: uppercase; font-weight: 600; }}
        .kpi-val {{ font-size: 26px; font-weight: 700; color: #0F766E; margin: 0 0 4px 0; }}
    </style>
</head>
<body>
    <header>
        <h1 style="margin:0 0 8px 0; font-size:24px;">{PROJECT_TITLE}</h1>
        <p style="margin:0 0 8px 0; color:#64748B;">{DATASET_NAMES}</p>
        <div class="badge">Team Members: {" | ".join(TEAM_MEMBERS)}</div>
    </header>

    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-title">Total Analyzed Incidents</div>
            <div class="kpi-val">{kpis['total_incidents']}</div>
            <small style="color:#64748B;">{kpis['year_window']}</small>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Reports Recorded as Fatal</div>
            <div class="kpi-val" style="color:#DC2626;">{kpis['fatality_rate']}</div>
            <small style="color:#64748B;">{kpis['fatal_subtitle']}</small>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Top Incident Country</div>
            <div class="kpi-val" style="color:#0284C7;">{kpis['top_country']}</div>
            <small style="color:#64748B;">{kpis['top_country_subtitle']}</small>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Highest Report Ratio Among Top 8</div>
            <div class="kpi-val" style="color:#D97706;">{kpis['highest_risk_label']}</div>
            <small style="color:#64748B;">{kpis['highest_risk_subtitle']}</small>
        </div>
    </div>

    {''.join(figs_html)}
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
    return output_path


if __name__ == "__main__":
    # Standalone launch helper: load local datasets, compute all indicators, and start Dash
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.data_loader import load_shark_data, load_tourism_data, clean_shark_data, clean_and_merge_tourism
    from src.indicators import (
        query_grouping_analysis,
        query_frequent_patterns,
        query_temporal_forecast,
        geocode_coastal_areas,
        query_spatial_clustering,
        query_tourism_enrichment,
    )

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    raw_sharks = load_shark_data(os.path.join(base_dir, "data", "attacks.csv"))
    raw_tourism = load_tourism_data(os.path.join(base_dir, "data", "tourism_arrivals.csv"))
    sharks = clean_shark_data(raw_sharks)
    merged = clean_and_merge_tourism(sharks, raw_tourism)

    q1 = query_grouping_analysis(sharks)
    q2 = query_frequent_patterns(sharks)
    q3 = query_temporal_forecast(sharks)
    geo = geocode_coastal_areas(sharks, cache_path=os.path.join(base_dir, "data", "locations_geocoded.csv"))
    q4 = query_spatial_clustering(sharks, geo, shp_path=os.path.join(base_dir, "data", "countries_shp", "ne_110m_admin_0_countries.shp"))
    bonus = query_tourism_enrichment(merged)

    figs = {
        "fig_countries": q1["fig_countries"],
        "fig_activities": q1["fig_activities"],
        "fig_species": q1["fig_species"],
        "fig_sensitivity": q2["fig_sensitivity"],
        "fig_rules": q2["fig_rules"],
        "fig_seasonality": q3["fig_seasonality"],
        "fig_forecast": q3["fig_forecast"],
        "fig_components": q3["fig_components"],
        "fig_map": q4["fig_map"],
        "fig_optics_map": q4["fig_optics_map"],
        "fig_comparison": bonus["fig_comparison"],
        "fig_dual_axis": bonus["fig_dual_axis"],
    }
    kpis_live = compute_dashboard_kpis(sharks, bonus)
    dash_app = create_dash_app(figs, kpis_live, clean_sharks=sharks, geo_df=q4["geo_df"])
    dash_app.run(debug=False, port=8050)

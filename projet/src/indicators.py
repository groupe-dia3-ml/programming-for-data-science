# Module containing the 4 analytical queries and the external tourism bonus analysis
# Aligned with Final_project.pdf and ESILV Labs 7, 8, and 9

import os
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from mlxtend.frequent_patterns import apriori, association_rules
from prophet import Prophet
from sklearn.cluster import OPTICS, KMeans
from scipy.stats import pearsonr, spearmanr


# ==============================================================================
# Query 1: Grouping & Aggregation [1 point] — Owner: Baptiste Noailhac
# ==============================================================================

# Function for computing grouping indicators (top countries, activities, species, fatality rates)
# Input: shark_df (pd.DataFrame) cleaned shark data, top_n (int) number of top countries
# Output: dictionary with summary DataFrames and interactive Plotly bar charts
def query_grouping_analysis(shark_df, top_n=10):
    # 1. Country-level aggregation
    country_stats = shark_df.groupby("Country_clean").agg(
        Total_Attacks=("Case Number", "count"),
        Fatal_Attacks=("Fatal_clean", lambda s: (s == "Y").sum()),
        Non_Fatal_Attacks=("Fatal_clean", lambda s: (s == "N").sum()),
    ).reset_index()
    country_stats["Fatality_Rate_Pct"] = (
        (country_stats["Fatal_Attacks"] / country_stats["Total_Attacks"]) * 100
    ).round(2)
    top_countries = country_stats.sort_values(by="Total_Attacks", ascending=False).head(top_n).reset_index(drop=True)

    # 2. Activity-level aggregation
    activity_stats = shark_df.groupby("Activity_group").agg(
        Total_Attacks=("Case Number", "count"),
        Fatal_Attacks=("Fatal_clean", lambda s: (s == "Y").sum()),
    ).reset_index()
    activity_stats["Fatality_Rate_Pct"] = (
        (activity_stats["Fatal_Attacks"] / activity_stats["Total_Attacks"]) * 100
    ).round(2)
    activity_stats = activity_stats.sort_values(by="Total_Attacks", ascending=False).reset_index(drop=True)

    # 3. Species-level aggregation (focusing on identified species for fatality comparison)
    species_stats = shark_df.groupby("Species_group").agg(
        Total_Attacks=("Case Number", "count"),
        Fatal_Attacks=("Fatal_clean", lambda s: (s == "Y").sum()),
    ).reset_index()
    species_stats["Fatality_Rate_Pct"] = (
        (species_stats["Fatal_Attacks"] / species_stats["Total_Attacks"]) * 100
    ).round(2)
    species_stats = species_stats.sort_values(by="Total_Attacks", ascending=False).reset_index(drop=True)
    species_identified = species_stats[species_stats["Species_group"] != "Unidentified"].copy()

    # 4. Interactive Plotly Charts
    fig_countries = px.bar(
        top_countries,
        x="Total_Attacks",
        y="Country_clean",
        orientation="h",
        color="Fatality_Rate_Pct",
        color_continuous_scale="Tealgrn",
        labels={
            "Total_Attacks": "Number of Recorded Attacks",
            "Country_clean": "Country",
            "Fatality_Rate_Pct": "Fatality Rate (%)",
        },
        title=f"Top {top_n} Countries by Shark Attacks (1960-2018) & Fatality Rate",
    )
    fig_countries.update_layout(yaxis={"autorange": "reversed"}, template="plotly_white")

    fig_activities = px.bar(
        activity_stats,
        x="Activity_group",
        y="Total_Attacks",
        color="Fatality_Rate_Pct",
        color_continuous_scale="Reds",
        labels={
            "Total_Attacks": "Number of Attacks",
            "Activity_group": "Activity Category",
            "Fatality_Rate_Pct": "Fatality Rate (%)",
        },
        title="Shark Attacks by Activity Group & Associated Fatality Rate (%)",
    )
    fig_activities.update_layout(template="plotly_white")

    fig_species = px.bar(
        species_identified,
        x="Species_group",
        y="Total_Attacks",
        color="Fatality_Rate_Pct",
        color_continuous_scale="OrRd",
        labels={
            "Total_Attacks": "Identified Incidents",
            "Species_group": "Shark Species Group",
            "Fatality_Rate_Pct": "Fatality Rate (%)",
        },
        title="Identified Shark Species Groups: Incident Count & Fatality Rate (%)",
    )
    fig_species.update_layout(template="plotly_white")

    return {
        "top_countries": top_countries,
        "activity_stats": activity_stats,
        "species_stats": species_stats,
        "fig_countries": fig_countries,
        "fig_activities": fig_activities,
        "fig_species": fig_species,
    }


# ==============================================================================
# Query 2: Frequent Pattern Mining (Apriori) [2 points] — Owner: Baptiste Noailhac
# ==============================================================================

# Function for extracting frequent itemsets and association rules using mlxtend Apriori
# Input: shark_df (pd.DataFrame), min_support (float), min_lift (float)
# Output: dictionary with support sensitivity, frequent itemsets, association rules, and Plotly figures
def query_frequent_patterns(shark_df, min_support=0.03, min_lift=1.05):
    cols = ["Country_clean", "Activity_group", "Type", "Season", "Time_of_day", "Fatal_clean"]
    df_cat = shark_df[cols].copy()

    # Exclude Unknown values so association rules reflect real observations
    for col in cols:
        df_cat[col] = df_cat[col].replace({"Unknown": np.nan})
    df_cat = df_cat.dropna()

    # Group minor countries into Other_Country to keep transaction space compact
    top_5_countries = shark_df["Country_clean"].value_counts().head(5).index.tolist()
    df_cat["Country_clean"] = df_cat["Country_clean"].apply(
        lambda c: c if c in top_5_countries else "Other_Country"
    )

    # Boolean one-hot transaction matrix (Lab 9 methodology)
    df_bool = pd.get_dummies(df_cat, dtype=bool)

    # 1. Support sensitivity sweep across thresholds
    support_thresholds = [0.15, 0.10, 0.08, 0.05, 0.04, 0.03, 0.02]
    sensitivity_counts = []
    for s in support_thresholds:
        itemsets_s = apriori(df_bool, min_support=s, use_colnames=True)
        sensitivity_counts.append(len(itemsets_s))
    sensitivity_df = pd.DataFrame({
        "min_support": support_thresholds,
        "pattern_count": sensitivity_counts,
    })

    fig_sensitivity = px.line(
        sensitivity_df,
        x="min_support",
        y="pattern_count",
        markers=True,
        labels={
            "min_support": "Minimal Support Threshold (min_support)",
            "pattern_count": "Number of Frequent Itemsets",
        },
        title="Apriori Support Sensitivity Curve (Lab 9 Pattern)",
    )
    fig_sensitivity.update_layout(template="plotly_white")

    # 2. Extract frequent itemsets and association rules
    frequent_itemsets = apriori(df_bool, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)
    rules["antecedents_str"] = rules["antecedents"].apply(lambda s: ", ".join(sorted(list(s))))
    rules["consequents_str"] = rules["consequents"].apply(lambda s: ", ".join(sorted(list(s))))
    rules_sorted = rules.sort_values(by=["lift", "confidence"], ascending=[False, False]).reset_index(drop=True)

    # 3. Interactive scatter plot of support vs. confidence colored by lift
    fig_rules = px.scatter(
        rules_sorted,
        x="support",
        y="confidence",
        color="lift",
        color_continuous_scale="Viridis",
        hover_data=["antecedents_str", "consequents_str"],
        labels={"support": "Support", "confidence": "Confidence", "lift": "Lift"},
        title="Association Rules: Support vs. Confidence (colored by Lift)",
    )
    fig_rules.update_layout(template="plotly_white")

    return {
        "n_transactions": int(len(df_bool)),
        "frequent_itemsets": frequent_itemsets,
        "rules": rules_sorted,
        "sensitivity_df": sensitivity_df,
        "fig_sensitivity": fig_sensitivity,
        "fig_rules": fig_rules,
    }


# ==============================================================================
# Query 3: Temporal Analysis & Forecasting (Prophet) [2 points] — Owner: Romain Thepaut
# ==============================================================================

# Function for analyzing hemisphere seasonality and forecasting shark attacks with Prophet
# Input: shark_df (pd.DataFrame), forecast_years (int)
# Output: dictionary with seasonality table, Prophet forecasts, components, and Plotly figures
def query_temporal_forecast(shark_df, forecast_years=5):
    # 1. Northern vs. Southern Hemisphere monthly seasonality
    df_valid_months = shark_df[shark_df["Month"].notna() & shark_df["Month"].isin(range(1, 13))].copy()
    df_valid_months["Month"] = df_valid_months["Month"].astype(int)

    us_months = (
        df_valid_months[df_valid_months["Country_clean"] == "United States"]["Month"]
        .value_counts(normalize=True)
        .sort_index() * 100
    )
    south_months = (
        df_valid_months[df_valid_months["Country_clean"].isin(["Australia", "South Africa"])]["Month"]
        .value_counts(normalize=True)
        .sort_index() * 100
    )

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    season_df = pd.DataFrame({
        "Month": month_names,
        "Northern_Hemisphere_US": [round(float(us_months.get(m, 0.0)), 2) for m in range(1, 13)],
        "Southern_Hemisphere_Aus_SA": [round(float(south_months.get(m, 0.0)), 2) for m in range(1, 13)],
    })

    fig_seasonality = go.Figure()
    fig_seasonality.add_trace(go.Scatter(
        x=season_df["Month"],
        y=season_df["Northern_Hemisphere_US"],
        mode="lines+markers",
        name="United States (Northern Hemisphere)",
        line=dict(color="#0284C7", width=3),
    ))
    fig_seasonality.add_trace(go.Scatter(
        x=season_df["Month"],
        y=season_df["Southern_Hemisphere_Aus_SA"],
        mode="lines+markers",
        name="Australia & South Africa (Southern Hemisphere)",
        line=dict(color="#DC2626", width=3),
    ))
    fig_seasonality.update_layout(
        title="Monthly Seasonality Comparison: Northern vs. Southern Hemisphere (% of Incidents)",
        xaxis_title="Month",
        yaxis_title="Share of Incidents (%)",
        template="plotly_white",
    )

    # 2. Annual Prophet 5-Year Forecast (excluding incomplete final partial year if < 60% of prior mean)
    annual_counts = shark_df.groupby("Year").size().reset_index(name="y").sort_values("Year")
    recent_avg = annual_counts["y"].iloc[-6:-1].mean()
    if len(annual_counts) > 5 and annual_counts["y"].iloc[-1] < 0.6 * recent_avg:
        annual_counts = annual_counts.iloc[:-1].copy()

    annual_counts["ds"] = pd.to_datetime(annual_counts["Year"].astype(str) + "-01-01")
    df_prophet_annual = annual_counts[["ds", "y"]].reset_index(drop=True)

    model_annual = Prophet(
        interval_width=0.95,
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False,
    )
    model_annual.fit(df_prophet_annual)
    future_annual = model_annual.make_future_dataframe(periods=forecast_years, freq="YS")
    forecast_annual = model_annual.predict(future_annual)

    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(
        x=df_prophet_annual["ds"],
        y=df_prophet_annual["y"],
        mode="markers",
        name="Observed Annual Incidents",
        marker=dict(color="#0F172A", size=6),
    ))
    fig_forecast.add_trace(go.Scatter(
        x=forecast_annual["ds"],
        y=forecast_annual["yhat"],
        mode="lines",
        name="Prophet Forecast (yhat)",
        line=dict(color="#0F766E", width=3),
    ))
    fig_forecast.add_trace(go.Scatter(
        x=forecast_annual["ds"],
        y=forecast_annual["yhat_upper"],
        mode="lines",
        name="95% Upper Bound",
        line=dict(color="#94A3B8", width=1, dash="dash"),
    ))
    fig_forecast.add_trace(go.Scatter(
        x=forecast_annual["ds"],
        y=forecast_annual["yhat_lower"],
        mode="lines",
        name="95% Lower Bound",
        line=dict(color="#94A3B8", width=1, dash="dash"),
        fill="tonexty",
        fillcolor="rgba(148, 163, 184, 0.2)",
    ))
    fig_forecast.update_layout(
        title=f"Global Shark Attacks Annual Trend & {forecast_years}-Year Prophet Forecast (95% CI)",
        xaxis_title="Year",
        yaxis_title="Annual Incident Count",
        template="plotly_white",
    )

    # 3. Monthly Prophet Decomposition (Trend + Yearly Seasonality Component, Lab 7 style)
    max_complete_year = int(annual_counts["Year"].max())
    monthly_df = df_valid_months[df_valid_months["Year"] <= max_complete_year].copy()
    monthly_df["ds"] = pd.to_datetime(
        monthly_df["Year"].astype(str) + "-" + monthly_df["Month"].astype(str).str.zfill(2) + "-01"
    )
    monthly_counts = monthly_df.groupby("ds").size().reset_index(name="y").sort_values("ds")

    model_monthly = Prophet(
        interval_width=0.95,
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
    )
    model_monthly.fit(monthly_counts)
    future_monthly = model_monthly.make_future_dataframe(periods=forecast_years * 12, freq="MS")
    forecast_monthly = model_monthly.predict(future_monthly)

    # Extract clean trend & yearly seasonality subplot
    one_year = forecast_monthly.tail(12).copy()
    one_year["Month_Num"] = one_year["ds"].dt.month
    one_year = one_year.sort_values("Month_Num")
    one_year["Month_Name"] = [month_names[m - 1] for m in one_year["Month_Num"]]

    fig_components = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Long-Term Monthly Trend Component", "Yearly Seasonal Effect (Monthly)"),
    )
    fig_components.add_trace(
        go.Scatter(x=forecast_monthly["ds"], y=forecast_monthly["trend"], mode="lines", name="Trend", line=dict(color="#0F766E", width=2.5)),
        row=1, col=1,
    )
    fig_components.add_trace(
        go.Bar(x=one_year["Month_Name"], y=one_year["yearly"], name="Yearly Seasonality", marker_color="#0284C7"),
        row=1, col=2,
    )
    fig_components.update_layout(
        title="Prophet Monthly Time-Series Decomposition (Trend & Seasonality Components)",
        template="plotly_white",
        showlegend=False,
    )

    return {
        "season_df": season_df,
        "fig_seasonality": fig_seasonality,
        "forecast_df": forecast_annual[["ds", "yhat", "yhat_lower", "yhat_upper"]],
        "monthly_forecast_df": forecast_monthly[["ds", "yhat", "trend", "yearly"]],
        "fig_forecast": fig_forecast,
        "fig_components": fig_components,
        "prophet_model": model_annual,
    }


# ==============================================================================
# Query 4: Spatial Analysis & Clustering (GeoPandas + OPTICS/KMeans) [2 points] — Owner: Louis Le Forestier
# ==============================================================================

# Accurate coastal area coordinates for major GSAF administrative zones
COASTAL_AREA_COORDINATES = {
    ("United States", "Florida"): (28.0836, -80.6081),
    ("United States", "Hawaii"): (20.7984, -156.3319),
    ("United States", "California"): (34.4208, -119.6982),
    ("United States", "South Carolina"): (32.7765, -79.9311),
    ("United States", "North Carolina"): (34.2257, -77.9447),
    ("United States", "Texas"): (27.8006, -97.3964),
    ("United States", "New Jersey"): (39.3643, -74.4229),
    ("United States", "Oregon"): (44.6368, -124.0535),
    ("United States", "New York"): (40.5884, -73.6579),
    ("United States", "Virginia"): (36.8529, -75.9780),
    ("United States", "Georgia"): (31.1499, -81.4915),
    ("United States", "Alabama"): (30.2460, -87.7008),
    ("United States", "Massachusetts"): (41.6688, -70.2962),
    ("United States", "Louisiana"): (29.2500, -90.0000),
    ("United States", "Puerto Rico"): (18.4655, -66.1057),
    ("Australia", "New South Wales"): (-33.8688, 151.2093),
    ("Australia", "Queensland"): (-27.4698, 153.0251),
    ("Australia", "Western Australia"): (-31.9505, 115.8605),
    ("Australia", "South Australia"): (-34.9285, 138.6007),
    ("Australia", "Victoria"): (-38.3300, 144.3200),
    ("Australia", "Tasmania"): (-42.8821, 147.3272),
    ("Australia", "Northern Territory"): (-12.4634, 130.8456),
    ("Australia", "Torres Strait"): (-10.5833, 142.2167),
    ("South Africa", "Kwazulu-Natal"): (-29.8587, 31.0218),
    ("South Africa", "Eastern Cape Province"): (-33.9608, 25.6022),
    ("South Africa", "Western Cape Province"): (-34.1167, 18.4667),
    ("Brazil", "Pernambuco"): (-8.0578, -34.8829),
    ("Brazil", "Rio De Janeiro"): (-22.9068, -43.1729),
    ("Brazil", "Bahia"): (-12.9714, -38.5014),
    ("Brazil", "Maranhao"): (-2.5307, -44.3068),
    ("Brazil", "Santa Catarina"): (-27.5954, -48.5480),
    ("Bahamas, The", "Abaco Islands"): (26.5412, -77.0636),
    ("Bahamas, The", "Grand Bahama"): (26.6594, -78.4975),
    ("Bahamas, The", "New Providence"): (25.0443, -77.3504),
    ("New Zealand", "North Island"): (-36.8485, 174.7633),
    ("New Zealand", "South Island"): (-43.5321, 172.6362),
    ("Mexico", "Quintana Roo"): (20.6296, -87.0739),
    ("Mexico", "Guerrero"): (16.8531, -99.8237),
    ("Mexico", "Baja California"): (24.1426, -110.3128),
    ("Mexico", "Veracruz"): (19.1738, -96.1342),
    ("Reunion", "Saint-Paul"): (-21.0097, 55.2707),
    ("Reunion", "Saint-Gilles"): (-21.0543, 55.2255),
    ("Reunion", "Saint-Leu"): (-21.1706, 55.2882),
}

# Country-level coastal fallback centroids to ensure >90% global geocoding coverage
COUNTRY_COASTAL_CENTROIDS = {
    "United States": (28.50, -81.00),
    "Australia": (-28.00, 152.50),
    "South Africa": (-32.50, 28.00),
    "Brazil": (-10.00, -35.50),
    "Bahamas, The": (25.03, -77.40),
    "New Zealand": (-37.78, 175.28),
    "Mexico": (20.50, -96.50),
    "Reunion": (-21.11, 55.53),
    "Papua New Guinea": (-6.31, 147.00),
    "Fiji": (-17.71, 178.07),
    "New Caledonia": (-21.25, 165.30),
    "French Polynesia": (-17.65, -149.43),
    "Egypt, Arab Rep.": (27.26, 33.81),
    "Italy": (40.85, 14.27),
    "Spain": (39.47, -0.38),
    "France": (43.30, 5.37),
    "Japan": (33.59, 130.40),
    "Philippines": (12.88, 121.77),
    "Indonesia": (-8.41, 115.19),
    "Mozambique": (-23.86, 35.38),
    "Cuba": (23.11, -82.37),
    "Costa Rica": (9.75, -84.62),
    "Ecuador": (-1.83, -80.75),
    "Chile": (-33.05, -71.62),
    "United Kingdom": (50.37, -4.14),
    "Hong Kong SAR, China": (22.32, 114.17),
    "Venezuela, RB": (10.60, -66.93),
    "Colombia": (10.39, -75.48),
    "Jamaica": (18.11, -77.30),
    "Bermuda": (32.31, -64.75),
    "Taiwan": (23.70, 121.50),
    "India": (15.30, 73.92),
    "Thailand": (7.88, 98.39),
    "Vietnam": (12.24, 109.19),
    "Viet Nam": (12.24, 109.19),
    "Turkiye": (36.88, 30.70),
    "Greece": (37.98, 23.73),
    "Croatia": (43.51, 16.44),
    "Canada": (44.65, -63.57),
    "Solomon Islands": (-9.43, 159.96),
    "Tonga": (-21.18, -175.20),
    "Samoa": (-13.83, -171.76),
    "Vanuatu": (-17.73, 168.32),
    "Seychelles": (-4.68, 55.49),
    "Mauritius": (-20.35, 57.55),
    "Kenya": (-4.04, 39.67),
    "Madagascar": (-18.77, 49.40),
    "Panama": (8.98, -79.52),
    "Dominican Republic": (18.49, -69.93),
    "Belize": (17.50, -88.20),
    "Honduras": (16.33, -86.53),
    "Nicaragua": (12.11, -86.24),
    "Israel": (32.09, 34.78),
    "Iran, Islamic Rep.": (27.18, 56.28),
    "Korea, Rep.": (35.18, 129.08),
    "Russian Federation": (43.12, 131.89),
    "China": (22.54, 114.06),
}


# Function for geocoding unique coastal (Country_clean, Area_clean) pairs and saving local cache
# Input: shark_df (pd.DataFrame), cache_path (str or None), force_refresh (bool)
# Output: DataFrame with columns ['Country_clean', 'Area_clean', 'latitude', 'longitude', 'geo_precision']
def geocode_coastal_areas(shark_df, cache_path=None, force_refresh=False):
    keys = ["Country_clean", "Area_clean"]
    columns = keys + ["latitude", "longitude", "geo_precision"]
    unique_pairs = shark_df[keys].drop_duplicates()
    geo_rows = []
    if cache_path and os.path.exists(cache_path) and not force_refresh:
        cached = pd.read_csv(cache_path, dtype={key: str for key in keys})
        if set(columns).issubset(cached.columns):
            matching = unique_pairs.merge(cached[columns].drop_duplicates(keys), on=keys)
            geo_rows = matching.to_dict("records")
            found = set(matching[keys].itertuples(index=False, name=None))
            unique_pairs = unique_pairs.loc[
                [pair not in found for pair in unique_pairs.itertuples(index=False, name=None)]
            ]

    for country, area in unique_pairs.itertuples(index=False, name=None):
        if (country, area) in COASTAL_AREA_COORDINATES:
            lat, lon = COASTAL_AREA_COORDINATES[(country, area)]
            geo_rows.append({
                "Country_clean": country,
                "Area_clean": area,
                "latitude": lat,
                "longitude": lon,
                "geo_precision": "area",
            })
        elif country in COUNTRY_COASTAL_CENTROIDS:
            lat, lon = COUNTRY_COASTAL_CENTROIDS[country]
            geo_rows.append({
                "Country_clean": country,
                "Area_clean": area,
                "latitude": lat,
                "longitude": lon,
                "geo_precision": "country_centroid",
            })

    geo_df = pd.DataFrame(geo_rows, columns=columns)
    if cache_path:
        dir_name = os.path.dirname(cache_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        geo_df.to_csv(cache_path, index=False)

    return geo_df


# Function for dynamically naming a spatial cluster based on its actual geographic centroid and top countries
# Input: cluster_subset (pd.DataFrame) subset of incidents belonging to one cluster
# Output: human-readable geographic basin name (str)
def label_spatial_cluster(cluster_subset):
    mean_lat = float(cluster_subset["latitude"].mean())
    mean_lon = float(cluster_subset["longitude"].mean())
    top_countries = cluster_subset["Country_clean"].value_counts().head(2).index.tolist()
    top_str = " / ".join(top_countries)

    # Geographic basin heuristics derived strictly from actual centroid coordinates
    if mean_lon < -110:
        return f"Pacific & US West Coast / Hawaii ({top_str})"
    if -110 <= mean_lon <= -30:
        if mean_lat >= 20:
            return f"US Atlantic, Florida & Caribbean ({top_str})"
        return f"South America & Tropical Americas ({top_str})"
    if -30 < mean_lon <= 65:
        if mean_lat < 0:
            return f"Southern Africa & Indian Ocean ({top_str})"
        return f"Europe, Mediterranean & Red Sea ({top_str})"
    return f"Australia & South-West Pacific ({top_str})"


# Function for running GeoPandas spatial join and K-Means / OPTICS spatial clustering (Lab 8 pattern)
# Input: shark_df (pd.DataFrame), geo_df (pd.DataFrame), shp_path (str or None), n_clusters (int)
# Output: dictionary with clustered GeoDataFrame, K-Means & OPTICS summaries, and Plotly world maps
def query_spatial_clustering(shark_df, geo_df, shp_path=None, n_clusters=6):
    keys = ["Country_clean", "Area_clean"]
    merged_geo = shark_df.merge(geo_df, on=keys, how="inner", validate="many_to_one")
    country_centroid_count = int(merged_geo["geo_precision"].eq("country_centroid").sum())
    merged_geo = merged_geo.loc[merged_geo["geo_precision"].eq("area")].copy()
    area_count = len(merged_geo)
    coverage_pct = round(100 * area_count / len(shark_df), 2) if len(shark_df) else 0.0
    if area_count < 2:
        raise ValueError("Spatial clustering requires at least two area-level incident locations.")

    # 1. Build GeoDataFrame (Lab 8 pattern)
    geometry = [Point(lon, lat) for lon, lat in zip(merged_geo["longitude"], merged_geo["latitude"])]
    gdf = gpd.GeoDataFrame(merged_geo, geometry=geometry, crs="EPSG:4326")

    # 2. Spatial join with Natural Earth countries shapefile when available
    sjoin_matched = 0
    if shp_path and os.path.exists(shp_path):
        world_raw = gpd.read_file(shp_path).to_crs("EPSG:4326")
        admin_col = "admin" if "admin" in world_raw.columns else ("ADMIN" if "ADMIN" in world_raw.columns else None)
        cont_col = "continent" if "continent" in world_raw.columns else ("CONTINENT" if "CONTINENT" in world_raw.columns else None)
        keep_cols = [c for c in [admin_col, cont_col, "geometry"] if c is not None]
        world = world_raw[keep_cols].copy()
        if admin_col:
            world = world.rename(columns={admin_col: "shp_admin"})
        if cont_col:
            world = world.rename(columns={cont_col: "shp_continent"})
        gdf = gpd.sjoin(gdf, world, how="left", predicate="intersects")
        gdf = gdf.loc[~gdf.index.duplicated()].drop(columns=["index_right"], errors="ignore")
        if "shp_admin" in gdf.columns:
            sjoin_matched = int(gdf["shp_admin"].notna().sum())

    coords = gdf[["latitude", "longitude"]].values

    # 3. K-Means spatial clustering with dynamic centroid-based cluster labeling
    cluster_count = min(n_clusters, len(np.unique(coords, axis=0)))
    kmeans = KMeans(n_clusters=cluster_count, random_state=42, n_init=10)
    gdf["kmeans_cluster"] = kmeans.fit_predict(coords)

    dynamic_labels = {}
    for cid in sorted(gdf["kmeans_cluster"].unique()):
        subset = gdf[gdf["kmeans_cluster"] == cid]
        dynamic_labels[cid] = label_spatial_cluster(subset)
    gdf["Cluster_Name"] = gdf["kmeans_cluster"].map(dynamic_labels)

    # 4. OPTICS density-based spatial clustering (Lab 8 comparison)
    optics = OPTICS(min_samples=min(25, area_count), xi=0.05, min_cluster_size=0.04)
    gdf["optics_cluster"] = optics.fit_predict(coords)
    gdf["OPTICS_Label"] = gdf["optics_cluster"].apply(
        lambda c: "Noise / Isolated Coast (-1)" if c == -1 else f"Dense Hotspot #{c}"
    )

    # 5. Summarize K-Means clusters
    cluster_summary = gdf.groupby("Cluster_Name").agg(
        Total_Incidents=("Case Number", "count"),
        Fatal_Count=("Fatal_clean", lambda s: (s == "Y").sum()),
        Mean_Lat=("latitude", "mean"),
        Mean_Lon=("longitude", "mean"),
        Dominant_Activity=("Activity_group", lambda s: s.mode().iloc[0] if len(s.mode()) > 0 else "Unknown"),
    ).reset_index()
    cluster_summary["Fatality_Rate_Pct"] = (
        (cluster_summary["Fatal_Count"] / cluster_summary["Total_Incidents"]) * 100
    ).round(2)
    cluster_summary["Mean_Lat"] = cluster_summary["Mean_Lat"].round(2)
    cluster_summary["Mean_Lon"] = cluster_summary["Mean_Lon"].round(2)
    cluster_summary = cluster_summary.sort_values(by="Total_Incidents", ascending=False).reset_index(drop=True)

    # Summarize OPTICS clusters
    optics_summary = gdf.groupby("OPTICS_Label").agg(
        Total_Incidents=("Case Number", "count"),
        Top_Country=("Country_clean", lambda s: s.mode().iloc[0] if len(s.mode()) > 0 else "Unknown"),
    ).reset_index().sort_values(by="Total_Incidents", ascending=False).reset_index(drop=True)

    # 6. Aggregate by coastal point for clean, fast Plotly world maps (bubble size = incident count)
    point_agg = gdf.groupby(["Country_clean", "Area_clean", "latitude", "longitude", "Cluster_Name"]).agg(
        Incidents=("Case Number", "count"),
        Fatal_Count=("Fatal_clean", lambda s: (s == "Y").sum()),
        Top_Activity=("Activity_group", lambda s: s.mode().iloc[0] if len(s.mode()) > 0 else "Unknown"),
    ).reset_index()
    point_agg["Fatality_Rate_Pct"] = ((point_agg["Fatal_Count"] / point_agg["Incidents"]) * 100).round(2)

    fig_map = px.scatter_geo(
        point_agg,
        lat="latitude",
        lon="longitude",
        size="Incidents",
        size_max=32,
        color="Cluster_Name",
        hover_name="Area_clean",
        hover_data={
            "Country_clean": True,
            "Incidents": True,
            "Fatality_Rate_Pct": True,
            "Top_Activity": True,
            "latitude": False,
            "longitude": False,
        },
        title=f"Coastal incident clusters (K-means k={cluster_count}, {coverage_pct}% area coverage)",
        projection="natural earth",
    )
    fig_map.update_geos(showcoastlines=True, coastlinecolor="#94A3B8", showland=True, landcolor="#F1F5F9")
    fig_map.update_layout(template="plotly_white", legend=dict(orientation="h", yanchor="bottom", y=-0.25))

    optics_points = gdf.groupby(["Country_clean", "Area_clean", "latitude", "longitude", "OPTICS_Label"]).agg(
        Incidents=("Case Number", "count"),
    ).reset_index()
    fig_optics_map = px.scatter_geo(
        optics_points,
        lat="latitude",
        lon="longitude",
        size="Incidents",
        size_max=28,
        color="OPTICS_Label",
        hover_name="Area_clean",
        hover_data={"Country_clean": True, "Incidents": True, "latitude": False, "longitude": False},
        title="Density-Based Coastal Hotspots — OPTICS Clustering (Lab 8 Comparison)",
        projection="natural earth",
    )
    fig_optics_map.update_geos(showcoastlines=True, coastlinecolor="#94A3B8", showland=True, landcolor="#F1F5F9")
    fig_optics_map.update_layout(template="plotly_white", legend=dict(orientation="h", yanchor="bottom", y=-0.25))

    return {
        "geo_df": gdf,
        "coverage_pct": coverage_pct,
        "area_count": area_count,
        "country_centroid_count": country_centroid_count,
        "sjoin_matched": sjoin_matched,
        "cluster_summary": cluster_summary,
        "optics_summary": optics_summary,
        "fig_map": fig_map,
        "fig_optics_map": fig_optics_map,
        "kmeans_model": kmeans,
        "optics_model": optics,
    }


# ==============================================================================
# External Bonus Query: World Bank Tourism Correlation [+1 point] — Owner: Romain Thepaut
# ==============================================================================

# Function for comparing reported incidents per million arrivals and their descriptive correlations
# Input: merged_df (pd.DataFrame) from clean_and_merge_tourism()
# Output: dictionary with enriched DataFrame, correlations, country ranking, and Plotly figures
def query_tourism_enrichment(merged_df):
    df_bonus = merged_df.copy()
    start_year, end_year = df_bonus["Year"].min(), df_bonus["Year"].max()
    period = f"{start_year}–{end_year}"

    # 1. Compute Shark Attacks per 1 Million International Tourists
    df_bonus["attacks_per_1M_tourists"] = (
        (df_bonus["annual_attacks"] / df_bonus["Arrivals"]) * 1_000_000
    ).round(4)

    # 2. Global Pearson and Spearman correlation across country-year observations
    p_corr, p_val = pearsonr(df_bonus["Arrivals"], df_bonus["annual_attacks"])
    s_corr, s_val = spearmanr(df_bonus["Arrivals"], df_bonus["annual_attacks"])

    # 3. Compare the eight countries and territories with the most reports
    country_comparison = df_bonus.groupby("Country_clean").agg(
        Years_Observed=("Year", "nunique"),
        Total_Attacks=("annual_attacks", "sum"),
        Total_Tourist_Arrivals=("Arrivals", "sum"),
    ).reset_index()
    country_comparison["attacks_per_1M_tourists"] = (
        (country_comparison["Total_Attacks"] / country_comparison["Total_Tourist_Arrivals"]) * 1_000_000
    ).round(3)
    country_comparison = (
        country_comparison.sort_values(by="Total_Attacks", ascending=False).head(8).reset_index(drop=True)
    )

    # 4. Clean Two-Panel Comparison Chart (no arbitrary visual multiplier)
    by_risk = country_comparison.sort_values(by="attacks_per_1M_tourists", ascending=False)
    fig_comparison = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            f"Reported incidents ({period})",
            "Reported incidents per million arrivals",
        ),
    )
    fig_comparison.add_trace(
        go.Bar(
            x=country_comparison["Country_clean"],
            y=country_comparison["Total_Attacks"],
            name="Total Attacks",
            marker_color="#0284C7",
            text=country_comparison["Total_Attacks"],
            textposition="outside",
        ),
        row=1, col=1,
    )
    fig_comparison.add_trace(
        go.Bar(
            x=by_risk["Country_clean"],
            y=by_risk["attacks_per_1M_tourists"],
            name="Reports / 1M Arrivals",
            marker_color="#DC2626",
            text=by_risk["attacks_per_1M_tourists"],
            textposition="outside",
        ),
        row=1, col=2,
    )
    fig_comparison.update_layout(
        title="Reported incidents and arrivals (World Bank ST.INT.ARVL)",
        template="plotly_white",
        showlegend=False,
    )

    # 5. Dual-axis time series for the United States
    us_data = df_bonus[df_bonus["Country_clean"] == "United States"].sort_values("Year")
    fig_dual_axis = go.Figure()
    fig_dual_axis.add_trace(go.Scatter(
        x=us_data["Year"],
        y=us_data["annual_attacks"],
        name="US Annual Shark Attacks",
        mode="lines+markers",
        line=dict(color="#0F172A", width=3),
    ))
    fig_dual_axis.add_trace(go.Scatter(
        x=us_data["Year"],
        y=us_data["Arrivals"] / 1_000_000,
        name="US Tourist Arrivals (Millions)",
        mode="lines+markers",
        line=dict(color="#0F766E", width=3),
        yaxis="y2",
    ))
    fig_dual_axis.update_layout(
        title=f"United States: annual incident reports and arrivals ({period})",
        xaxis=dict(title="Year"),
        yaxis=dict(title=dict(text="Annual Attacks", font=dict(color="#0F172A"))),
        yaxis2=dict(
            title=dict(text="Tourist Arrivals (M)", font=dict(color="#0F766E")),
            overlaying="y",
            side="right",
        ),
        template="plotly_white",
    )

    return {
        "enriched_df": df_bonus,
        "pearson_corr": float(p_corr),
        "pearson_pval": float(p_val),
        "spearman_corr": float(s_corr),
        "spearman_pval": float(s_val),
        "country_comparison": country_comparison,
        "fig_comparison": fig_comparison,
        "fig_dual_axis": fig_dual_axis,
    }

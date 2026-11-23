# -*- coding: utf-8 -*-
# Module containing the 4 analytical queries and the external tourism bonus analysis
# Aligned with Final_project.pdf and ESILV Labs 7, 8, and 9

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr, spearmanr
from mlxtend.frequent_patterns import apriori, association_rules
from prophet import Prophet
from sklearn.cluster import KMeans, OPTICS


# ==============================================================================
# Query 1: Grouping & Aggregation [1 point] — Owner: Baptiste Noailhac
# ==============================================================================

# Function for computing grouping indicators (top countries, activities, fatality rates)
# Input: cleaned shark_df (pd.DataFrame), top_n (int)
# Output: dictionary with summary DataFrames and Plotly bar figures
def query_grouping_analysis(shark_df, top_n=10):
    # 1. Group by Country_clean to get total attacks, fatal attacks, and fatality rate
    country_summary = shark_df.groupby('Country_clean').agg(
        total_attacks=('Country_clean', 'count'),
        fatal_attacks=('Fatal_clean', lambda s: (s == 'Y').sum()),
        non_fatal_attacks=('Fatal_clean', lambda s: (s == 'N').sum())
    ).reset_index()
    country_summary['fatality_rate_pct'] = (
        (country_summary['fatal_attacks'] / country_summary['total_attacks']) * 100
    ).round(2)
    top_countries = country_summary.sort_values(by='total_attacks', ascending=False).head(top_n).reset_index(drop=True)

    # 2. Group by Activity_group
    activity_summary = shark_df.groupby('Activity_group').agg(
        total_attacks=('Activity_group', 'count'),
        fatal_attacks=('Fatal_clean', lambda s: (s == 'Y').sum())
    ).reset_index()
    activity_summary['fatality_rate_pct'] = (
        (activity_summary['fatal_attacks'] / activity_summary['total_attacks']) * 100
    ).round(2)
    activity_summary = activity_summary.sort_values(by='total_attacks', ascending=False).reset_index(drop=True)

    # 3. Create interactive Plotly figure for Top Countries
    fig_countries = px.bar(
        top_countries.sort_values(by='total_attacks', ascending=True),
        x='total_attacks',
        y='Country_clean',
        orientation='h',
        color='fatality_rate_pct',
        color_continuous_scale='Reds',
        labels={'total_attacks': 'Total Shark Attacks', 'Country_clean': 'Country', 'fatality_rate_pct': 'Fatality Rate (%)'},
        title=f"Top {top_n} Countries by Shark Attacks (1960-2023) & Fatality Rate",
        template='plotly_white'
    )
    fig_countries.update_layout(height=400)

    # 4. Create grouped bar figure for Activities
    fig_activity = px.bar(
        activity_summary,
        x='Activity_group',
        y='total_attacks',
        color='fatality_rate_pct',
        color_continuous_scale='Turbo',
        labels={'total_attacks': 'Incident Count', 'Activity_group': 'Victim Activity', 'fatality_rate_pct': 'Fatality Rate (%)'},
        title="Shark Attacks and Fatality Rate by Victim Activity",
        template='plotly_white'
    )
    fig_activity.update_layout(height=400)

    return {
        "top_countries": top_countries,
        "activity_summary": activity_summary,
        "fig_countries": fig_countries,
        "fig_activity": fig_activity,
        "fig": fig_countries
    }


# ==============================================================================
# Query 2: Frequent Pattern Mining (Apriori) [2 points] — Owner: Baptiste Noailhac
# ==============================================================================

# Function for extracting frequent itemsets and association rules using mlxtend Apriori
# Input: cleaned shark_df (pd.DataFrame), min_support (float), min_lift (float)
# Output: dictionary with frequent itemsets, association rules DataFrame, and Plotly figures
def query_frequent_patterns(shark_df, min_support=0.04, min_lift=1.05):
    # Select discrete columns for transaction mining
    feature_cols = ['Country_clean', 'Activity_group', 'Type_clean', 'Season', 'Time_of_day', 'Fatal_clean']
    top_5_countries = shark_df['Country_clean'].value_counts().head(5).index

    subset = shark_df[feature_cols].copy()
    subset['Country_clean'] = subset['Country_clean'].apply(
        lambda c: f"Country={c}" if c in top_5_countries else "Country=Other"
    )
    subset['Activity_group'] = "Activity=" + subset['Activity_group'].astype(str)
    subset['Type_clean'] = "Type=" + subset['Type_clean'].astype(str)
    subset['Season'] = "Season=" + subset['Season'].astype(str)
    subset['Time_of_day'] = "Time=" + subset['Time_of_day'].astype(str)
    subset['Fatal_clean'] = "Fatal=" + subset['Fatal_clean'].astype(str)

    # One-hot encode into boolean matrix
    one_hot = pd.get_dummies(subset, prefix="", prefix_sep="", dtype=bool)

    # Run Apriori
    itemsets = apriori(one_hot, min_support=min_support, use_colnames=True)

    # Generate association rules if frequent itemsets found
    if not itemsets.empty:
        rules = association_rules(itemsets, metric="lift", min_threshold=min_lift)
        rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
        rules = rules.sort_values(by="lift", ascending=False).reset_index(drop=True)
    else:
        rules = pd.DataFrame()

    # Create Plotly scatter plot (Support vs Confidence colored by Lift)
    if not rules.empty:
        fig_rules = px.scatter(
            rules.head(50),
            x='support',
            y='confidence',
            color='lift',
            size='lift',
            hover_data=['antecedents_str', 'consequents_str'],
            labels={'support': 'Support', 'confidence': 'Confidence', 'lift': 'Lift'},
            title=f"Apriori Association Rules (min_support={min_support}, min_lift={min_lift})",
            color_continuous_scale='Viridis',
            template='plotly_white'
        )
        fig_rules.update_layout(height=450)
    else:
        fig_rules = go.Figure()
        fig_rules.add_annotation(text="No rules generated with current thresholds", showarrow=False)

    return {
        "itemsets": itemsets,
        "rules": rules,
        "fig_rules": fig_rules,
        "fig": fig_rules
    }


# ==============================================================================
# Query 3: Temporal Analysis & Forecasting (Prophet) [2 points] — Owner: Romain Thepaut
# ==============================================================================

# Function for analyzing temporal seasonality and forecasting shark attacks with Prophet
# Input: cleaned shark_df (pd.DataFrame), forecast_years (int)
# Output: dictionary with monthly/annual series, Prophet forecast DataFrame, and Plotly figures
def query_temporal_forecast(shark_df, forecast_years=5):
    # 1. Build annual time series for reliable long-term trend forecasting
    annual_ts = shark_df.groupby('Year').size().reset_index(name='y')
    annual_ts['ds'] = pd.to_datetime(annual_ts['Year'].astype(str) + '-01-01')

    # 2. Fit Prophet model with 95% uncertainty interval
    model = Prophet(interval_width=0.95, yearly_seasonality=False)
    model.fit(annual_ts[['ds', 'y']])

    # 3. Create future dataframe for 5-year forecast
    future = model.make_future_dataframe(periods=forecast_years, freq='YE')
    forecast = model.predict(future)

    # 4. Monthly seasonality profile by Hemisphere
    north_countries = ['United States', 'Bahamas, The', 'Mexico', 'Egypt, Arab Rep.']
    south_countries = ['Australia', 'South Africa', 'Brazil', 'New Zealand']

    monthly_north = shark_df[shark_df['Country_clean'].isin(north_countries)].dropna(subset=['Month']).groupby('Month').size().reset_index(name='Attacks_North')
    monthly_south = shark_df[shark_df['Country_clean'].isin(south_countries)].dropna(subset=['Month']).groupby('Month').size().reset_index(name='Attacks_South')
    seasonality = pd.merge(monthly_north, monthly_south, on='Month', how='outer').fillna(0).sort_values(by='Month')
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    seasonality['Month_Name'] = seasonality['Month'].astype(int).apply(lambda m: month_labels[m-1] if 1 <= m <= 12 else str(m))

    # 5. Build Seasonality Figure
    fig_seasonality = go.Figure()
    fig_seasonality.add_trace(go.Bar(
        x=seasonality['Month_Name'],
        y=seasonality['Attacks_North'],
        name='Northern Hemisphere (USA, Bahamas...)',
        marker_color='#1E88E5'
    ))
    fig_seasonality.add_trace(go.Bar(
        x=seasonality['Month_Name'],
        y=seasonality['Attacks_South'],
        name='Southern Hemisphere (Australia, South Africa...)',
        marker_color='#D81B60'
    ))
    fig_seasonality.update_layout(
        title="Hemisphere Seasonality Comparison (Peak in Northern Summer vs. Southern Summer)",
        xaxis_title="Month",
        yaxis_title="Incident Count",
        barmode='group',
        template='plotly_white',
        height=400
    )

    # 6. Build Interactive Prophet Forecast Figure
    fig_forecast = go.Figure()
    # Historical actual values
    fig_forecast.add_trace(go.Scatter(
        x=annual_ts['ds'].dt.year,
        y=annual_ts['y'],
        mode='markers+lines',
        name='Historical Observed',
        marker=dict(color='#0F172A', size=6)
    ))
    # Forecast trendline
    fig_forecast.add_trace(go.Scatter(
        x=forecast['ds'].dt.year,
        y=forecast['yhat'],
        mode='lines',
        name='Prophet Trend (yhat)',
        line=dict(color='#0284C7', width=3)
    ))
    # Uncertainty intervals
    fig_forecast.add_trace(go.Scatter(
        x=forecast['ds'].dt.year,
        y=forecast['yhat_upper'],
        mode='lines',
        line=dict(width=0),
        showlegend=False
    ))
    fig_forecast.add_trace(go.Scatter(
        x=forecast['ds'].dt.year,
        y=forecast['yhat_lower'],
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(2, 132, 199, 0.2)',
        name='95% Confidence Interval'
    ))
    fig_forecast.update_layout(
        title=f"Prophet Time-Series Forecast of Global Shark Attacks (Next {forecast_years} Years)",
        xaxis_title="Year",
        yaxis_title="Annual Incident Count",
        template='plotly_white',
        height=450
    )

    return {
        "annual_ts": annual_ts,
        "forecast": forecast,
        "seasonality": seasonality,
        "fig_forecast": fig_forecast,
        "fig_seasonality": fig_seasonality,
        "fig": fig_forecast
    }


# ==============================================================================
# Query 4: Spatial Analysis & Clustering (GeoPandas + OPTICS/KMeans) [2 points] — Owner: Louis Le Forestier
# ==============================================================================

# Function for geocoding coastal areas and running spatial hotspot clustering
# Input: cleaned shark_df (pd.DataFrame), geo_df (pd.DataFrame), shp_path (str), n_clusters (int)
# Output: dictionary with clustered GeoDataFrame, cluster summary table, and Plotly map figure
def query_spatial_clustering(shark_df, geo_df, shp_path=None, n_clusters=6):
    # 1. Merge shark attacks with cached coordinates
    spatial_df = pd.merge(
        shark_df,
        geo_df,
        on=['Country_clean', 'Area_clean'],
        how='inner'
    ).copy()

    if spatial_df.empty:
        raise ValueError("No matching coordinates found between shark_df and geo_df.")

    # 2. Run KMeans spatial clustering
    coords = spatial_df[['latitude', 'longitude']].values
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    spatial_df['cluster'] = kmeans.fit_predict(coords)

    # 3. Label clusters by geographical region based on cluster centers
    centers = kmeans.cluster_centers_
    cluster_labels = {}
    for i, (lat, lon) in enumerate(centers):
        if lat > 15 and -100 <= lon <= -60:
            cluster_labels[i] = "US East Coast / Florida"
        elif lat > 15 and -130 <= lon < -100:
            cluster_labels[i] = "US West Coast / California"
        elif 10 <= lat <= 30 and -165 <= lon <= -145:
            cluster_labels[i] = "Hawaii / Pacific Islands"
        elif -45 <= lat <= -10 and 130 <= lon <= 160:
            cluster_labels[i] = "East Australia / New Zealand"
        elif -40 <= lat <= -15 and 100 <= lon < 130:
            cluster_labels[i] = "Western Australia"
        elif -40 <= lat <= -20 and 15 <= lon <= 40:
            cluster_labels[i] = "South Africa"
        else:
            cluster_labels[i] = f"Hotspot Cluster {i+1}"
    spatial_df['cluster_name'] = spatial_df['cluster'].map(cluster_labels)

    # 4. Summarize clusters
    cluster_summary = spatial_df.groupby('cluster_name').agg(
        incident_count=('Country_clean', 'count'),
        fatal_count=('Fatal_clean', lambda s: (s == 'Y').sum()),
        dominant_activity=('Activity_group', lambda s: s.value_counts().index[0] if not s.empty else "N/A"),
        avg_lat=('latitude', 'mean'),
        avg_lon=('longitude', 'mean')
    ).reset_index()
    cluster_summary['fatality_rate_pct'] = (
        (cluster_summary['fatal_count'] / cluster_summary['incident_count']) * 100
    ).round(2)
    cluster_summary = cluster_summary.sort_values(by='incident_count', ascending=False).reset_index(drop=True)

    # 5. Plotly interactive scatter_geo world map
    fig_map = px.scatter_geo(
        spatial_df,
        lat='latitude',
        lon='longitude',
        color='cluster_name',
        hover_name='Area_clean',
        hover_data=['Country_clean', 'Activity_group', 'Fatal_clean', 'Year'],
        title="Global Coastal Shark Attack Hotspots (K-Means & OPTICS Spatial Clusters)",
        template='plotly_white',
        projection='natural earth'
    )
    fig_map.update_geos(showcountries=True, countrycolor="#D1D5DB", showocean=True, oceancolor="#F0F9FF")
    fig_map.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))

    return {
        "spatial_df": spatial_df,
        "cluster_summary": cluster_summary,
        "fig_map": fig_map,
        "fig": fig_map
    }


# ==============================================================================
# External Bonus Query: World Bank Tourism Correlation [+1 point] — Owner: Romain Thepaut
# ==============================================================================

# Function for computing tourism-adjusted shark attack rates and correlations (1995-2020)
# Input: merged_df (pd.DataFrame) from clean_and_merge_tourism()
# Output: dictionary with enriched DataFrame, correlation metrics, and Plotly comparison figures
def query_tourism_enrichment(merged_df):
    # 1. Compute normalized risk rate per 1 Million tourist arrivals
    df = merged_df.copy()
    df['attacks_per_1M_tourists'] = (df['annual_attacks'] / df['Arrivals']) * 1_000_000

    # 2. Compute Pearson and Spearman correlation
    p_corr, p_pval = pearsonr(df['Arrivals'], df['annual_attacks'])
    s_corr, s_pval = spearmanr(df['Arrivals'], df['annual_attacks'])

    # 3. Aggregate by country over the 26-year period (1995-2020)
    country_agg = df.groupby('Country_clean').agg(
        total_attacks=('annual_attacks', 'sum'),
        total_arrivals=('Arrivals', 'sum')
    ).reset_index()
    country_agg['attacks_per_1M_tourists'] = (
        (country_agg['total_attacks'] / country_agg['total_arrivals']) * 1_000_000
    ).round(3)
    country_agg = country_agg[country_agg['total_attacks'] >= 5].sort_values(
        by='total_attacks', ascending=False
    ).reset_index(drop=True)

    # 4. Build Comparative Ranking Figure (Raw Attacks vs. Risk per 1M Tourists)
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=country_agg['Country_clean'].head(8),
        y=country_agg['total_attacks'].head(8),
        name='Raw Shark Attack Count',
        marker_color='#0284C7'
    ))
    fig_comp.add_trace(go.Bar(
        x=country_agg['Country_clean'].head(8),
        y=country_agg['attacks_per_1M_tourists'].head(8) * 50,  # Scaled for dual visibility
        name='Attacks per 1M Tourists (Scaled x50)',
        marker_color='#F59E0B'
    ))
    fig_comp.update_layout(
        title="Raw Attacks vs. Relative Tourism Risk (Attacks per 1M Arrivals, 1995-2020)",
        xaxis_title="Country",
        yaxis_title="Metric Value",
        barmode='group',
        template='plotly_white',
        height=420
    )

    # 5. Build Global Time-Series Dual-Axis Trend (Attacks vs. Global Tourism)
    global_trends = df.groupby('Year').agg(
        total_attacks=('annual_attacks', 'sum'),
        total_arrivals=('Arrivals', 'sum')
    ).reset_index()

    fig_trends = go.Figure()
    fig_trends.add_trace(go.Scatter(
        x=global_trends['Year'],
        y=global_trends['total_attacks'],
        name='Global Shark Attacks',
        mode='lines+markers',
        line=dict(color='#DC2626', width=3)
    ))
    fig_trends.add_trace(go.Scatter(
        x=global_trends['Year'],
        y=global_trends['total_arrivals'] / 1_000_000,
        name='Tourist Arrivals (Millions)',
        mode='lines+markers',
        line=dict(color='#2563EB', width=3, dash='dot'),
        yaxis='y2'
    ))
    fig_trends.update_layout(
        title=f"Parallel Evolution: Shark Attacks vs. International Tourist Arrivals (Pearson r={p_corr:.2f})",
        xaxis_title="Year",
        yaxis=dict(title='Global Shark Attacks', tickfont=dict(color='#DC2626')),
        yaxis2=dict(title='Tourist Arrivals (Millions)', tickfont=dict(color='#2563EB'), overlaying='y', side='right'),
        template='plotly_white',
        height=450
    )

    return {
        "enriched_df": df,
        "country_agg": country_agg,
        "global_trends": global_trends,
        "pearson_corr": p_corr,
        "pearson_pval": p_pval,
        "spearman_corr": s_corr,
        "spearman_pval": s_pval,
        "fig_comp": fig_comp,
        "fig_trends": fig_trends,
        "fig": fig_trends
    }

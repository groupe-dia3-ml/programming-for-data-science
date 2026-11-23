# Module containing the 4 analytical queries and the external tourism bonus analysis
# Aligned with Final_project.pdf and ESILV Labs 7, 8, and 9

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ==============================================================================
# Query 1: Grouping & Aggregation [1 point] — Owner: Baptiste Noailhac
# ==============================================================================

# Function for computing grouping indicators (top countries, activities, fatality rates)
# Input: cleaned shark_df (pd.DataFrame), top_n (int)
# Output: dictionary with summary DataFrames and Plotly bar figures
def query_grouping_analysis(shark_df, top_n=10):
    # TODO (Baptiste):
    # 1. Group by Country_clean to get total attacks, fatal attacks, and fatality_rate (%) -> keep top_n
    # 2. Group by Activity_group to get total attacks and fatality_rate (%)
    # 3. Group by cleaned shark Species to compare top species and fatality rates
    # 4. Create interactive Plotly bar charts for countries and activities
    raise NotImplementedError("TODO: implement query_grouping_analysis()")


# ==============================================================================
# Query 2: Frequent Pattern Mining (Apriori) [2 points] — Owner: Baptiste Noailhac
# ==============================================================================

# Function for extracting frequent itemsets and association rules using mlxtend Apriori
# Input: cleaned shark_df (pd.DataFrame), min_support (float), min_lift (float)
# Output: dictionary with frequent itemsets, association rules DataFrame, and Plotly figures
def query_frequent_patterns(shark_df, min_support=0.05, min_lift=1.05):
    # TODO (Baptiste):
    # 1. Select discrete columns (e.g., Country_top, Activity_group, Type, Season, Time_of_day, Fatal_clean)
    # 2. One-hot encode into a boolean DataFrame (pd.get_dummies(..., dtype=bool) or TransactionEncoder)
    # 3. Run support sensitivity analysis across multiple min_support thresholds (like Lab 9)
    # 4. Run apriori(df_bool, min_support=min_support, use_colnames=True)
    # 5. Run association_rules(frequent_itemsets, metric='lift', min_threshold=min_lift)
    # 6. Build Plotly scatter plot (support vs confidence, colored by lift)
    raise NotImplementedError("TODO: implement query_frequent_patterns()")


# ==============================================================================
# Query 3: Temporal Analysis & Forecasting (Prophet) [2 points] — Owner: Romain Thepaut
# ==============================================================================

# Function for analyzing temporal seasonality and forecasting shark attacks with Prophet
# Input: cleaned shark_df (pd.DataFrame), forecast_years (int)
# Output: dictionary with monthly/annual series, Prophet forecast DataFrame, and Plotly figures
def query_temporal_forecast(shark_df, forecast_years=5):
    # TODO (Romain):
    # 1. Build annual or monthly time series (columns 'ds' and 'y') from 1960 to last complete year
    # 2. Compare monthly seasonality between Northern Hemisphere (e.g., United States)
    #    and Southern Hemisphere (e.g., Australia, South Africa)
    # 3. Fit Prophet(interval_width=0.95) on the time series (like Lab 7)
    # 4. Generate future dataframe for forecast_years and predict yhat, yhat_lower, yhat_upper
    # 5. Build Plotly figures for hemisphere seasonality and Prophet forecast
    raise NotImplementedError("TODO: implement query_temporal_forecast()")


# ==============================================================================
# Query 4: Spatial Analysis & Clustering (GeoPandas + OPTICS/KMeans) [2 points] — Owner: Louis Le Forestier
# ==============================================================================

# Function for geocoding coastal areas and running spatial hotspot clustering
# Input: cleaned shark_df (pd.DataFrame), geo_df (pd.DataFrame), shp_path (str), n_clusters (int)
# Output: dictionary with clustered GeoDataFrame, cluster summary table, and Plotly map figure
def query_spatial_clustering(shark_df, geo_df, shp_path=None, n_clusters=6):
    # TODO (Louis):
    # 1. Merge shark_df with geo_df on ['Country_clean', 'Area_clean'] to attach latitude and longitude
    # 2. Build GeoDataFrame using shapely Point(longitude, latitude) with crs='EPSG:4326'
    # 3. Optional spatial join (sjoin) with ne_110m_admin_0_countries.shp (like Lab 8)
    # 4. Run KMeans(n_clusters=n_clusters, random_state=42) and OPTICS(...) on [['latitude', 'longitude']]
    # 5. Summarize each cluster (count, fatality rate, dominant activity)
    # 6. Build interactive Plotly scatter_geo world map colored by spatial cluster
    raise NotImplementedError("TODO: implement query_spatial_clustering()")


# ==============================================================================
# External Bonus Query: World Bank Tourism Correlation [+1 point] — Owner: Romain Thepaut
# ==============================================================================

# Function for computing tourism-adjusted shark attack rates and correlations (1995-2020)
# Input: merged_df (pd.DataFrame) from clean_and_merge_tourism()
# Output: dictionary with enriched DataFrame, correlation metrics, and Plotly comparison figures
def query_tourism_enrichment(merged_df):
    # TODO (Romain):
    # 1. Compute attacks_per_1M_tourists = (annual_attacks / Arrivals) * 1_000_000
    # 2. Compute Pearson and Spearman correlation between Arrivals and annual_attacks
    # 3. Build comparative ranking: Top countries by raw attacks vs. attacks per 1M tourists
    # 4. Build Plotly dual-axis trend figure (attacks vs. tourist arrivals over 1995-2020)
    raise NotImplementedError("TODO: implement query_tourism_enrichment()")

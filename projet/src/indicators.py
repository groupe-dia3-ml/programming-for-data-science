# -*- coding: utf-8 -*-
"""
Module containing modular analytical query implementations for the Final Project.
Includes:
- Query 1: Grouping / Aggregation indicator [1 pt]
- Query 2: Frequent Pattern Mining indicator (Apriori / SPM) [2 pts]
- Query 3: Temporal Dynamics & Forecasting indicator (Prophet) [2 pts]
- Query 4: Spatial Information & Clustering indicator (OPTICS / K-Means) [2 pts]
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.cluster import OPTICS, KMeans


# ==============================================================================
# Query 1: Aggregation & Grouping Query [1 point]
# ==============================================================================

def compute_aggregation_query(df: pd.DataFrame, 
                              group_col: str, 
                              target_col: str) -> pd.DataFrame:
    """
    Function for calculating group-level summary indicators (e.g. maximal, mean, sum).
    
    Input:
        df (pd.DataFrame): Input multidimensional dataset.
        group_col (str): Categorical column used for grouping.
        target_col (str): Numeric column on which aggregates are calculated.
    Output:
        pd.DataFrame: Sorted DataFrame with aggregated metrics (Sum, Mean, Max, Count).
    """
    # Group by the specified categorical variable and compute comprehensive aggregations
    agg_df = df.groupby(group_col)[target_col].agg(
        Total_Sum='sum',
        Average='mean',
        Maximum='max',
        Event_Count='count'
    ).reset_index()
    
    # Sort descending by Total_Sum for immediate ranking insight
    agg_df = agg_df.sort_values(by='Total_Sum', ascending=False)
    
    return agg_df


# ==============================================================================
# Query 2: Frequent Pattern Mining Query [2 points]
# ==============================================================================

def compute_pattern_mining_query(df: pd.DataFrame, 
                                 feature_cols: List[str], 
                                 min_support: float = 0.05,
                                 min_lift: float = 1.1) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Function for extracting frequent itemsets and association rules from categorical features.
    
    Input:
        df (pd.DataFrame): Input dataset.
        feature_cols (List[str]): Categorical attributes to mine.
        min_support (float): Minimum support threshold sigma.
        min_lift (float): Minimum lift threshold for rule quality filtering.
    Output:
        Tuple[pd.DataFrame, pd.DataFrame]: (frequent_itemsets, association_rules_df)
    """
    # Subset selected features and convert to string type
    subset = df[feature_cols].dropna().astype(str)
    
    # One-hot encode the selected categorical features into boolean format
    one_hot = pd.get_dummies(subset, prefix_sep='=')
    
    # Run the Apriori algorithm
    itemsets = apriori(one_hot, min_support=min_support, use_colnames=True)
    
    # Generate association rules if frequent itemsets exist
    if not itemsets.empty:
        rules = association_rules(itemsets, metric="lift", min_threshold=min_lift)
        # Sort rules descending by support
        rules = rules.sort_values(by="support", ascending=False)
    else:
        rules = pd.DataFrame()
        
    return itemsets, rules


# ==============================================================================
# Query 3: Temporal Dynamics & Forecasting Query [2 points]
# ==============================================================================

def compute_temporal_trend_query(df: pd.DataFrame, 
                                 date_col: str, 
                                 value_col: str, 
                                 freq: str = 'M') -> pd.DataFrame:
    """
    Function for temporal aggregation and time-series evolution.
    Prepares time series for Prophet or rolling trend models.
    
    Input:
        df (pd.DataFrame): Input dataset.
        date_col (str): Column name containing datetime stamps.
        value_col (str): Column name containing observation values to aggregate.
        freq (str): Resampling frequency ('D' for daily, 'W' for weekly, 'M' for monthly).
    Output:
        pd.DataFrame: Resampled time series with date (ds) and value (y).
    """
    # Convert date column to datetime format
    temp_df = df.copy()
    temp_df['ds'] = pd.to_datetime(temp_df[date_col], errors='coerce')
    temp_df = temp_df.dropna(subset=['ds'])
    
    # Group by the specified frequency
    ts = temp_df.set_index('ds').resample(freq)[value_col].agg(['sum', 'mean', 'count']).reset_index()
    ts.rename(columns={'sum': 'y'}, inplace=True)
    
    return ts


# ==============================================================================
# Query 4: Spatial Information & Clustering Query [2 points]
# ==============================================================================

def compute_spatial_clustering_query(df: pd.DataFrame, 
                                     lat_col: str, 
                                     lon_col: str, 
                                     algorithm: str = "optics",
                                     min_samples: int = 5,
                                     n_clusters: int = 5) -> pd.DataFrame:
    """
    Function for spatial cluster identification on geographic coordinates.
    
    Input:
        df (pd.DataFrame): Input dataset with geographic coordinates.
        lat_col (str): Column name for Latitude.
        lon_col (str): Column name for Longitude.
        algorithm (str): 'optics' or 'kmeans'.
        min_samples (int): OPTICS min_samples parameter.
        n_clusters (int): KMeans number of clusters.
    Output:
        pd.DataFrame: DataFrame containing original coordinates and cluster labels.
    """
    # Filter valid coordinates (drop missing or out-of-range latitude/longitude)
    spatial_df = df.dropna(subset=[lat_col, lon_col]).copy()
    coords = spatial_df[[lat_col, lon_col]].values
    
    if algorithm.lower() == "optics":
        # Fit OPTICS clustering algorithm
        clusterer = OPTICS(min_samples=min_samples)
        spatial_df['cluster'] = clusterer.fit_predict(coords)
    else:
        # Fit KMeans clustering algorithm
        clusterer = KMeans(n_clusters=n_clusters, random_state=42)
        spatial_df['cluster'] = clusterer.fit_predict(coords)
        
    return spatial_df

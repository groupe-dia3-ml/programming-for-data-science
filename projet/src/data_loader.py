# -*- coding: utf-8 -*-
"""
Module for loading, inspecting, and preprocessing multidimensional datasets.
Strictly adheres to ESILV Programming for Data Science project conventions.
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Function for reading and loading a CSV multidimensional dataset.
    
    Input:
        file_path (str): Relative or absolute path to the dataset file.
    Output:
        pd.DataFrame: Cleaned Pandas DataFrame.
    """
    # Check if the file exists before attempting to read it
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")
    
    # Read CSV file using pandas
    df = pd.read_csv(file_path)
    
    # Clean whitespace in column names to avoid indexing errors
    df.columns = df.columns.str.strip()
    
    return df


def summarize_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Function to profile and summarize the multidimensional dataset.
    Generates required metrics: shape, data types, missing values, and value ranges.
    
    Input:
        df (pd.DataFrame): Input DataFrame to summarize.
    Output:
        dict: Dictionary containing summary statistics and metadata.
    """
    # Compute basic dimensions (rows, columns)
    n_rows, n_cols = df.shape
    
    # Inspect data types of each column
    dtypes_dict = df.dtypes.astype(str).to_dict()
    
    # Compute count of missing values per column
    missing_dict = df.isnull().sum().to_dict()
    
    # Calculate summary statistics (ranges: min, max, quantiles) for numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    ranges_dict = {}
    if not numeric_df.empty:
        for col in numeric_df.columns:
            ranges_dict[col] = {
                "min": float(numeric_df[col].min()),
                "max": float(numeric_df[col].max()),
                "mean": float(numeric_df[col].mean()),
                "std": float(numeric_df[col].std())
            }
            
    summary = {
        "num_rows": n_rows,
        "num_cols": n_cols,
        "columns": list(df.columns),
        "data_types": dtypes_dict,
        "missing_values": missing_dict,
        "numeric_ranges": ranges_dict
    }
    
    return summary


def print_summary_report(summary: Dict[str, Any]) -> None:
    """
    Function for displaying a clean human-readable summary report in the console or notebook.
    
    Input:
        summary (dict): Output from summarize_dataset.
    Output:
        None (prints report to stdout).
    """
    print("=" * 70)
    print("MULTIDIMENSIONAL DATASET SUMMARY REPORT")
    print("=" * 70)
    print(f"Total Rows (Records):    {summary['num_rows']:,}")
    print(f"Total Columns (Fields):  {summary['num_cols']}")
    print("-" * 70)
    print(f"{'Column Name':<30} | {'Dtype':<12} | {'Missing Values':<15}")
    print("-" * 70)
    for col in summary['columns']:
        dtype = summary['data_types'].get(col, '')
        missing = summary['missing_values'].get(col, 0)
        pct = (missing / summary['num_rows']) * 100 if summary['num_rows'] > 0 else 0
        print(f"{col:<30} | {dtype:<12} | {missing:<7} ({pct:.1f}%)")
    print("=" * 70)

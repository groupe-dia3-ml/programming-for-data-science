# -*- coding: utf-8 -*-
# Module for loading, exploring, cleaning, and merging the project datasets
# Owner: Louis Le Forestier
# Primary dataset: Global Shark Attack (GSAF - Kaggle mexwell)
# Bonus dataset: International tourism, number of arrivals (World Bank ST.INT.ARVL)

import os
import re
import pandas as pd
import numpy as np

# Mapping dictionary to align GSAF country names with World Bank official names
COUNTRY_MAPPING = {
    "USA": "United States",
    "UNITED STATES": "United States",
    "ENGLAND": "United Kingdom",
    "SCOTLAND": "United Kingdom",
    "WALES": "United Kingdom",
    "UNITED KINGDOM": "United Kingdom",
    "BAHAMAS": "Bahamas, The",
    "EGYPT": "Egypt, Arab Rep.",
    "RUSSIA": "Russian Federation",
    "SOUTH KOREA": "Korea, Rep.",
    "IRAN": "Iran, Islamic Rep.",
    "VENEZUELA": "Venezuela, RB",
    "HONG KONG": "Hong Kong SAR, China",
    "TURKEY": "Turkiye",
    "VIETNAM": "Viet Nam",
    "ST. MARTIN": "St. Martin (French part)",
}

# List of southern hemisphere countries for seasonal alignment
SOUTHERN_HEMISPHERE_COUNTRIES = {
    "Australia", "South Africa", "Brazil", "New Zealand", "Papua New Guinea",
    "Reunion", "New Caledonia", "Mozambique", "Fiji", "Chile", "Argentina",
    "Madagascar", "Mauritius", "Seychelles", "Vanuatu", "Solomon Islands"
}


# Function for loading the primary Global Shark Attack dataset (CSV or Excel)
# Input: file_path (str) - path to attacks.csv or GSAF5.xls inside projet/data/
# Output: raw pandas DataFrame of shark attacks
def load_shark_data(file_path):
    # Verify file existence on disk
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Shark dataset not found at '{file_path}'. See doc/DATA_SETUP.md."
        )

    # Detect file format and load accordingly
    if file_path.lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        # Load CSV using latin-1 encoding to preserve special characters
        df = pd.read_csv(file_path, encoding='latin-1')

    # Clean whitespace in column names
    df.columns = df.columns.str.strip()
    return df


# Function for loading the external World Bank tourism dataset (ST.INT.ARVL)
# Input: file_path (str) - path to tourism_arrivals.csv inside projet/data/
# Output: raw pandas DataFrame of international tourist arrivals
def load_tourism_data(file_path):
    # Verify file existence on disk
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Tourism dataset not found at '{file_path}'. See doc/DATA_SETUP.md."
        )

    # Read World Bank CSV skipping the first 4 metadata header rows
    df = pd.read_csv(file_path, skiprows=4)
    # Clean column headers
    df.columns = df.columns.str.strip()
    # Drop trailing empty column if created by export
    unnamed_cols = [c for c in df.columns if c.startswith('Unnamed:')]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
    return df


# Function for profiling and summarizing any dataset (mandatory EDA step)
# Input: df (pd.DataFrame), dataset_name (str)
# Output: dictionary with shape, dtypes, missing values, and value ranges
def summarize_dataset(df, dataset_name="Dataset"):
    # Extract dimensions
    n_rows, n_cols = df.shape

    # Data types dictionary
    dtypes_dict = df.dtypes.astype(str).to_dict()

    # Missing values count and percentage per column
    missing_counts = df.isna().sum().to_dict()
    missing_pct = ((df.isna().sum() / n_rows) * 100).round(2).to_dict() if n_rows > 0 else {}

    # Ranges for numeric features and unique counts for categorical features
    numeric_ranges = {}
    categorical_uniques = {}

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            valid_vals = df[col].dropna()
            if not valid_vals.empty:
                numeric_ranges[col] = {
                    "min": float(valid_vals.min()),
                    "max": float(valid_vals.max()),
                    "median": float(valid_vals.median())
                }
        else:
            categorical_uniques[col] = int(df[col].nunique(dropna=True))

    summary = {
        "dataset_name": dataset_name,
        "n_rows": n_rows,
        "n_cols": n_cols,
        "dtypes": dtypes_dict,
        "missing_counts": missing_counts,
        "missing_pct": missing_pct,
        "numeric_ranges": numeric_ranges,
        "categorical_uniques": categorical_uniques
    }
    return summary


# Helper function to extract month (1-12) from noisy raw Date strings
def _extract_month_from_date(date_str):
    if pd.isna(date_str):
        return np.nan
    s = str(date_str).lower()
    month_names = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    for m_str, m_num in month_names.items():
        if m_str in s:
            return m_num
    return np.nan


# Helper function to categorize seasons based on month and hemisphere
def _derive_season(month, country):
    if pd.isna(month):
        return "Unknown"
    m = int(month)
    is_south = country in SOUTHERN_HEMISPHERE_COUNTRIES
    if not is_south:
        if m in [6, 7, 8]:
            return "Summer"
        elif m in [9, 10, 11]:
            return "Autumn"
        elif m in [12, 1, 2]:
            return "Winter"
        else:
            return "Spring"
    else:
        if m in [12, 1, 2]:
            return "Summer"
        elif m in [3, 4, 5]:
            return "Autumn"
        elif m in [6, 7, 8]:
            return "Winter"
        else:
            return "Spring"


# Helper function to categorize raw Activity string into clean buckets
def _clean_activity(activity_str):
    if pd.isna(activity_str):
        return "Other"
    s = str(activity_str).lower()
    if any(k in s for k in ['surf', 'board', 'paddl', 'kayak', 'canoe']):
        return "Surfing"
    elif any(k in s for k in ['swim', 'bath', 'float', 'snork']):
        return "Swimming"
    elif any(k in s for k in ['div', 'scuba', 'spear', 'free-div']):
        return "Diving"
    elif any(k in s for k in ['fish', 'hook', 'net']):
        return "Fishing"
    elif any(k in s for k in ['wading', 'standing', 'treading', 'walking']):
        return "Wading"
    return "Other"


# Helper function to bucket noisy Time strings into 4 standard intervals
def _clean_time_of_day(time_str):
    if pd.isna(time_str):
        return "Unknown"
    s = str(time_str).strip().lower()
    # Direct keyword matches
    if any(k in s for k in ['morning', 'am', 'dawn']):
        return "Morning (06-12)"
    if any(k in s for k in ['afternoon', 'noon', 'pm', 'midday']):
        return "Afternoon (12-18)"
    if any(k in s for k in ['night', 'dusk', 'evening', 'sunset', 'midnight']):
        return "Evening/Night (18-06)"

    # Regex parse for HHhMM or HH:MM
    match = re.search(r'(\d{1,2})[h:]?(\d{2})?', s)
    if match:
        try:
            hour = int(match.group(1))
            if 6 <= hour < 12:
                return "Morning (06-12)"
            elif 12 <= hour < 18:
                return "Afternoon (12-18)"
            elif 18 <= hour <= 24 or 0 <= hour < 6:
                return "Evening/Night (18-06)"
        except ValueError:
            pass
    return "Unknown"


# Helper function to clean country names
def _clean_country_name(country_val):
    if pd.isna(country_val):
        return "Unknown"
    c_str = str(country_val).strip().rstrip('?').upper()
    if c_str in COUNTRY_MAPPING:
        return COUNTRY_MAPPING[c_str]
    return c_str.title()


# Function for cleaning and feature engineering the Global Shark Attack dataset
# Input: raw shark attacks DataFrame
# Output: cleaned DataFrame with Year, Month, Season, Country_clean, Activity_group, Time_of_day, Fatal_clean
def clean_shark_data(df):
    # Make an explicit working copy
    clean_df = df.copy()

    # Drop noisy metadata/administrative export columns not needed for KDD
    cols_to_drop = [
        'href', 'href formula', 'pdf', 'Case Number.1', 'Case Number.2',
        'original order', 'Investigator or Source'
    ]
    existing_drop = [c for c in cols_to_drop if c in clean_df.columns]
    unnamed_cols = [c for c in clean_df.columns if c.startswith('Unnamed:')]
    clean_df = clean_df.drop(columns=existing_drop + unnamed_cols, errors='ignore')

    # Convert Year to numeric and filter modern reliable reporting period (1960 to 2023)
    clean_df['Year_num'] = pd.to_numeric(clean_df['Year'], errors='coerce')
    clean_df = clean_df[(clean_df['Year_num'] >= 1960) & (clean_df['Year_num'] <= 2023)].copy()
    clean_df['Year'] = clean_df['Year_num'].astype(int)
    clean_df = clean_df.drop(columns=['Year_num'])

    # Standardize Country names using dictionary and Title Case
    clean_df['Country_clean'] = clean_df['Country'].apply(_clean_country_name)

    # Standardize Area names (remove whitespace and trailing punctuation)
    clean_df['Area_clean'] = clean_df['Area'].fillna('Unknown').astype(str).str.strip().str.title()

    # Extract Month (1-12) and derive hemisphere-aware Season
    clean_df['Month'] = clean_df['Date'].apply(_extract_month_from_date)
    clean_df['Season'] = clean_df.apply(lambda r: _derive_season(r['Month'], r['Country_clean']), axis=1)

    # Bucket Activity into normalized categories
    clean_df['Activity_group'] = clean_df['Activity'].apply(_clean_activity)

    # Standardize Fatal indicator to strictly Y, N, or Unknown
    def _clean_fatal(f):
        if pd.isna(f): return "Unknown"
        s = str(f).strip().upper()
        if s.startswith('Y'): return 'Y'
        if s.startswith('N'): return 'N'
        return "Unknown"
    clean_df['Fatal_clean'] = clean_df['Fatal (Y/N)'].apply(_clean_fatal)

    # Standardize Time of day
    clean_df['Time_of_day'] = clean_df['Time'].apply(_clean_time_of_day)

    # Standardize Incident Type
    def _clean_type(t):
        if pd.isna(t): return "Unprovoked"
        s = str(t).strip().capitalize()
        if s in ["Unprovoked", "Provoked", "Boating", "Sea disaster", "Invalid"]:
            return s
        return "Other"
    clean_df['Type_clean'] = clean_df['Type'].apply(_clean_type)

    # Clean Sex (M, F, Unknown)
    def _clean_sex(s):
        if pd.isna(s): return "Unknown"
        val = str(s).strip().upper()
        if val in ['M', 'F']: return val
        return "Unknown"
    clean_df['Sex_clean'] = clean_df['Sex'].apply(_clean_sex) if 'Sex' in clean_df.columns else "Unknown"

    return clean_df


# Function for reshaping tourism data and merging it with annual shark attack counts
# Input: cleaned shark_df (pd.DataFrame), raw tourism_df (pd.DataFrame)
# Output: merged DataFrame on (Country_clean, Year) covering 1995-2020 with annual attacks and arrivals
def clean_and_merge_tourism(shark_df, tourism_df):
    # Melt World Bank tourism dataset from wide year columns to long format
    year_cols = [c for c in tourism_df.columns if c.isdigit()]
    melted = pd.melt(
        tourism_df,
        id_vars=['Country Name', 'Country Code'],
        value_vars=year_cols,
        var_name='Year',
        value_name='Arrivals'
    )

    # Convert Year to integer and filter the overlapping period (1995 to 2020)
    melted['Year'] = pd.to_numeric(melted['Year'], errors='coerce')
    melted = melted.dropna(subset=['Year', 'Arrivals']).copy()
    melted['Year'] = melted['Year'].astype(int)
    melted = melted[(melted['Year'] >= 1995) & (melted['Year'] <= 2020)]

    # Align country names
    melted['Country_clean'] = melted['Country Name'].apply(_clean_country_name)

    # Aggregate annual shark attacks and fatal attacks by Country_clean and Year
    shark_period = shark_df[(shark_df['Year'] >= 1995) & (shark_df['Year'] <= 2020)].copy()
    annual_shark = shark_period.groupby(['Country_clean', 'Year']).agg(
        annual_attacks=('Country_clean', 'count'),
        fatal_attacks=('Fatal_clean', lambda s: (s == 'Y').sum())
    ).reset_index()

    # Inner join on Country_clean and Year
    merged = pd.merge(
        melted,
        annual_shark,
        on=['Country_clean', 'Year'],
        how='inner'
    )

    # Sort chronologically by country
    merged = merged.sort_values(by=['Country_clean', 'Year']).reset_index(drop=True)
    return merged

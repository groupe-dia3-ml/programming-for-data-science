# Module for loading, exploring, cleaning, and merging the project datasets
# Primary dataset: Global Shark Attack (GSAF - Kaggle mexwell)
# Bonus dataset: International tourism, number of arrivals (World Bank ST.INT.ARVL)

import os
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


# Function for loading the primary Global Shark Attack dataset (CSV or Excel)
# Input: file_path (str) - path to attacks.csv or GSAF5.xls inside projet/data/
# Output: raw pandas DataFrame of shark attacks
def load_shark_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Shark dataset not found at '{file_path}'. See doc/DATA_SETUP.md."
        )

    # TODO (Maxime): handle both .csv (with encoding='latin-1') and .xls/.xlsx files
    # Hint: check file_path.lower().endswith(('.xls', '.xlsx')) and use pd.read_excel()
    # Otherwise use pd.read_csv(file_path, encoding='latin-1')
    # Strip extra spaces from column names with df.columns = df.columns.str.strip()
    raise NotImplementedError("TODO: implement load_shark_data()")


# Function for loading the external World Bank tourism dataset (ST.INT.ARVL)
# Input: file_path (str) - path to tourism_arrivals.csv inside projet/data/
# Output: raw pandas DataFrame of international tourist arrivals
def load_tourism_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Tourism dataset not found at '{file_path}'. See doc/DATA_SETUP.md."
        )

    # TODO (Maxime): read World Bank CSV using pd.read_csv(file_path, skiprows=4)
    # Remove any unnamed trailing empty column if present
    raise NotImplementedError("TODO: implement load_tourism_data()")


# Function for profiling and summarizing any dataset (mandatory EDA step)
# Input: df (pd.DataFrame), dataset_name (str)
# Output: dictionary with shape, dtypes, missing values, and value ranges
def summarize_dataset(df, dataset_name="Dataset"):
    # TODO (Maxime): compute and print:
    # 1. Number of rows and columns (df.shape)
    # 2. Column names and data types (df.dtypes)
    # 3. Missing values count and percentage per column (df.isna().sum())
    # 4. Min and max range for numeric columns + unique count for categorical columns
    raise NotImplementedError("TODO: implement summarize_dataset()")


# Function for cleaning and feature engineering the Global Shark Attack dataset
# Input: raw shark attacks DataFrame
# Output: cleaned DataFrame with Year, Month, Season, Country_clean, Activity_group, Time_of_day, Fatal_clean
def clean_shark_data(df):
    # TODO (Maxime):
    # 1. Drop empty/metadata columns (href, href formula, pdf, Case Number.1, original order, Unnamed:*)
    #    and document why each column was dropped in Markdown
    # 2. Convert Year to numeric and filter reliable modern records (Year >= 1960)
    # 3. Extract Month (1-12) from Date and derive hemisphere-aware Season
    # 4. Standardize Country into Country_clean using COUNTRY_MAPPING + title case
    # 5. Group raw Activity text into clean categories (Surfing, Swimming, Diving/Snorkeling, Fishing, Wading, Other)
    # 6. Standardize Fatal (Y/N) into Fatal_clean ('Y', 'N', 'Unknown') and bucket Time into Time_of_day
    raise NotImplementedError("TODO: implement clean_shark_data()")


# Function for reshaping tourism data and merging it with annual shark attack counts
# Input: cleaned shark_df (pd.DataFrame), raw tourism_df (pd.DataFrame)
# Output: merged DataFrame on (Country_clean, Year) covering 1995-2020 with annual attacks and arrivals
def clean_and_merge_tourism(shark_df, tourism_df):
    # TODO (Maxime / Romain):
    # 1. Reshape tourism_df from wide year columns to long format using pd.melt()
    #    -> columns: Country_clean, Country Code, Year, Arrivals
    # 2. Convert Year to int and drop missing Arrivals rows
    # 3. Aggregate shark_df by (Country_clean, Year) to get annual_attacks and fatal_attacks
    # 4. Inner join both tables on ['Country_clean', 'Year']
    raise NotImplementedError("TODO: implement clean_and_merge_tourism()")

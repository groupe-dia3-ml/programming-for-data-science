# Module for loading, exploring, cleaning, and merging the project datasets
# Primary dataset: Global Shark Attack (GSAF - Kaggle / sharkattackfile.net)
# Bonus dataset: International tourism, number of arrivals (World Bank ST.INT.ARVL)

import io
import os
import re
import zipfile
from pathlib import Path
import requests
import pandas as pd
import numpy as np


# Official / public direct download URLs for cross-platform automatic fallback (Windows, macOS, Linux)
SHARK_FALLBACK_URL = "https://raw.githubusercontent.com/SmilodonCub/DATA607/master/attacks.csv"
TOURISM_FALLBACK_URL = "https://api.worldbank.org/v2/en/indicator/ST.INT.ARVL?downloadformat=csv"


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
    "REUNION": "Reunion",
    "BERMUDA": "Bermuda",
    "NEW CALEDONIA": "New Caledonia",
    "PAPUA NEW GUINEA": "Papua New Guinea",
    "FIJI": "Fiji",
    "FRENCH POLYNESIA": "French Polynesia",
}


# Function for finding a dataset file across standard local folders (Windows/macOS/Linux safe)
# Input: file_path (str or Path) - requested path to the dataset file
# Output: Path object pointing to an existing local file, or None if not found locally
def find_local_data_file(file_path):
    requested = Path(file_path)
    filename = requested.name
    candidates = [
        requested,
        Path("..") / "projet" / "data" / filename,
        Path("..") / "data" / filename,
        Path("projet") / "data" / filename,
        Path("data") / filename,
        Path(filename),
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


# Function for loading the primary Global Shark Attack dataset (local first, auto-download fallback)
# Input: file_path (str or Path) - path to attacks.csv or GSAF5.xls
# Output: raw pandas DataFrame of shark attacks
def load_shark_data(file_path):
    local_file = find_local_data_file(file_path)

    if local_file is None:
        # Cross-platform fallback: download directly into local ./data/ folder (no Kaggle account needed)
        target = Path("data") / "attacks.csv"
        target.parent.mkdir(parents=True, exist_ok=True)
        print(f"Local shark dataset not found. Downloading automatically to {target} ...")
        response = requests.get(SHARK_FALLBACK_URL, timeout=30)
        response.raise_for_status()
        target.write_bytes(response.content)
        local_file = target
        print(f"Downloaded shark dataset successfully ({local_file.stat().st_size:,} bytes).")

    # Detect file format automatically so both CSV and Excel exports work on any OS
    if local_file.suffix.lower() in (".xls", ".xlsx"):
        df = pd.read_excel(local_file)
    else:
        # Standard GSAF CSV uses latin-1 encoding due to accented place names
        df = pd.read_csv(local_file, encoding="latin-1", low_memory=False)

    # Strip trailing spaces from column names (e.g. 'Sex ' -> 'Sex', 'Species ' -> 'Species')
    df.columns = df.columns.str.strip()
    return df


# Function for loading the external World Bank tourism dataset (local first, auto-download fallback)
# Input: file_path (str or Path) - path to tourism_arrivals.csv
# Output: raw pandas DataFrame of international tourist arrivals
def load_tourism_data(file_path):
    local_file = find_local_data_file(file_path)

    if local_file is None:
        # Cross-platform fallback: download and extract official World Bank ST.INT.ARVL CSV ZIP in memory
        target = Path("data") / "tourism_arrivals.csv"
        target.parent.mkdir(parents=True, exist_ok=True)
        print(f"Local tourism dataset not found. Downloading World Bank ST.INT.ARVL to {target} ...")
        response = requests.get(TOURISM_FALLBACK_URL, timeout=30)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            csv_members = [name for name in zf.namelist() if name.startswith("API_ST.INT.ARVL")]
            if not csv_members:
                raise RuntimeError("Could not locate API_ST.INT.ARVL CSV inside World Bank ZIP archive.")
            target.write_bytes(zf.read(csv_members[0]))
        local_file = target
        print(f"Downloaded World Bank tourism dataset successfully ({local_file.stat().st_size:,} bytes).")

    # World Bank CSV downloads start with 4 metadata lines before the header
    df = pd.read_csv(local_file, skiprows=4)
    df.columns = df.columns.str.strip()
    # Remove any completely empty trailing column
    df = df.dropna(how="all", axis=1)
    return df


# Function for profiling and summarizing any dataset (mandatory EDA step)
# Input: df (pd.DataFrame), dataset_name (str)
# Output: dictionary with shape, dtypes, missing values, numeric ranges, and categorical counts
def summarize_dataset(df, dataset_name="Dataset"):
    summary = {
        "dataset_name": dataset_name,
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_counts": df.isna().sum().to_dict(),
        "missing_pct": (df.isna().mean() * 100).round(2).to_dict(),
        "numeric_ranges": {},
        "categorical_unique": {},
    }

    # Compute min, max, mean, and median for numeric columns
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        series = df[col].dropna()
        if len(series) > 0:
            summary["numeric_ranges"][col] = {
                "min": float(series.min()),
                "max": float(series.max()),
                "mean": round(float(series.mean()), 2),
                "median": round(float(series.median()), 2),
            }

    # Compute cardinality (unique values) for categorical columns
    cat_cols = df.select_dtypes(exclude=[np.number]).columns
    for col in cat_cols:
        summary["categorical_unique"][col] = int(df[col].nunique(dropna=True))

    return summary


# Function for grouping noisy free-text Activity descriptions into clean categories
# Input: act (str or NaN) - raw activity text from GSAF
# Output: standardized activity category string
def categorize_activity(act):
    if not isinstance(act, str) or pd.isna(act):
        return "Other"
    act_lower = act.lower()
    if any(k in act_lower for k in ["surf", "bodyboard", "paddleboard", "boogie", "kite"]):
        return "Surfing"
    if "snork" in act_lower or any(k in act_lower for k in ["div", "spear"]):
        return "Diving/Snorkeling"
    if any(k in act_lower for k in ["swim", "bath", "float"]):
        return "Swimming"
    if "fish" in act_lower:
        return "Fishing"
    if any(k in act_lower for k in ["wading", "standing", "treading", "walking"]):
        return "Wading"
    if any(k in act_lower for k in ["boat", "kayak", "canoe", "rowing", "sailing", "ski"]):
        return "Boating/Kayaking"
    return "Other"


# Function for extracting major shark species groups from raw Species text
# Input: species_val (str or NaN) - raw shark species description
# Output: standardized shark species group string
def categorize_species(species_val):
    if not isinstance(species_val, str) or pd.isna(species_val):
        return "Unidentified"
    s = species_val.lower().strip()
    if s == "" or any(k in s for k in ["unconfirmed", "not confirmed", "questionable", "invalid", "unidentified"]):
        return "Unidentified"
    if "white" in s:
        return "White Shark"
    if "tiger" in s:
        return "Tiger Shark"
    if "bull" in s or "zambezi" in s:
        return "Bull Shark"
    if "blacktip" in s or "spinner" in s:
        return "Blacktip/Spinner Shark"
    if "reef" in s or "nurse" in s or "lemon" in s or "wobbegong" in s:
        return "Reef/Nurse Shark"
    if "hammerhead" in s or "mako" in s or "bronze" in s or "whaler" in s or "raggedtooth" in s or "blue" in s:
        return "Hammerhead/Mako/Whaler"
    if "shark" in s:
        return "Other Named Shark"
    return "Unidentified"


# Function for extracting month number (1-12) from unstructured Date strings
# Input: date_val (str or NaN) - raw GSAF Date string
# Output: integer month (1 to 12) or np.nan if missing
def parse_month(date_val):
    if not isinstance(date_val, str) or pd.isna(date_val):
        return np.nan
    months = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }
    date_lower = date_val.lower()
    for m_str, m_num in months.items():
        if m_str in date_lower:
            return m_num
    return np.nan


# Function for assigning hemisphere-aware Season from Month and Country
# Input: month (float/int), country (str)
# Output: Season string ('Summer', 'Autumn', 'Winter', 'Spring', or 'Unknown')
def assign_season(month, country):
    if pd.isna(month):
        return "Unknown"
    month = int(month)
    southern_countries = {
        "Australia", "South Africa", "New Zealand", "Brazil", "Chile",
        "Argentina", "Uruguay", "Reunion", "Fiji", "New Caledonia",
        "Papua New Guinea", "French Polynesia", "Mozambique",
    }
    is_south = country in southern_countries

    if month in (12, 1, 2):
        return "Summer" if is_south else "Winter"
    if month in (3, 4, 5):
        return "Autumn" if is_south else "Spring"
    if month in (6, 7, 8):
        return "Winter" if is_south else "Summer"
    if month in (9, 10, 11):
        return "Spring" if is_south else "Autumn"
    return "Unknown"


# Function for bucketing raw incident Time text into Time_of_day periods
# Input: t_val (str or NaN) - raw time string (e.g. '14h30', 'Afternoon')
# Output: period label ('Morning (06-12)', 'Afternoon (12-18)', 'Evening/Night (18-06)', 'Unknown')
def categorize_time(t_val):
    if not isinstance(t_val, str) or pd.isna(t_val):
        return "Unknown"
    t_val = t_val.lower().strip()
    if any(k in t_val for k in ["afternoon", "midday", "noon"]):
        return "Afternoon (12-18)"
    if "morning" in t_val:
        return "Morning (06-12)"
    if any(k in t_val for k in ["night", "evening", "dusk", "sunset"]):
        return "Evening/Night (18-06)"

    # Parse numeric hour formats such as 14h00, 14:30, or 1400
    match = re.search(r"(\d{1,2})[h:]?(\d{2})?", t_val)
    if match:
        hour = int(match.group(1))
        if 6 <= hour < 12:
            return "Morning (06-12)"
        if 12 <= hour < 18:
            return "Afternoon (12-18)"
        if (18 <= hour <= 24) or (0 <= hour < 6):
            return "Evening/Night (18-06)"
    return "Unknown"


# Function for standardizing raw Fatal (Y/N) entries into Y, N, or Unknown
# Input: f_val (str or NaN) - raw fatality indicator
# Output: 'Y', 'N', or 'Unknown'
def clean_fatality(f_val):
    if not isinstance(f_val, str) or pd.isna(f_val):
        return "Unknown"
    f_clean = f_val.strip().upper()
    if f_clean in ("Y", "FATAL"):
        return "Y"
    if f_clean in ("N", "NOT FATAL"):
        return "N"
    return "Unknown"


# Function for cleaning and feature engineering the Global Shark Attack dataset
# Input: df (pd.DataFrame) - raw shark attacks DataFrame
# Output: cleaned DataFrame with Year, Month, Season, Country_clean, Area_clean, Activity_group, Species_group, Time_of_day, Fatal_clean
def clean_shark_data(df):
    # 1. Remove trailing completely empty rows present in GSAF CSV exports
    cleaned = df.dropna(how="all").copy()
    if "Case Number" in cleaned.columns:
        cleaned = cleaned[
            cleaned["Case Number"].notna()
            & (cleaned["Case Number"].astype(str).str.strip() != "")
            & (cleaned["Case Number"].astype(str).str.strip() != "0")
        ].copy()

    # 2. Drop administrative / duplicate export columns that carry no analytical value
    cols_to_drop = [
        "href", "href formula", "pdf", "Case Number.1", "Case Number.2",
        "original order", "Unnamed: 22", "Unnamed: 23", "Investigator or Source",
    ]
    cleaned = cleaned.drop(columns=[c for c in cols_to_drop if c in cleaned.columns])

    # 3. Filter reliable modern reporting window (1960 - 2023)
    cleaned["Year"] = pd.to_numeric(cleaned["Year"], errors="coerce")
    cleaned = cleaned[
        cleaned["Year"].notna() & (cleaned["Year"] >= 1960) & (cleaned["Year"] <= 2023)
    ].copy()
    cleaned["Year"] = cleaned["Year"].astype(int)

    # 4. Normalize Country names to match World Bank naming conventions
    raw_country = cleaned["Country"].astype(str).str.strip().str.rstrip("?").str.strip().str.upper()
    cleaned["Country_clean"] = raw_country.map(COUNTRY_MAPPING)
    cleaned["Country_clean"] = cleaned["Country_clean"].fillna(raw_country.str.title())
    cleaned["Country_clean"] = cleaned["Country_clean"].replace({"Nan": "Unknown", "": "Unknown"})

    # 5. Clean Area and Location text
    cleaned["Area_clean"] = (
        cleaned["Area"].astype(str).str.strip().str.title().replace({"Nan": "Unknown", "": "Unknown"})
    )
    cleaned["Location_clean"] = (
        cleaned["Location"].astype(str).str.strip().replace({"Nan": "Unknown", "": "Unknown"})
    )

    # 6. Extract Month and hemisphere-aware Season
    cleaned["Month"] = cleaned["Date"].apply(parse_month)
    cleaned["Season"] = cleaned.apply(lambda r: assign_season(r["Month"], r["Country_clean"]), axis=1)

    # 7. Categorize Activity, Species, Fatality, Time_of_day, Sex, Age, and Type
    cleaned["Activity_group"] = cleaned["Activity"].apply(categorize_activity)
    cleaned["Species_group"] = (
        cleaned["Species"].apply(categorize_species) if "Species" in cleaned.columns else "Unidentified"
    )
    cleaned["Fatal_clean"] = (
        cleaned["Fatal (Y/N)"].apply(clean_fatality) if "Fatal (Y/N)" in cleaned.columns else "Unknown"
    )
    cleaned["Time_of_day"] = (
        cleaned["Time"].apply(categorize_time) if "Time" in cleaned.columns else "Unknown"
    )
    if "Sex" in cleaned.columns:
        cleaned["Sex_clean"] = (
            cleaned["Sex"].astype(str).str.strip().str.upper().apply(lambda x: x if x in ("M", "F") else "Unknown")
        )
    else:
        cleaned["Sex_clean"] = "Unknown"
    cleaned["Age_clean"] = pd.to_numeric(cleaned["Age"], errors="coerce") if "Age" in cleaned.columns else np.nan
    cleaned["Type"] = cleaned["Type"].fillna("Unprovoked").astype(str).str.strip().str.title()

    return cleaned.reset_index(drop=True)


# Function for reshaping tourism data and merging it with annual shark attack counts
# Input: shark_df (pd.DataFrame) cleaned shark data, tourism_df (pd.DataFrame) raw World Bank data
# Output: merged DataFrame on (Country_clean, Year) covering 1995-2020 with annual attacks and arrivals
def clean_and_merge_tourism(shark_df, tourism_df):
    id_vars = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
    year_cols = [c for c in tourism_df.columns if c.isdigit()]

    # Reshape World Bank wide table into tidy long format
    tourism_long = pd.melt(
        tourism_df,
        id_vars=id_vars,
        value_vars=year_cols,
        var_name="Year",
        value_name="Arrivals",
    )
    tourism_long["Year"] = pd.to_numeric(tourism_long["Year"], errors="coerce")
    tourism_long["Arrivals"] = pd.to_numeric(tourism_long["Arrivals"], errors="coerce")
    tourism_long = tourism_long.dropna(subset=["Arrivals", "Year"]).copy()
    tourism_long["Year"] = tourism_long["Year"].astype(int)
    tourism_long = tourism_long[(tourism_long["Year"] >= 1995) & (tourism_long["Year"] <= 2020)].copy()
    tourism_long["Country_clean"] = tourism_long["Country Name"].astype(str).str.strip()

    # Aggregate shark attacks per Country and Year
    shark_agg = shark_df.groupby(["Country_clean", "Year"]).agg(
        annual_attacks=("Case Number", "count"),
        fatal_attacks=("Fatal_clean", lambda s: (s == "Y").sum()),
    ).reset_index()

    # Inner join on harmonized Country_clean and Year
    merged = pd.merge(
        tourism_long[["Country_clean", "Country Code", "Year", "Arrivals"]],
        shark_agg,
        on=["Country_clean", "Year"],
        how="inner",
    )
    return merged.sort_values(by=["Country_clean", "Year"]).reset_index(drop=True)

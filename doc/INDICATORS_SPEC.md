# Analytical Indicators & Dashboard Technical Specification

This document defines every data cleaning step, analytical indicator, visualization, and Markdown explanation required to fulfill `Final_project.pdf`.

---

## 1. EDA & Preprocessing (`01_eda_and_cleaning.ipynb` / `src/data_loader.py`)

### Mandatory EDA Outputs `[2 pts]`
For both datasets (`attacks.csv` and `tourism_arrivals.csv`), `summarize_dataset()` must output:
- Dataset dimensions (`n_rows`, `n_cols`).
- Exact column names and `dtypes`.
- Number and percentage of missing values per column.
- Numeric ranges (`min`, `max`, median) and number of unique values for categorical columns.

### Cleaning & Feature Engineering Rules
Every dropped column or filter must be justified in a Markdown cell:
1. **Dropped metadata columns:** `href`, `href formula`, `pdf`, `Case Number.1`, `Case Number.2`, `original order`, `Unnamed: *` (administrative/export artifacts not needed for KDD).
2. **Temporal filter:** Keep modern reliable records (`Year >= 1960` and `Year <= 2023`) for time-series and pattern mining; extract `Month` (1-12) and `Season` (`Summer`, `Autumn`, `Winter`, `Spring`) accounting for Northern vs. Southern hemisphere.
3. **Activity grouping:** Normalize noisy free-text `Activity` strings into clean buckets: `Surfing`, `Swimming`, `Diving/Snorkeling`, `Fishing`, `Wading`, `Boating/Kayaking`, `Other`.
4. **Fatality cleaning:** Standardize `Fatal (Y/N)` to strictly `Y`, `N`, or `Unknown`.
5. **Time-of-day bucketing:** Map raw `Time` strings into `Morning (06-12)`, `Afternoon (12-18)`, `Evening/Night (18-06)`, `Unknown`.
6. **Country normalization (critical for World Bank merge):** Strip whitespace, remove trailing `?`, and apply an explicit mapping dictionary:
   - `USA` -> `United States`
   - `ENGLAND` / `SCOTLAND` / `WALES` / `UNITED KINGDOM` -> `United Kingdom`
   - `BAHAMAS` -> `Bahamas, The`
   - `EGYPT` -> `Egypt, Arab Rep.`
   - `RUSSIA` -> `Russian Federation`
   - `SOUTH KOREA` -> `Korea, Rep.`
   - `IRAN` -> `Iran, Islamic Rep.`
   - `VENEZUELA` -> `Venezuela, RB`
   - `HONG KONG` -> `Hong Kong SAR, China`
   - Standard title case for matching names (`AUSTRALIA` -> `Australia`, `SOUTH AFRICA` -> `South Africa`, `BRAZIL` -> `Brazil`, `MEXICO` -> `Mexico`, `FRANCE` -> `France`, `NEW ZEALAND` -> `New Zealand`).

---

## 2. The Four Analytical Queries `[7 pts]`

> [!IMPORTANT]
> Every indicator below **must** have its own Markdown cell explaining: (1) how it is calculated, (2) what it represents, and (3) how to interpret it. Missing an explanation incurs a **-2 points penalty**.

### Query 1 — Grouping & Aggregation `[1 pt]`
- **Owner:** Baptiste Noailhac (`02_grouping_and_apriori.ipynb`)
- **Calculations:**
  - Total attack counts and share (%) for the **Top 10 Countries**.
  - Attack count and **Fatality Rate (`Fatal %`)** by `Activity_group`.
  - Top shark `Species` (cleaned: Great White, Tiger, Bull, Blacktip, Reef, Nurse, Unidentified) vs. fatality rate.
- **Visualizations:** Plotly horizontal bar chart (Top 10 Countries) and grouped/colored bar chart (Attacks & Fatality Rate by Activity).

### Query 2 — Frequent Pattern Mining (`Apriori`) `[2 pts]`
- **Owner:** Baptiste Noailhac (`02_grouping_and_apriori.ipynb`)
- **Course reference:** Lab 9 (`mlxtend.frequent_patterns.apriori` & `association_rules`).
- **Calculations:**
  - Build a boolean one-hot transaction table from discretized attributes (`Country_top`, `Activity_group`, `Type`, `Season`, `Time_of_day`, `Fatal`).
  - Run a support sensitivity sweep (e.g. `min_support` from `0.03` to `0.30`) and plot the number of frequent itemsets found.
  - Extract association rules with `metric="lift"` (`min_threshold >= 1.05`) and sort by `lift` and `confidence`.
- **Visualizations:** Support sensitivity curve + Plotly scatter plot (`support` vs. `confidence`, colored by `lift`, with rule labels on hover).

### Query 3 — Temporal Dynamics & Forecasting (`Prophet`) `[2 pts]`
- **Owner:** Romain Thepaut (`03_temporal_forecasting.ipynb`)
- **Course reference:** Lab 7 (`prophet.Prophet`, `plot_plotly`, `plot_components_plotly`).
- **Calculations:**
  - Aggregate monthly/annual shark attack counts from 1960 to the last complete year (`ds`, `y`).
  - Compare monthly seasonality profiles between **Northern Hemisphere** (e.g. USA — peak in July/August) and **Southern Hemisphere** (e.g. Australia / South Africa — peak in December/January/February).
  - Fit `Prophet(interval_width=0.95)` and forecast the next **5 years** (`yhat`, `yhat_lower`, `yhat_upper`).
- **Visualizations:** Hemisphere seasonality comparison plot + Prophet interactive forecast plot with uncertainty intervals and trend changepoints.

### Query 4 — Spatial Analysis & Hotspot Clustering (`GeoPandas` + `OPTICS` / `K-Means`) `[2 pts]`
- **Owner:** Louis Le Forestier (`04_spatial_clustering.ipynb`)
- **Course reference:** Lab 8 (`geopandas`, `shapely.geometry.Point`, `sjoin`, `sklearn.cluster.OPTICS`, `KMeans`).
- **Calculations:**
  - Geocode unique `(Area, Country)` coastal zones into `projet/data/locations_geocoded.csv`.
  - Build a `GeoDataFrame` (`EPSG:4326`) and perform spatial join with `ne_110m_admin_0_countries.shp`.
  - Apply **K-Means** (`n_clusters=6`, `random_state=42`) and **OPTICS** on `[['latitude', 'longitude']]` to detect major global coastal hotspots (US East Coast / Florida, Hawaii, East Australia, West Australia, South Africa, Brazil/Caribbean).
  - Summarize each cluster (attack count, dominant activity, fatality rate).
- **Visualizations:** Interactive Plotly `scatter_geo` world map colored by spatial cluster with hover details.

---

## 3. External Dataset Bonus — Tourism Risk Correlation `[+1 pt]`

- **Owner:** Romain Thepaut (`05_tourism_bonus.ipynb`)
- **Join:** Inner join on `(Country_clean, Year)` across **1995-2020** (26 overlapping years).
- **Calculations:**
  - Tourism-normalized risk indicator:
    `attacks_per_1M_tourists = (annual_attacks / annual_arrivals) * 1_000_000`
  - Global and per-country **Pearson** and **Spearman** correlation between annual tourist arrivals and annual shark attacks.
  - Comparative ranking of top affected coastal countries: **Raw Attack Count** vs. **Attacks per 1 Million Tourists** (distinguishing sheer volume from relative risk).
- **Visualizations:** Dual-axis time-series chart (attacks vs. tourist arrivals) + side-by-side ranking bar chart.

---

## 4. Interactive Dash Dashboard `[2 pts]`

- **Owner:** Louis Le Forestier (`projet/src/dashboard.py`)
- **Mandatory Header Elements:**
  - Project title and both dataset titles (`Global Shark Attack (GSAF)` + `World Bank International Tourism (ST.INT.ARVL)`).
  - Full names of all 4 team members (`Maxime Laurent`, `Louis Le Forestier`, `Baptiste Noailhac`, `Romain Thepaut`).
- **Layout:** 5 clean tabs (`dcc.Tabs`) matching the 4 queries + Tourism Bonus, with interactive filters (year slider, country selector, activity filter).
- **Static Proof Export:** `export_dashboard_html()` saves `rendu/Laurent_dashboard.html` so the instructor has offline proof of all charts (`-2 pts` penalty protection).

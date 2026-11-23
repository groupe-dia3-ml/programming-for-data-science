# Programming for Data Science — Global Shark Attacks & International Tourism Analysis

<p align="center">
  <img src="https://img.shields.io/badge/ESILV-A4%20DIA3%20(2026--2027)-0F172A?style=flat-square" alt="ESILV A4 DIA3">
  <img src="https://img.shields.io/badge/Python-3.10+-1E293B?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Dashboard-Plotly%20Dash-0F766E?style=flat-square&logo=plotly&logoColor=white" alt="Plotly Dash">
  <img src="https://img.shields.io/badge/Primary%20Data-Global%20Shark%20Attack%20(GSAF)-0284C7?style=flat-square" alt="GSAF Dataset">
  <img src="https://img.shields.io/badge/Bonus%20Data-World%20Bank%20ST.INT.ARVL-334155?style=flat-square" alt="World Bank Tourism">
</p>

---

## 📌 Executive Overview

Final project deliverable for the **Programming for Data Science** course taught by **Hugo Alatrista-Salas** at **ESILV (École Supérieure d'Ingénieurs Léonard de Vinci — A4 DIA3)**.

The objective is to implement the end-to-end **Knowledge Discovery in Databases (KDD)** process on a real-world **multidimensional dataset** (satisfying the **Temporal**, **Spatial**, and **Analytical** axes), contextualize it with an external macroeconomic dataset (`+1 bonus point`), and visualize all derived intelligence inside an interactive **Python Dash** prototype.

### 🎯 Core Problem Statement
*How are global shark attack incidents distributed across time, seasons, recreational activities, and coastal hotspots, and does the historical growth in reported attacks reflect increased biological danger or simply the expansion of international coastal tourism?*

---

## 👥 Team & Ownership

| Member | Role | GitHub | Contact | Primary Domain |
| :--- | :--- | :--- | :--- | :--- |
| **Maxime LAURENT** | Team Leader | [@maximelrnt](https://github.com/maximelrnt) | `maxime.laurent@edu.devinci.fr` | EDA, Data Ingestion, Cleaning Contract, Master Rendu Notebook & Slides |
| **Baptiste NOAILHAC** | Core Contributor | [@BaptisteNoai](https://github.com/BaptisteNoai) | `baptiste.noailhac@edu.devinci.fr` | Query 1 (Grouping & Fatality Rates) & Query 2 (Apriori Pattern Mining) |
| **Romain THEPAUT** | Core Contributor | [@RomThpt](https://github.com/RomThpt) | `romain.thepaut@edu.devinci.fr` | Query 3 (Temporal & Prophet Forecasting) & External Tourism Bonus Query |
| **Louis LE FORESTIER** | Core Contributor | [@louislefo](https://github.com/louislefo) | `louis.le_forestier@edu.devinci.fr` | Query 4 (Spatial Clustering GeoPandas/OPTICS) & Interactive Dash Dashboard |

---

## 🗂️ Datasets Overview

> [!NOTE]
> Datasets are stored **locally** inside `projet/data/` and excluded from Git via `.gitignore`. See [`doc/DATA_SETUP.md`](doc/DATA_SETUP.md) for details.

1. **Primary Multidimensional Dataset:** [Global Shark Attack File (GSAF — Kaggle mexwell)](https://www.kaggle.com/datasets/mexwell/global-shark-attack)
   - **Temporal Axis (*When*):** `Date`, `Year`, `Month`, `Season`, and `Time_of_day` (filtered to the modern era 1960–2023).
   - **Spatial Axis (*Where*):** `Country`, `Area` (state/province), and coastal `Location` mapped to `(latitude, longitude)`.
   - **Analytical Axis (*What*):** `Type` (Unprovoked, Provoked), `Activity_group` (Surfing, Swimming, Diving...), `Sex`, `Age`, and `Fatal_clean` (`Y`, `N`).
2. **External Macroeconomic Bonus Dataset (+1 pt):** [World Bank International Tourism Arrivals (`ST.INT.ARVL`)](https://data.worldbank.org/indicator/ST.INT.ARVL)
   - Panel dataset of international tourist arrivals across 266 nations over 1995–2020, merged by `(Country_clean, Year)`.
3. **Geospatial Reference Shapefile:** Natural Earth 110m Admin-0 Countries (`ne_110m_admin_0_countries.*`).

---

## 🗺️ Project Roadmap & 4-Part Work Breakdown

To ensure seamless parallel collaboration without Git merge conflicts, the project is structured into **four independent modules**, with each member owning their designated branch, notebook, and functions:

```text
                                  ┌── Part 1 (Maxime): EDA & Cleaning Contract (src/data_loader.py)
                                  │
[Raw Datasets in projet/data/] ───┼── Part 2 (Baptiste): Grouping & Apriori Mining (Q1 & Q2)
                                  │
                                  ├── Part 3 (Romain): Prophet Seasonality & Tourism Bonus (Q3 & Bonus)
                                  │
                                  └── Part 4 (Louis): Spatial Clustering & Dash Prototype (Q4 & Dashboard)
                                  │
                                  ▼
             [Final Consolidation: rendu/Laurent_notebook.ipynb & slides]
```

### 👤 Part 1: Data Exploration, Cleaning Contract & Master Assembly
* **Assigned to:** **Maxime LAURENT** (`@maximelrnt`)
* **Branch:** `feature/eda-cleaning`
* **Assigned Files:**
  - `projet/notebooks/01_eda_and_cleaning_todo.ipynb`
  - `projet/src/data_loader.py`
  - Coordination of `rendu/Laurent_notebook.ipynb` and `rendu/Laurent_slides.pdf`
* **Key Missions & Deliverables:**
  1. **Task 1 — EDA Profiling [2 pts]:** Implement `summarize_dataset()` outputting row/column counts, dtypes, missing values counts/percentages, and numeric ranges.
  2. **Data Cleaning & Standardization:**
     - Justify in Markdown every dropped column (`href`, `pdf`, `Case Number.1`, `Unnamed:*`).
     - Filter reliable modern records (`Year >= 1960` & `Year <= 2023`).
     - Derive `Month` (1–12) and hemisphere-aware `Season` (`Summer`, `Autumn`, `Winter`, `Spring`).
     - Map free-text `Activity` into 6 clean categories (`Surfing`, `Swimming`, `Diving`, `Fishing`, `Wading`, `Other`).
     - Normalize country names (`COUNTRY_MAPPING`) to match World Bank standards.
  3. **Panel Merge:** Reshape World Bank tourism data (`pd.melt`) and inner join on `(Country_clean, Year)` for 1995–2020.
  4. **Master Consolidation:** Assemble team contributions into `rendu/Laurent_notebook.ipynb` and coordinate the 5-minute defense presentation deck.

---

### 👤 Part 2: Descriptive Grouping & Apriori Pattern Mining
* **Assigned to:** **Baptiste NOAILHAC** (`@BaptisteNoai`)
* **Branch:** `feature/grouping-apriori`
* **Assigned Files:**
  - `projet/notebooks/02_grouping_and_apriori_todo.ipynb`
  - Functions in `projet/src/indicators.py`: `query_grouping_analysis()`, `query_frequent_patterns()`
* **Key Missions & Deliverables:**
  1. **Query 1 — Grouping & Aggregation [1 pt]:**
     - Group shark attacks by `Country_clean` and compute incident volume and fatality rate: $\text{Fatality Rate (\%)} = \frac{\text{Fatal Attacks}}{\text{Total Attacks}} \times 100$.
     - Group by `Activity_group` to contrast high-volume activities (Surfing) vs high-mortality activities (Diving/Swimming).
     - Build interactive Plotly horizontal bar charts and grouped activity comparisons.
     - Add a human-readable Markdown cell explaining calculations, meaning, and interpretation.
  2. **Query 2 — Frequent Pattern Mining (`Apriori`) [2 pts]:**
     - One-hot encode discrete behavioral features (`Country_clean`, `Activity_group`, `Type_clean`, `Season`, `Time_of_day`, `Fatal_clean`).
     - Run `mlxtend.frequent_patterns.apriori` at $\sigma = 0.04$ with support sensitivity curve.
     - Extract association rules (`association_rules`) filtered by $\text{Lift} \ge 1.05$.
     - Produce an interactive Plotly scatter plot (Support vs Confidence colored by Lift).
     - Add a human-readable Markdown cell detailing the rule metrics and interpretation.

---

### 👤 Part 3: Temporal Dynamics, Prophet Forecasting & Tourism Bonus
* **Assigned to:** **Romain THEPAUT** (`@RomThpt`)
* **Branch:** `feature/temporal-tourism`
* **Assigned Files:**
  - `projet/notebooks/03_temporal_forecasting_todo.ipynb`
  - `projet/notebooks/05_tourism_bonus_todo.ipynb`
  - Functions in `projet/src/indicators.py`: `query_temporal_forecast()`, `query_tourism_enrichment()`
* **Key Missions & Deliverables:**
  1. **Query 3 — Temporal Analysis & Forecasting [2 pts]:**
     - Compare monthly seasonality between Northern Hemisphere (USA, Bahamas — peak in July/August) and Southern Hemisphere (Australia, South Africa — peak in Dec/Jan/Feb).
     - Fit Facebook `Prophet(interval_width=0.95)` on the annual series from 1960 to 2023.
     - Forecast the next 5 years ($\hat{y}$) with 95% Bayesian confidence intervals $[\hat{y}_{lower}, \hat{y}_{upper}]$.
     - Plot interactive seasonality bars and Prophet trend forecast in Plotly.
     - Add a human-readable Markdown cell explaining the inverted seasonality and long-term stabilization.
  2. **External Dataset Bonus — Tourism Risk Analysis [+1 pt]:**
     - Compute normalized risk: $\text{Attacks per 1M Tourists} = \frac{\text{Annual Attacks}}{\text{Annual Tourist Arrivals}} \times 1,000,000$.
     - Calculate global Pearson ($r$) and Spearman ($\rho$) correlation between tourist volume and incident rates ($r = 0.60, p < 0.001$).
     - Build comparative rankings: Raw Attack Volume vs Attacks per 1M Arrivals.
     - Plot dual-axis time-series trend (global tourism vs shark attacks).
     - Add a human-readable Markdown cell explaining why tourism volume drives reported attacks.

---

### 👤 Part 4: Spatial Hotspot Clustering & Interactive Dash Prototype
* **Assigned to:** **Louis LE FORESTIER** (`@louislefo`)
* **Branch:** `feature/spatial-dashboard`
* **Assigned Files:**
  - `projet/notebooks/04_spatial_clustering_todo.ipynb`
  - Function in `projet/src/indicators.py`: `query_spatial_clustering()`
  - `projet/src/dashboard.py`
  - `rendu/Laurent_dashboard.html`
* **Key Missions & Deliverables:**
  1. **Query 4 — Spatial Analysis & Hotspot Clustering [2 pts]:**
     - Geocode unique coastal regions into `projet/data/locations_geocoded.csv`.
     - Build a `GeoDataFrame` (`EPSG:4326`) and overlay onto `ne_110m_admin_0_countries.shp`.
     - Apply unsupervised **K-Means** ($k=6$) and **OPTICS** clustering on `[latitude, longitude]`.
     - Automatically identify the 6 global epicenters (Florida/US East, California/US West, Hawaii, East Australia, West Australia, South Africa).
     - Build an interactive Plotly `scatter_geo` world map colored by spatial cluster.
     - Add a human-readable Markdown cell explaining coastal cluster distributions.
  2. **Task 3 — Interactive Plotly Dash Prototype [2 pts]:**
     - Build the multi-tab Plotly Dash application in `src/dashboard.py` displaying all 4 queries + Tourism Bonus.
     - Include mandatory header: Project title, both dataset names, and all 4 team members.
     - Implement the static HTML export function `export_dashboard_html()` saving `rendu/Laurent_dashboard.html` to guarantee immunity against the `-2 pts` penalty.

---

## 📊 Evaluation Rubric & Anti-Penalty Matrix

Total: **20 Points + 1 Bonus Point**

| Task | Evaluation Criteria | Points | Responsible Member |
| :--- | :--- | :---: | :--- |
| **1. Data Exploration** | Ingestion, shape, dtypes, missing data, numeric ranges, and human Markdown description. | **2 pts** | **Maxime LAURENT** |
| **2. Information Building** | **Four distinct analytical queries** implemented as documented functions: | **7 pts** | |
| ↳ *Query 1* | Aggregation & Grouping (Attacks & Fatality rate by Country/Activity). | *1 pt* | **Baptiste NOAILHAC** |
| ↳ *Query 2* | Frequent Pattern Mining (`Apriori` + Association Rules with `mlxtend`). | *2 pts* | **Baptiste NOAILHAC** |
| ↳ *Query 3* | Temporal Dynamics & 5-year `Prophet` forecasting. | *2 pts* | **Romain THEPAUT** |
| ↳ *Query 4* | Spatial Hotspot Clustering (`GeoPandas` + `OPTICS` / `K-Means`). | *2 pts* | **Louis LE FORESTIER** |
| **3. Interactive Dashboard** | Python **Dash** web prototype with 5 tabs, team credits, and offline HTML proof. | **2 pts** | **Louis LE FORESTIER** |
| **4. GitHub Repository** | Clean public repository, modular structure, informative documentation. | **1 pt** | **All Members** |
| **5. Presentation & Demo** | 5-minute slide deck (`Laurent_slides.pdf`), live notebook demo, Q&A. | **8 pts** | **All Members** (presenter drawn randomly) |
| **6. External Dataset** | Macroeconomic World Bank Tourism integration & relative risk correlation. | **+1 pt** | **Romain THEPAUT** |

### ⚠️ Critical Penalties to Avoid (from `Final_project.pdf`):
* **-2 points**: Any function lacking `# Input:`, `# Output:`, or descriptive comments.
* **-2 points**: Any indicator missing a human-readable Markdown explanation cell.
* **-2 points**: Non-working Dash dashboard or missing static proof (`rendu/Laurent_dashboard.html`).
* **-8 points**: Any group member absent during the live presentation and Q&A.

---

## 📁 Repository Architecture

```text
programming-for-data-science/
├── .gitignore                              # Excludes local datasets, .venv, and caches
├── README.md                               # Main project presentation & roadmap (this file)
├── REQUIREMENTS.md                         # Detailed environment setup & dependency guide
├── requirements.txt                        # Python dependencies
│
├── doc/                                    # Technical project documentation
│   ├── PROJECT_OVERVIEW.md                 # Academic context, grading rubric, and checklist
│   ├── DATA_SETUP.md                       # Local dataset installation instructions
│   ├── INDICATORS_SPEC.md                  # Methodological specification for all 4 queries + bonus
│   └── TEAM_WORKFLOW.md                    # Git conventions and collaborative rules
│
├── projet/                                 # Collaborative development workspace
│   ├── Final_project.pdf                   # Official subject instructions (Hugo Alatrista-Salas)
│   ├── README.md                           # Development guidelines
│   ├── data/                               # LOCAL ONLY dataset directory (see doc/DATA_SETUP.md)
│   │   ├── attacks.csv                     # Primary GSAF Shark Attacks dataset
│   │   ├── tourism_arrivals.csv            # World Bank International Tourism arrivals
│   │   ├── locations_geocoded.csv          # Cached coastal coordinates
│   │   └── countries_shp/                  # Natural Earth shapefile
│   ├── notebooks/                          # Development notebooks with structured TODOs
│   │   ├── 01_eda_and_cleaning_todo.ipynb  # (Maxime)
│   │   ├── 02_grouping_and_apriori_todo.ipynb # (Baptiste)
│   │   ├── 03_temporal_forecasting_todo.ipynb # (Romain)
│   │   ├── 04_spatial_clustering_todo.ipynb# (Louis)
│   │   └── 05_tourism_bonus_todo.ipynb     # (Romain)
│   └── src/                                # Modular production-ready Python functions
│       ├── __init__.py
│       ├── data_loader.py                  # Loading, profiling, and cleaning functions
│       ├── indicators.py                   # The 4 analytical queries + Tourism Bonus
│       └── dashboard.py                    # Interactive Plotly Dash web dashboard
│
└── rendu/                                  # Official deliverable package (DVLC submission)
    ├── README.md                           # Submission metadata & checklist
    ├── Laurent_notebook.ipynb              # Master executable notebook (all functions + __main__)
    ├── Laurent_dashboard.html              # Static offline proof of the Plotly Dash dashboard
    └── Laurent_slides.pdf                  # 5-minute final oral presentation slides
```

---

## 🚀 Quickstart & Development Setup

### 1. Clone & Setup Environment
```bash
git clone https://github.com/groupe-dia3-ml/programming-for-data-science.git
cd programming-for-data-science

# Create virtual environment
python -m venv .venv
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Local Data
Follow [`doc/DATA_SETUP.md`](doc/DATA_SETUP.md) to place `attacks.csv`, `tourism_arrivals.csv`, and `locations_geocoded.csv` inside `projet/data/`.

### 3. Run the Interactive Dashboard
```bash
python projet/src/dashboard.py
```
Open your browser at `http://127.0.0.1:8050/` to explore all five tabs.

### 4. Run the Master Deliverable Notebook
Open and run [`rendu/Laurent_notebook.ipynb`](rendu/Laurent_notebook.ipynb) in Jupyter. It executes all data collection, cleaning, query indicators, and proof generation from top to bottom with zero errors.

---
*May the Force be with you!* 🚀

# 🤖 Gemini / AI Agent & Team Project Bible: Final Project Guide

> **Course**: Programming for Data Science — Master in Data Science (ESILV)  
> **Instructor**: Hugo Alatrista-Salas  
> **Student Leader**: Maxime LAURENT (`maximelrnt`)  
> **Repository**: [groupe-dia3-ml/programming-for-data-science](https://github.com/groupe-dia3-ml/programming-for-data-science)  
> **Target Branch**: `main` (via Pull Requests from `feature/*`)

---

## 📌 1. Project Purpose & Core Directives

This document serves as the **operational instruction set** and **single source of truth** for AI assistants (Antigravity, Gemini) and human collaborators working on the Final Project.

### High-Level Objective
Construct an end-to-end **Knowledge Discovery in Databases (KDD)** prototype to extract, model, and visualize actionable intelligence from a **multidimensional dataset**.

A valid dataset **MUST** feature three fundamental axes:
1. 🕒 **Temporal Dimension (*When*)**: Timestamp, date, or sequential time steps.
2. 🗺️ **Spatial Dimension (*Where*)**: Geographic coordinates (latitude, longitude), administrative polygons, or geolocated zones.
3. 📊 **Analytical Dimension (*Characteristics*)**: Quantitative and qualitative domain metrics (e.g., casualties, magnitude, financial amount, category, duration, severity).

---

## 📋 2. Official Evaluation Rubric & Requirements

Total: **20 points + 1 bonus point**

| Task | Description | Points |
| :--- | :--- | :---: |
| **1. Data Exploration** | Load data, explore shape, data types, missing values, ranges. Full human-readable Markdown description of domain meaning. | **2 pts** |
| **2. Information Building** | **Four distinct analytical queries** implemented as modular functions with Markdown explanations: | **7 pts** |
| ↳ *Query 1* | Aggregation / Grouping query (e.g., maximum, sum, rate by group). | *1 pt* |
| ↳ *Query 2* | Frequent pattern mining (Apriori, PrefixSpan) or advanced ML (clustering, text mining). | *2 pts* |
| ↳ *Queries 3 & 4* | Two queries modeling Temporal and Spatial dynamics (Prophet forecasting & OPTICS/K-Means spatial clustering). | *4 pts* |
| **3. Interactive Dashboard** | Python **Dash** (Plotly) dashboard displaying the results of the 4 queries, team member names, and dataset title. | **2 pts** |
| **4. GitHub Repository** | Clean, organized public GitHub repository with informative README and modular code. | **1 pt** |
| **5. Presentation & Demo** | 5-minute slide deck presentation (`Laurent_slides.pdf`) and live notebook demonstration with Q&A. | **8 pts** |
| **6. External Dataset** | Enrich findings or contextualize results using a second complementary dataset. | **+1 bonus pt** |

### ⚠️ Critical Penalties to Avoid (from PDF):
* **-2 points**: Code not organized into functions with comments explaining name, input, output, and rationale.
* **-2 points**: Indicator not explained in human terms in a Markdown cell (calculation + interpretation).
* **-2 points**: Dashboard not functioning or lacking proof of execution.
* **-8 points**: Any group member absent during the live demo/presentation.

---

## 🏗️ 3. Strict Coding Conventions

According to **Page 4 of `Final_project.pdf`**, all notebook code must strictly follow this pattern:

```python
# ==============================================================================
# Function Definitions with Inputs, Outputs, and Comments
# ==============================================================================

def load_data(file_path: str) -> pd.DataFrame:
    """
    Function for loading the multidimensional dataset.
    
    Input:
        file_path (str): Relative or absolute path to the CSV/data file.
    Output:
        pd.DataFrame: Cleaned DataFrame ready for exploration.
    """
    # Read the CSV with proper delimiter and encoding
    df = pd.read_csv(file_path)
    # Strip whitespace from column headers
    df.columns = df.columns.str.strip()
    return df

def query_aggregation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Query 1: Computes aggregation metrics across categories.
    Input: df (pd.DataFrame)
    Output: pd.DataFrame with aggregated indicators
    """
    # Group by category and compute aggregate metrics
    grouped = df.groupby('category').agg({'value': ['count', 'sum', 'mean']})
    return grouped

# ... other query functions ...

# ==============================================================================
# Main Execution Block
# ==============================================================================
if __name__ == "__main__":
    # Step 1: Data collection & loading
    file_path = "data/my_dataset.csv"
    data = load_data(file_path)
    
    # Step 2: Indicators construction
    res_q1 = query_aggregation(data)
    res_q2 = query_pattern_mining(data)
    res_q3 = query_temporal_forecasting(data)
    res_q4 = query_spatial_clustering(data)
    
    # Step 3: Launch visualization prototype / Dashboard
    # launch_dashboard(data, res_q1, res_q2, res_q3, res_q4)
```

---

## 🗂️ 4. Recommended Multidimensional Datasets

The dataset must be **validated by the instructor**. Top candidates fitting all 3 axes:

1. **EM-DAT Global Disaster Database** ([https://doc.emdat.be](https://doc.emdat.be))
   * *Temporal*: Date, start year/month, duration.
   * *Spatial*: Country, region, latitude, longitude, ISO codes.
   * *Analytical*: Disaster type, deaths, injured, total damage (USD), disaster subgroup.
2. **NOAA Global Severe Weather & Climate** ([https://www.ncei.noaa.gov/access/search/index](https://www.ncei.noaa.gov/access/search/index))
   * *Temporal*: Timestamp of weather events.
   * *Spatial*: Station coordinates (lat/lon), state/country.
   * *Analytical*: Precipitation, temperature anomalies, storm severity.
3. **NYC TLC Yellow/Green Taxi Trip Records** ([NYC TLC Trip Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page))
   * *Temporal*: Pickup and dropoff datetime.
   * *Spatial*: Pickup/dropoff taxi zones or GPS coordinates.
   * *Analytical*: Fare amount, tip amount, passenger count, trip distance, payment type.
4. **Global Wildfire / Forest Fire Activity (NASA FIRMS / Kaggle)**
   * *Temporal*: Detection date & time.
   * *Spatial*: Latitude, longitude.
   * *Analytical*: Brightness temperature, fire radiative power (FRP), day/night, confidence.

---

## 🌿 5. Git & Pull Request Workflow

All work must follow an industry-standard Git workflow:

```text
main (stable, production-ready deliverable)
  │
  └── feature/final-project-setup (Pull Request #1: scaffolding & guidelines)
        │
        ├── feature/data-collection (PR: dataset validation & loading functions)
        ├── feature/indicators-modeling (PR: 4 queries implementation)
        └── feature/dash-prototype (PR: Plotly Dash web dashboard)
```

### Pull Request Rules:
1. **Never commit directly to `main`**: Always develop on a descriptive `feature/*` branch.
2. **Self-contained commits**: Meaningful commit messages following Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`).
3. **Reproducibility**: Ensure all code cells in notebooks run cleanly from top to bottom before pushing.
4. **No large junk files**: Keep `.venv-1/`, `.ipynb_checkpoints/`, `__pycache__/`, and temporary files out of Git.

---

## 📅 6. Project Checklist & Progress Tracker

- [x] **Repository Linking & Remote Configuration** (`groupe-dia3-ml/programming-for-data-science`)
- [x] **Project Scaffolding & Architecture** (`projet/src/`, `projet/data/`, `projet/slides/`)
- [x] **`gemini.md` & `requirements.txt` Setup**
- [ ] **Step 1: Dataset Selection & Teacher Validation**
- [ ] **Step 2: Data Exploration Notebook Section (`load_data`)**
- [ ] **Step 3: Query 1 (Aggregation Indicator)**
- [ ] **Step 4: Query 2 (Frequent Pattern Mining or ML)**
- [ ] **Step 5: Query 3 (Temporal Dynamics / Prophet Forecasting)**
- [ ] **Step 6: Query 4 (Spatial Information / OPTICS or K-Means Clustering)**
- [ ] **Step 7: Plotly Dash Interactive Dashboard (`dashboard.py`)**
- [ ] **Step 8: HTML/PDF Dashboard Export (`Laurent_dashboard.html`)**
- [ ] **Step 9: Slides Deck Preparation (`Laurent_slides.pdf`)**
- [ ] **Step 10: 5-Minute Presentation & Demo Rehearsal**

# Local Data Directory

Datasets are **not tracked by Git** (see `.gitignore`). Every team member must install the datasets locally in this folder.

Follow the complete step-by-step installation guide in [`../../doc/DATA_SETUP.md`](../../doc/DATA_SETUP.md).

## Expected Local Files

1. `attacks.csv` (or `GSAF5.xls`) — Primary dataset from Kaggle (`https://www.kaggle.com/datasets/mexwell/global-shark-attack`)
2. `tourism_arrivals.csv` — External bonus dataset from World Bank (`https://data.worldbank.org/indicator/ST.INT.ARVL`)
3. `locations_geocoded.csv` — Coastal `(Area, Country -> latitude, longitude)` cache generated once by `04_spatial_clustering_todo.ipynb`
4. `countries_shp/` — Natural Earth country polygons copied from Lab 8 (`ne_110m_admin_0_countries.*`)

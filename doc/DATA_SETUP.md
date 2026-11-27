# Local Data Installation & Setup Guide

Datasets are **not committed to Git** (they are ignored via `.gitignore`). Every team member can either download them manually into `projet/data/` OR simply run any notebook: `load_shark_data()` and `load_tourism_data()` use cross-platform `pathlib.Path` and **automatically download both CSVs in pure Python** (Windows, macOS, Linux, no Kaggle login required) whenever local files are not found.

---

## 1. Expected Local Folder Layout

After completing the steps below, your local `projet/data/` folder should look like this:

```text
projet/data/
├── .gitkeep
├── README.md
├── attacks.csv                  # Primary dataset (Global Shark Attack - Kaggle mexwell)
├── tourism_arrivals.csv         # External bonus dataset (World Bank ST.INT.ARVL)
├── locations_geocoded.csv       # Generated once by notebook 04 (coastal coordinates cache)
└── countries_shp/               # Optional Natural Earth shapefile (copied from Lab 8)
    ├── ne_110m_admin_0_countries.shp
    ├── ne_110m_admin_0_countries.dbf
    ├── ne_110m_admin_0_countries.shx
    └── ne_110m_admin_0_countries.prj
```

---

## 2. Primary Dataset — Global Shark Attack (Kaggle)

- **Title:** Global Shark Attack (GSAF — Global Shark Attack File)
- **URL:** https://www.kaggle.com/datasets/mexwell/global-shark-attack

### Manual Download (Recommended)
1. Open https://www.kaggle.com/datasets/mexwell/global-shark-attack and sign in to your Kaggle account.
2. Click **Download** to download the archive (`.zip`).
3. Extract the archive and locate the main data file (e.g. `attacks.csv` or `GSAF5.xls` / `global-shark-attack.csv`).
4. Move the file into `projet/data/` and rename it cleanly to **`attacks.csv`** (or keep `GSAF5.xls` if it is an Excel file — `projet/src/data_loader.py` is designed to handle both).

---

## 3. External Bonus Dataset — International Tourism Arrivals (World Bank)

- **Title:** International tourism, number of arrivals (Indicator `ST.INT.ARVL`)
- **Official Page:** https://data.worldbank.org/indicator/ST.INT.ARVL
- **Direct CSV ZIP Download (no login required):** https://api.worldbank.org/v2/en/indicator/ST.INT.ARVL?downloadformat=csv
- **Coverage:** 266 countries and regions, 1995-2020 (26 years).

### Option A — Automatic Download via Python (Fastest, Recommended)

From the root of the repository (with `.venv` activated), run:

```bash
python -c "import requests, zipfile, io, os; os.makedirs('projet/data', exist_ok=True); r = requests.get('https://api.worldbank.org/v2/en/indicator/ST.INT.ARVL?downloadformat=csv', timeout=20); z = zipfile.ZipFile(io.BytesIO(r.content)); name = [n for n in z.namelist() if n.startswith('API_ST.INT.ARVL')][0]; open('projet/data/tourism_arrivals.csv', 'wb').write(z.read(name)); print('Saved projet/data/tourism_arrivals.csv')"
```

### Option B — Manual Download
1. Open https://data.worldbank.org/indicator/ST.INT.ARVL and click **CSV** under the *Download* section (or open the direct ZIP URL above).
2. Extract the downloaded `.zip` archive.
3. Find the file named `API_ST.INT.ARVL_DS2_en_csv_v2_*.csv`.
4. Copy it to `projet/data/` and rename it to **`tourism_arrivals.csv`**.

> [!NOTE]
> The World Bank CSV contains 4 metadata header rows at the top. Always load it with `pd.read_csv("projet/data/tourism_arrivals.csv", skiprows=4)`.

---

## 4. Spatial Auxiliary Files (for Query 4)

1. **Country Shapefile (`projet/data/countries_shp/`):**
   - Copy the `countries_shp/` folder provided in **Lab 8** (`ne_110m_admin_0_countries.*`) into `projet/data/countries_shp/`.
   - Alternatively, download the 110m Admin 0 Countries shapefile from Natural Earth (`https://www.naturalearthdata.com/downloads/110m-cultural-vectors/`).
2. **Geocoded Coastal Zones (`projet/data/locations_geocoded.csv`):**
   - The raw GSAF dataset stores `Country`, `Area`, and `Location` as text without raw `latitude`/`longitude` columns.
   - The geocoding cell assigns coastal area coordinates from a local lookup and caches them. It reuses matching pairs, looks up newly encountered pairs, and records country-only fallbacks separately from area coordinates.

---

## 5. Verify Your Local Data Setup

Run this quick check from the repository root after placing your files:

```bash
python -c "import os; files = ['projet/data/attacks.csv', 'projet/data/tourism_arrivals.csv']; print({f: os.path.exists(f) for f in files})"
```

Both entries should return `True` before you start coding the notebooks.

The offline HTML proof embeds Plotly and the [Plotly world 110m basemap](https://cdn.plot.ly/un/world_110m.json). The repository includes the basemap asset. For standalone notebook generation, place it under `data/world_110m.json` or allow the notebook to download it once.

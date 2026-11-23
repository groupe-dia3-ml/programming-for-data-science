# Environment & Dependencies Setup Guide

This guide explains how every team member sets up an identical local Python environment for the **Programming for Data Science** final project.

---

## 1. Prerequisites

- **Python:** 3.10 or 3.11 (recommended for smooth `prophet` and `geopandas` wheel compatibility on Windows and macOS).
- **Git:** Latest stable version.
- **IDE:** VS Code (with the Python and Jupyter extensions) or JupyterLab.

Check your Python version before starting:

```bash
python --version
```

---

## 2. Create and Activate the Virtual Environment

Always work inside a local `.venv` at the root of the repository (ignored by `.gitignore`).

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Python Dependencies

Upgrade `pip` first, then install everything from `requirements.txt`:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Key Libraries Included

| Category | Packages | Usage in Project |
| --- | --- | --- |
| Data Manipulation | `pandas`, `numpy`, `scipy`, `openpyxl`, `xlrd` | Loading CSV/Excel datasets, cleaning, merging, correlations |
| Visualization & Dashboard | `plotly`, `dash`, `dash-bootstrap-components`, `matplotlib` | Interactive figures and Dash web application |
| Frequent Pattern Mining | `mlxtend`, `prefixspan` | Query 2 — `apriori` and `association_rules` |
| Temporal Modeling | `prophet` | Query 3 — Multi-year shark attack forecasting |
| Spatial Modeling | `geopandas`, `shapely`, `scikit-learn` | Query 4 — GeoDataFrames, spatial joins, `OPTICS` and `KMeans` |
| Notebooks & HTTP | `jupyter`, `ipykernel`, `nbformat`, `requests` | Running `.ipynb` notebooks and World Bank CSV download / geocoding |

---

## 4. Register the Jupyter Kernel (Recommended)

So VS Code and Jupyter can select `.venv` directly:

```bash
python -m ipykernel install --user --name=pds-shark-project --display-name="Python (.venv - PDS Project)"
```

---

## 5. Verify Your Installation

Run this single check to make sure all core packages import without errors:

```bash
python -c "import pandas, numpy, scipy, plotly, dash, prophet, mlxtend, geopandas, sklearn, requests; print('Environment OK')"
```

Expected output:

```text
Environment OK
```

---

## 6. Next Step: Local Datasets

Datasets are **not committed to Git** — each team member downloads them locally into `projet/data/`.
Follow [`doc/DATA_SETUP.md`](doc/DATA_SETUP.md) to download both datasets and verify file paths.

---

## 7. Common Troubleshooting

- **`UnicodeDecodeError` when reading the Shark Attacks CSV:** Always pass `encoding="latin-1"` (or `encoding="ISO-8859-1"`) to `pd.read_csv()`.
- **`.xls` file instead of `.csv`:** If the Kaggle archive contains an Excel file (`GSAF5.xls` / `.xlsx`), `xlrd` and `openpyxl` are already included in `requirements.txt` so `pd.read_excel()` works out of the box.
- **`prophet` slow first import:** Prophet initializes `cmdstanpy` on first load; this is normal and only happens once per kernel session.

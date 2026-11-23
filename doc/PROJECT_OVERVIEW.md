# Project Overview & Grading Rubric

## 1. Academic Context

- **Institution:** ESILV — Ecole Superieure d'Ingenieurs Leonard de Vinci (A4 DIA3, 2026-2027)
- **Course:** Programming for Data Science
- **Instructor:** Hugo Alatrista-Salas
- **Repository:** https://github.com/groupe-dia3-ml/programming-for-data-science
- **Official Subject:** [`projet/Final_project.pdf`](../projet/Final_project.pdf)

---

## 2. Project Goal & Multidimensional Problem Statement

This project implements an end-to-end **Knowledge Discovery in Databases (KDD)** workflow on global shark attack incidents (`Global Shark Attack — GSAF`), enriched with international tourism arrival statistics (`World Bank ST.INT.ARVL`).

The primary dataset satisfies all three mandatory multidimensional axes:
1. **Temporal Dimension (When):** Incident `Date`, `Year`, `Month`, and `Time` spanning several decades (dense modern reporting from 1960 onward).
2. **Spatial Dimension (Where):** `Country`, `Area`, and `Location` enriched with geocoded `(latitude, longitude)` coordinates for coastal hotspot clustering.
3. **Analytical Dimension (What):** Incident `Type` (Unprovoked, Provoked, Boating, etc.), `Activity` (Surfing, Swimming, Diving, Fishing, Wading), shark `Species`, victim `Sex`/`Age`, `Injury`, and `Fatal (Y/N)`.

**Core Research Question:**
*How are global shark attacks distributed across time, seasons, activities, and coastal hotspots, and does the historical increase in reported attacks reflect a rising risk or simply the growth of international coastal tourism?*

---

## 3. Official Evaluation Rubric (20 Points + 1 Bonus Point)

| Task | Requirement | Points | Deliverable / Module |
| --- | --- | :---: | --- |
| **1. Data Exploration** | Load datasets, print rows/columns, data types, missing values per column, numeric value ranges, and human-readable Markdown description of dataset meaning and dropped features. | **2 pts** | `01_eda_and_cleaning.ipynb` / `src/data_loader.py` |
| **2. Information Building** | Four distinct analytical queries implemented as functions, each visualized and explained in a dedicated Markdown cell: | **7 pts** | `02..04_*.ipynb` / `src/indicators.py` |
| - Query 1 | Grouping / aggregation query (top countries, activity distribution, fatality rates). | *1 pt* | `02_grouping_and_apriori.ipynb` |
| - Query 2 | Frequent pattern mining (`mlxtend` `apriori` + `association_rules`). | *2 pts* | `02_grouping_and_apriori.ipynb` |
| - Query 3 | Temporal analysis and multi-year forecasting (`Prophet`). | *2 pts* | `03_temporal_forecasting.ipynb` |
| - Query 4 | Spatial analysis and hotspot clustering (`GeoPandas` + `OPTICS`/`K-Means`). | *2 pts* | `04_spatial_clustering.ipynb` |
| **3. Visualization Dashboard** | Python **Dash** dashboard organizing all four queries + tourism bonus, clearly displaying all 4 team member names and dataset names. | **2 pts** | `src/dashboard.py` + `rendu/Laurent_dashboard.html` |
| **4. GitHub Repository** | Public GitHub repository with clean modular code, informative `README.md`, and documentation. | **1 pt** | Root repo + `doc/` |
| **5. Presentation & Demo** | 5-minute slide presentation (`Laurent_slides.pdf`), live notebook demo (presenter picked right before start), and Q&A. | **8 pts** | `rendu/Laurent_slides.pdf` + `rendu/Laurent_notebook.ipynb` |
| **6. External Dataset (Bonus)** | Enrich and interpret primary findings with World Bank International Tourism (`ST.INT.ARVL`, 1995-2020). | **+1 pt** | `05_tourism_bonus.ipynb` |

---

## 4. Critical Anti-Penalty Checklist

Before submitting to DVLC, verify every single rule below:

- [ ] **[-2 pts penalty]** All code is organized into functions (`def name_function():`) called from `if __name__ == "__main__":` and hosted in a **public** GitHub repository with a clear `README.md`.
- [ ] **[-2 pts penalty]** Every single function includes comments documenting its purpose, `# Input:`, and `# Output:`, and every dropped column or filtering decision is justified in Markdown/comments.
- [ ] **[-2 pts penalty]** Every single indicator has a dedicated human-readable **Markdown cell** explaining how it is calculated, what it represents, and how to interpret it.
- [ ] **[-2 pts penalty]** The Dash dashboard runs without errors AND static proof (`rendu/Laurent_dashboard.html` or `.pdf`) is included in the submission.
- [ ] **[-8 pts penalty]** All 4 team members are physically present during the presentation and capable of running the live demo and answering Q&A.

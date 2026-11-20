# Final Project — Multidimensional KDD Visualization Prototype

> **Course**: Programming for Data Science — Master in Data Science (ESILV)  
> **Instructor**: Hugo Alatrista-Salas  
> **Lead Deliverable**: `Laurent_notebook.ipynb`  
> **Presentation**: `Laurent_slides.pdf`  
> **Dashboard**: `Laurent_dashboard.html` / `src/dashboard.py`

---

## 🎯 Project Objective

The goal of this final project is to build an end-to-end data mining and visualization prototype applying the **Knowledge Discovery in Databases (KDD)** process to a **multidimensional dataset**:
1. **Temporal Dimension (*When*)**: Event dates, periods, or time-series timestamps.
2. **Spatial Dimension (*Where*)**: Latitude, longitude, country, city, or administrative zones.
3. **Analytical Dimension (*Characteristics*)**: Quantitative attributes, categories, and domain metrics.

---

## 📂 Project Directory Structure

```text
projet/
├── Final_project.pdf            # Official project subject & evaluation rules
├── README.md                    # Project-level guide & instructions
├── Laurent_notebook.ipynb       # Main submission notebook
│
├── data/                        # Datasets directory
│   ├── .gitkeep
│   └── README.md                # Data documentation & sourcing links
│
├── src/                         # Modular Python functions
│   ├── __init__.py
│   ├── data_loader.py           # Data ingestion, schema validation & exploration
│   ├── indicators.py            # The 4 analytical queries (Aggregation, Mining, Time, Space)
│   └── dashboard.py             # Plotly Dash web dashboard application
│
└── slides/                      # Presentation slides directory
    └── README.md                # Slide guidelines & timing (5 minutes presentation)
```

---

## 📋 Deliverable & Grading Checklist (20 Points + 1 Extra Point)

### 1. Data Exploration [2 points]
* Load multidimensional dataset into a pandas DataFrame.
* Profile the data: number of rows and columns, data types, missing value distribution, numerical value ranges.
* Human-readable Markdown cell explaining the real-world significance of each attribute.

### 2. Information Building (4 Queries) [7 points]
* **Query 1 [1 pt]**: Aggregation / grouping query (e.g. `groupby` with `sum`, `max`, `count`, rate calculations).
* **Query 2 [2 pts]**: Frequent pattern mining (Apriori, PrefixSpan) or advanced ML (deep learning, text mining).
* **Queries 3 & 4 [4 pts]**: Temporal forecasting (Prophet) and Spatial clustering (OPTICS / K-Means on coordinates with GeoPandas).
* *Mandatory:* Every indicator must have an accompanying Markdown box describing how it was computed, what it represents, and how to interpret it.

### 3. Interactive Visualization Dashboard [2 points]
* Implemented in Python **Dash** (`src/dashboard.py`).
* Consolidates all four query results into an intuitive visual layout.
* Clearly displays team member names and dataset title.

### 4. GitHub Repository [1 point]
* Code organized cleanly into reusable functions.
* Detailed README and `.gitignore`.

### 5. Final Presentation & Demo [8 points]
* 5-minute presentation using slides (`Laurent_slides.pdf`).
* Live demo of the notebook and dashboard.
* Q&A session with the instructor.

### 6. External Dataset [1 Extra Point]
* Enrich analysis by joining or cross-referencing an external data source.

---

## ⚠️ Anti-Penalty Rules (Avoid Losing Points!)
1. **Always use functions with docstrings:** Every technique must be encapsulated in a `def func_name(df):` block with comments detailing `Input`, `Output`, and key implementation decisions (**-2 pts penalty if missing**).
2. **Always document indicators in Markdown:** No standalone code without human explanation (**-2 pts penalty if missing**).
3. **Working Dashboard:** Must be verifiable and operational (**-2 pts penalty if broken**).
4. **All team members must be present at the demo** (**-8 pts penalty if missing**).

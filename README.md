# Programming for Data Science — ESILV (Master Data & IA)

Repository for the **Programming for Data Science** course taught by **Hugo Alatrista-Salas** at **ESILV (École Supérieure d'Ingénieurs Léonard de Vinci)**.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Repository](https://img.shields.io/badge/GitHub-groupe--dia3--ml-green.svg)](https://github.com/groupe-dia3-ml/programming-for-data-science)
[![Framework](https://img.shields.io/badge/Dashboard-Plotly%20Dash-orange.svg)](https://dash.plotly.com/)

---

## 👥 Team Members

* **Maxime LAURENT** (*Team Leader*) — [maxime.laurent@edu.devinci.fr](mailto:maxime.laurent@edu.devinci.fr)
* *(Team members to be added)*

---

## 📁 Repository Architecture

```text
├── projet/                          # 🚀 FINAL PROJECT DELIVERABLE WORKSPACE
│   ├── Final_project.pdf            # Official project requirements & instructions
│   ├── README.md                    # Detailed guide to project requirements & scoring
│   ├── Laurent_notebook.ipynb       # Official deliverable notebook (functions + main block)
│   ├── data/                        # Datasets (Temporal, Spatial, Analytical)
│   ├── src/                         # Modular Python functions
│   │   ├── __init__.py
│   │   ├── data_loader.py           # Data loading & statistical profiling
│   │   ├── indicators.py            # The 4 analytical queries / indicators
│   │   └── dashboard.py             # Interactive Plotly Dash web application
│   └── slides/                      # Final 5-minute presentation slides
│
├── gemini.md                        # 🤖 AI Assistant & Team Project Bible / Roadmap
├── requirements.txt                 # Project Python dependencies
└── .gitignore                       # Clean Git exclusion rules
```

---

## 🚀 Quickstart & Setup

### 1. Clone the repository
```bash
git clone https://github.com/groupe-dia3-ml/programming-for-data-science.git
cd programming-for-data-science
```

### 2. Set up virtual environment
```bash
python -m venv .venv
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the interactive Dashboard prototype
```bash
cd projet
python src/dashboard.py
```
Open your browser at `http://127.0.0.1:8050/` to explore the dashboard.

---

## 🎯 Final Project Overview

The objective is to implement the full **Knowledge Discovery in Databases (KDD)** pipeline on a real **multidimensional dataset** (combining **Temporal**, **Spatial**, and **Analytical** dimensions).

The deliverable includes:
1. **Interactive Notebook (`Laurent_notebook.ipynb`)**: Clean modular functions with documented inputs/outputs and human-readable Markdown explanations.
2. **Four Analytical Queries**:
   - Aggregation / Grouping query [1 pt]
   - Pattern Mining / ML query [2 pts]
   - Temporal forecasting (Prophet) [2 pts]
   - Spatial clustering (OPTICS / K-Means / GeoPandas) [2 pts]
3. **Interactive Dashboard (`dashboard.py`)**: Built with Plotly Dash organizing the 4 indicators.
4. **Final Presentation (`Laurent_slides.pdf`)**: 5-minute slide deck and live demonstration.

See [`gemini.md`](gemini.md) and [`projet/README.md`](projet/README.md) for full instructions, grading rubrics, and development workflows.

# Project Guidelines & AI Assistant Reference

> **Course:** Programming for Data Science — ESILV A4 DIA3 (2026-2027)
> **Instructor:** Hugo Alatrista-Salas
> **Team Leader:** Maxime Laurent (`@maximelrnt`)
> **Members:** Maxime Laurent, Louis Le Forestier, Baptiste Noailhac, Romain Thepaut
> **Repository:** https://github.com/groupe-dia3-ml/programming-for-data-science

---

## 1. Selected Datasets (Local Only — Not Tracked in Git)

1. **Primary Multidimensional Dataset:** Global Shark Attack (GSAF)
   - Source: https://www.kaggle.com/datasets/mexwell/global-shark-attack
   - Expected local path: `projet/data/attacks.csv` (or `GSAF5.xls`)
2. **External Bonus Dataset (+1 extra point):** International tourism, number of arrivals (World Bank `ST.INT.ARVL`)
   - Source: https://data.worldbank.org/indicator/ST.INT.ARVL
   - Direct CSV ZIP: https://api.worldbank.org/v2/en/indicator/ST.INT.ARVL?downloadformat=csv
   - Expected local path: `projet/data/tourism_arrivals.csv`

Full local installation instructions are documented in [`doc/DATA_SETUP.md`](doc/DATA_SETUP.md).

---

## 2. Repository Map & Source of Truth

- [`README.md`](README.md) — Main project overview and team ownership table
- [`REQUIREMENTS.md`](REQUIREMENTS.md) & [`requirements.txt`](requirements.txt) — Python environment setup
- [`doc/PROJECT_OVERVIEW.md`](doc/PROJECT_OVERVIEW.md) — Official rubric (`20 pts + 1 bonus pt`) and anti-penalty checklist
- [`doc/DATA_SETUP.md`](doc/DATA_SETUP.md) — Local dataset download and verification guide
- [`doc/INDICATORS_SPEC.md`](doc/INDICATORS_SPEC.md) — Technical specs for Queries 1-4, Tourism Bonus, and Dash dashboard
- [`doc/TEAM_WORKFLOW.md`](doc/TEAM_WORKFLOW.md) — Ownership split and Git workflow
- `projet/notebooks/*_todo.ipynb` — Working notebooks with structured `TODO` scaffolds
- `projet/src/` — Shared modular Python functions (`data_loader.py`, `indicators.py`, `dashboard.py`)
- `rendu/` — Official DVLC deliverables (`Laurent_notebook.ipynb`, `Laurent_dashboard.html`, `Laurent_slides.pdf`)

---

## 3. Coding & Grading Rules (Mandatory)

1. Write all Python code, variable names, docstrings, and comments in **English**, in a clean, readable student style.
2. Encapsulate every data loading, cleaning, querying, and dashboard step inside functions (`def func_name(...):`) with explicit `# Function ...`, `# Input: ...`, and `# Output: ...` comment headers (`-2 pts` penalty if missing).
3. Call all functions in order from a single `if __name__ == "__main__":` block in `rendu/Laurent_notebook.ipynb`.
4. Justify every dropped column and cleaning decision in Markdown/comments (`-2 pts` penalty if missing).
5. Accompany every analytical indicator with a human-readable Markdown cell explaining calculation, meaning, and interpretation (`-2 pts` penalty per missing indicator).
6. Never commit local dataset files (`projet/data/*.csv`, `*.xls*`, `*.zip`) to Git.
7. Do not use emojis in code, comments, notebooks, or Markdown documentation.

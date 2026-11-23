# Team Workflow & Collaboration Guide

## 1. Team Ownership Split

| Member | GitHub | Assigned Notebooks & Modules | Branch Name |
| --- | --- | --- | --- |
| **Maxime Laurent** (Team Leader) | `@maximelrnt` | `01_eda_and_cleaning_todo.ipynb`, `src/data_loader.py`, final assembly of `rendu/Laurent_notebook.ipynb` & `rendu/Laurent_slides.pdf` | `feature/eda-cleaning` |
| **Baptiste Noailhac** | `@BaptisteNoai` | `02_grouping_and_apriori_todo.ipynb`, Query 1 & Query 2 in `src/indicators.py` | `feature/grouping-apriori` |
| **Romain Thepaut** | `@RomThpt` | `03_temporal_forecasting_todo.ipynb`, `05_tourism_bonus_todo.ipynb`, Query 3 & Bonus in `src/indicators.py` | `feature/temporal-tourism` |
| **Louis Le Forestier** | `@louislefo` | `04_spatial_clustering_todo.ipynb`, Query 4 in `src/indicators.py`, `src/dashboard.py`, `rendu/Laurent_dashboard.html` | `feature/spatial-dashboard` |

---

## 2. Step-by-Step Collaboration Pipeline

1. **Phase 1 — Local Setup (Everyone):**
   - Clone `groupe-dia3-ml/programming-for-data-science`.
   - Follow [`REQUIREMENTS.md`](../REQUIREMENTS.md) and [`doc/DATA_SETUP.md`](DATA_SETUP.md).
2. **Phase 2 — Cleaning Contract First (Maxime):**
   - Implement `src/data_loader.py` and `01_eda_and_cleaning_todo.ipynb` first so everyone uses the exact same cleaned columns (`Year`, `Month`, `Season`, `Country_clean`, `Area_clean`, `Activity_group`, `Time_of_day`, `Fatal_clean`) and merged tourism table.
3. **Phase 3 — Parallel Work on Queries (Baptiste, Romain, Louis):**
   - Each member completes their assigned `*_todo.ipynb` notebook and copies finalized reusable functions into `projet/src/indicators.py` / `projet/src/dashboard.py`.
   - Every indicator must include a clear Markdown explanation (calculation, meaning, interpretation).
4. **Phase 4 — Final Consolidation (`rendu/`):**
   - Merge all finalized functions and Markdown explanations into `rendu/Laurent_notebook.ipynb` with a single `if __name__ == "__main__":` block at the end.
   - Generate `rendu/Laurent_dashboard.html` (and optionally print to PDF).
   - Finalize the 5-minute slide deck in `rendu/Laurent_slides.pdf`.
   - Switch the GitHub repository from **Private** to **Public** before submission.

---

## 3. Coding Standards (Mandatory for Full Credit)

1. **Language:** Write all Python code, variable names, docstrings, and comments in **English**.
2. **Function Header Format (from `Final_project.pdf` page 4):**
   Every function must follow this comment format to avoid the `-2 pts` penalty:
   ```python
   # Function for computing attack counts and fatality rates by activity
   # Input: cleaned shark attacks DataFrame
   # Output: aggregated DataFrame sorted by attack count
   def compute_activity_stats(df):
       ...
   ```
3. **Student-Readable Code:** Keep functions simple, explicit, well-commented line by line where helpful, and easy for every member to explain during Q&A (the presenter for the live demo is picked randomly by the instructor right before the presentation).
4. **No Local Data in Git:** Never `git add -f` any `.csv`, `.xls`, or `.zip` file inside `projet/data/`.
5. **No Emojis:** Keep all Markdown files, code comments, charts, and slides clean and technical without emojis.

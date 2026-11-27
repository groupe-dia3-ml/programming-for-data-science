# Final Deliverables Folder (`rendu/`)

This folder holds the **official team deliverables** to upload to **DVLC** before the last lab session.

---

## Required Files

| File | Required | Status | Description |
| --- | :---: | :---: | --- |
| [`notebook.ipynb`](notebook.ipynb) | Mandatory | Completed & executed (self-contained) | Complete KDD notebook (header with all 6 team members + GitHub link, modular documented functions, Markdown explanations for every indicator, single `if __name__ == "__main__":` block). |
| [`slides.pdf`](slides.pdf) | Mandatory | Ready (rebuild PDF from `slides.tex` after updating member names) | 10-minute group presentation slide deck exported to PDF (see [`projet/slides/README.md`](../projet/slides/README.md)). |
| [`dashboard.html`](dashboard.html) | Strongly recommended | Generated (offline HTML proof ready) | Self-contained HTML proof with all 12 plots and their world basemap. |

---

## Pre-Submission Verification Checklist

- [ ] `notebook.ipynb` runs top-to-bottom without errors (uses local data files in `projet/data/` or auto-downloads if absent).
- [ ] Every function has `# Function ...`, `# Input: ...`, `# Output: ...` comments (`-2 pts` penalty if missing).
- [ ] Every dropped column and cleaning decision is justified in Markdown (`-2 pts` penalty if missing).
- [ ] Every indicator (Queries 1 to 4 + Tourism Bonus) has a dedicated Markdown explanation cell (calculation, meaning, interpretation; `-2 pts` penalty if missing).
- [ ] The Dash dashboard displays all 6 team member names (`Maxime Laurent`, `Louis Le Forestier`, `Baptiste Noailhac`, `Romain Thepaut`, `Fabien Ramel`, `Rayan Iguercha`) and both dataset names.
- [ ] `dashboard.html` opens cleanly offline with all interactive Plotly charts.
- [ ] GitHub repository `https://github.com/groupe-dia3-ml/programming-for-data-science` is set to **Public** (`[1 pt]`) with an up-to-date `README.md`.
- [ ] All 6 team members are prepared and present for the **10-minute group presentation + Q&A** (`-8 pts` penalty if any member is absent).

# Final Deliverables Folder (`rendu/`)

This folder holds the **official deliverables** to upload to **DVLC** by the Team Leader (**Maxime Laurent**) before the last lab session.

---

## Required Files & Exact Naming Convention

Per [`projet/Final_project.pdf`](../projet/Final_project.pdf) (Section 5), deliverables must use the Team Leader's family name (`Laurent`):

| File | Required | Status | Description |
| --- | :---: | :---: | --- |
| `Laurent_notebook.ipynb` | Mandatory | Completed & executed (self-contained) | Complete KDD notebook (header with 4 team members + GitHub link, modular documented functions, Markdown explanations for every indicator, single `if __name__ == "__main__":` block). |
| `Laurent_slides.pdf` | Mandatory | To be added | 5-minute slide deck exported to PDF (see [`projet/slides/README.md`](../projet/slides/README.md)). |
| `Laurent_dashboard.html` (or `.pdf`) | Strongly recommended | Generated (offline HTML proof ready) | Offline visual proof of the working Plotly Dash dashboard (prevents `-2 pts` penalty). |

---

## Pre-Submission Verification Checklist

- [ ] `Laurent_notebook.ipynb` runs top-to-bottom without errors when local data files are in `projet/data/`.
- [ ] Every function has `# Function ...`, `# Input: ...`, `# Output: ...` comments.
- [ ] Every dropped column and cleaning decision is justified in Markdown.
- [ ] Every indicator (Queries 1 to 4 + Tourism Bonus) has a dedicated Markdown explanation cell (calculation, meaning, interpretation).
- [ ] The Dash dashboard displays all 4 team member names (`Maxime Laurent`, `Louis Le Forestier`, `Baptiste Noailhac`, `Romain Thepaut`) and both dataset names.
- [ ] `Laurent_dashboard.html` opens cleanly offline with all interactive Plotly charts.
- [ ] GitHub repository `https://github.com/groupe-dia3-ml/programming-for-data-science` is set to **Public** with an up-to-date `README.md`.
- [ ] All 4 members have tested running the notebook locally for the random live demo selection.

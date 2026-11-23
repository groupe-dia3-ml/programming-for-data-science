# Presentation Slides Guide (5 Minutes + Live Demo + Q&A)

The final exported slide deck must be placed in **`../../rendu/Laurent_slides.pdf`** before uploading to DVLC.

## Recommended 6-Slide Structure (5 Minutes Total)

| Slide | Title | Target Time | Key Content |
| :---: | --- | :---: | --- |
| **1** | Context, Team & Datasets | 0:45 | Project title, 4 team members, multidimensional problem statement, Global Shark Attack (GSAF) + World Bank Tourism (`ST.INT.ARVL`). |
| **2** | KDD Pipeline & Data Cleaning | 0:45 | Dataset dimensions, missing values, dropped columns justification, country normalization, and coastal geocoding. |
| **3** | Queries 1 & 2 (Grouping & Apriori) | 1:00 | Top countries, fatality rate by activity/species, and strongest `Apriori` association rules (support, confidence, lift). |
| **4** | Queries 3 & 4 (Forecast & Spatial) | 1:00 | Northern vs. Southern hemisphere seasonality, `Prophet` 5-year forecast, and `OPTICS` / `K-Means` coastal hotspot clusters. |
| **5** | External Dataset Bonus (Tourism) | 1:00 | Raw attack count vs. **Attacks per 1M tourists** (1995-2020) and correlation analysis explaining temporal trends. |
| **6** | Conclusion & Demo Transition | 0:30 | Key takeaways, data limitations (reporting bias, missing territories), and live transition to `Laurent_notebook.ipynb` and Dash. |

## Important Reminder

The instructor chooses **one student randomly** right before the presentation to run the live demo. All 4 team members must attend (`-8 pts` penalty if anyone is absent) and be able to explain every function in `rendu/Laurent_notebook.ipynb`.

# Presentation Slides Guide (10-Minute Group Presentation + Live Demo + Q&A)

The six-slide presentation is available as [`slides.pdf`](../../rendu/slides.pdf). Edit [`slides.tex`](slides.tex) to revise the slides.

Build from the repository root with TeX Live (XeLaTeX, Beamer, PGFPlots, and TeX Gyre Heros).

```sh
slides_build=$(mktemp -d)
latexmk -xelatex -halt-on-error -outdir="$slides_build" projet/slides/slides.tex
cp "$slides_build/slides.pdf" rendu/slides.pdf
```

The cover illustration and vector map are in `assets/`. The map uses the coastal cluster points saved in the final notebook and [Natural Earth 1:110m land](https://github.com/nvkelso/natural-earth-vector/blob/v5.1.2/geojson/ne_110m_land.geojson).

## Recommended 6-Slide Structure (10 Minutes Total + Q&A)

| Slide | Title | Target Time | Key Content |
| :---: | --- | :---: | --- |
| **1** | Context, Team & Datasets | 1:15 | Project title, all 6 team members, multidimensional problem statement, Global Shark Attack (GSAF) + World Bank Tourism (`ST.INT.ARVL`). |
| **2** | KDD Pipeline & Data Cleaning | 1:30 | Dataset dimensions, missing values, dropped columns justification, country normalization, and coastal geocoding. |
| **3** | Queries 1 & 2 (Grouping & Apriori) | 2:00 | Top countries, fatality rate by activity/species, and strongest `Apriori` association rules (support, confidence, lift). |
| **4** | Queries 3 & 4 (Forecast & Spatial) | 2:00 | Northern vs. Southern hemisphere seasonality, `Prophet` 5-year forecast, and `OPTICS` / `K-Means` coastal hotspot clusters. |
| **5** | External Dataset Bonus (Tourism) | 2:00 | Raw attack count vs. **Incidents per 1M arrivals** (1995–2017) and the correlation across matched country-years. |
| **6** | Conclusion & Demo Transition | 1:15 | Key takeaways, data limitations (reporting bias, missing territories), and live transition to `notebook.ipynb` and Dash (`dashboard.html`). |

## Important Reminder

The oral defense is a **10-minute group presentation with Q&A** where all 6 team members present together (no random draw). All 6 team members must attend (`-8 pts` penalty if anyone is absent) and be able to answer questions on `rendu/notebook.ipynb`.

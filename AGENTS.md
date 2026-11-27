# Programming in Data Science

This repository contains the DIA3 final project on reported shark incidents and international tourism arrivals. The official rubric is in `projet/Final_project.pdf`.

## Run and validate

- Install dependencies with `python -m pip install -r requirements.txt` in a Python virtual environment.
- Follow `doc/DATA_SETUP.md` for dataset filenames and sources. Keep raw datasets local.
- From the repository root, validate the submission notebook with `jupyter nbconvert --to notebook --execute --output-dir=/tmp rendu/Laurent_notebook.ipynb`.
- Rebuild the slides with the command in `projet/slides/README.md` and review the rendered PDF.

## Deliverables

- Keep the submission notebook self-contained so it can run on DVLC with the required libraries and dataset files or download access.
- Preserve the `Laurent_` filenames required for the team submission. Update the slide source and export together.
- Keep reported incident counts distinct from individual risk. Note the missing country-years when interpreting tourism ratios.

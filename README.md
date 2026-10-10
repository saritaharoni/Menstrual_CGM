# Menstrual cycle dynamics of CGM metrics and diet in non-diabetic women: figure code

Code that reproduces Figures 2–6 and Table 1 of the manuscript from pre-computed analysis results.

## Contents
- `Menstrual_CGM.ipynb`: renders Figures 2–6 and Table 1, saved with its outputs.
- `figures/`: the rendered figures (PNG and PDF).
- `fig_store.py`, `plot_helpers.py`: small helper modules used by the notebook.
- `data/`: pre-computed plot inputs. All are aggregate.
- `data/restricted/`: participant-level inputs, which are **not** included (see below).

## Running
```bash
pip install -r requirements.txt
jupyter lab Menstrual_CGM.ipynb
```
The Settings cell lists every input and whether it is present. Figures 3 and 6 run from
`data/`. Figure 2, Table 1 and Figures 4 and 5 also need the restricted files.

## Inputs
| file | content |
|---|---|
| `figure_panels.csv` | aggregate |
| `fig3_cgm_trends.csv` | aggregate |
| `fig3_cgm_stats.csv` | aggregate |
| `fig4_hourly_cv.csv` | aggregate |
| `fig4_day_night_cv.csv` | restricted, not in repository |
| `fig5_grids.csv` | aggregate |
| `fig5_deltas.csv` | restricted, not in repository |
| `fig5_paired.csv` | restricted, not in repository |
| `fig6_activity_summary.csv` | aggregate |
| `fig6_activity_curves.csv` | aggregate |
| `fig6_activity_interaction.csv` | aggregate |
| `fig6_covariate_interaction.csv` | aggregate |
| `cohort.csv` | restricted, not in repository |
| `baseline_covariates.csv` | restricted, not in repository |
| `fig4_meals.pkl` | restricted, not in repository |
| `table1.csv` | Table 1 (written by the notebook) |

## Data availability
The raw CGM, diet-logging and clinical data come from the Human Phenotype Project (HPP) and
cannot be shared publicly because of participant privacy. Researchers can request access
through the HPP data-access process.

"""Shared results store for the menstrual-cycle figures.

Every analysis notebook in this folder appends the *already-computed* plotting data
for its panels into a single long-format CSV (`figure_data.csv`). Figure notebooks
(figures_2_6.ipynb) then load that file and replot — no analysis is re-run.

Two kinds of panel data are supported:
  - save_trend(...)        binned mean +/- SEM points + a calibrated spline curve
                           (carbs, exercise probability, metabolites, CGM metrics)
  - save_distribution(...) raw per-subject points + a balance test p-value
                           (age, BMI across the cycle)
"""
import os
import numpy as np
import pandas as pd

FIG_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figure_data.csv')

COLS = ['source', 'metric', 'label', 'series', 'x', 'y', 'sem', 'n',
        'p_fdr', 'p_perm', 'verdict', 'balance_p', 'balance_stat']

# The circular permutation test is run ONLY for FDR-significant metrics. For the rest
# it is not performed and the source notebooks leave P_Spec at its 1.0 placeholder.
FDR_ALPHA = 0.05


def _load_all():
    if os.path.exists(FIG_DATA) and os.path.getsize(FIG_DATA) > 0:
        return pd.read_csv(FIG_DATA)
    return pd.DataFrame(columns=COLS)


def _upsert(rows, source, metrics):
    """Replace any existing rows for (source, metric) then append the new ones."""
    df = _load_all()
    if len(df):
        metrics = [str(m) for m in metrics]
        keep = ~((df['source'] == source) & (df['metric'].astype(str).isin(metrics)))
        df = df[keep]
    out = pd.concat([df, pd.DataFrame(rows, columns=COLS)], ignore_index=True)
    out.to_csv(FIG_DATA, index=False)
    return out


def save_trend(source, metric, label, binned, x_curve, y_curve,
               p_fdr=np.nan, p_perm=np.nan, verdict=''):
    """binned: DataFrame with columns bin, mean, sem, count (already filtered).
    x_curve/y_curve: the calibrated spline curve exactly as plotted in the source."""
    # Permutation is performed only for FDR-significant metrics; otherwise it was not
    # run, so store p_perm as NaN ("not tested") rather than the 1.0 placeholder.
    if pd.isna(p_fdr) or p_fdr >= FDR_ALPHA:
        p_perm = np.nan
    rows = []
    for _, r in binned.iterrows():
        rows.append({'source': source, 'metric': metric, 'label': label, 'series': 'binned',
                     'x': float(r['bin']), 'y': float(r['mean']),
                     'sem': float(r['sem']) if 'sem' in r else np.nan,
                     'n': float(r['count']) if 'count' in r else np.nan,
                     'p_fdr': p_fdr, 'p_perm': p_perm, 'verdict': verdict,
                     'balance_p': np.nan, 'balance_stat': ''})
    for xi, yi in zip(np.asarray(x_curve, float), np.asarray(y_curve, float)):
        rows.append({'source': source, 'metric': metric, 'label': label, 'series': 'spline',
                     'x': float(xi), 'y': float(yi), 'sem': np.nan, 'n': np.nan,
                     'p_fdr': p_fdr, 'p_perm': p_perm, 'verdict': verdict,
                     'balance_p': np.nan, 'balance_stat': ''})
    return _upsert(rows, source, [metric])


def save_distribution(source, metric, label, x, y, balance_p=np.nan, balance_stat=''):
    """x: cycle position per subject; y: value per subject (one row per subject)."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    rows = [{'source': source, 'metric': metric, 'label': label, 'series': 'points',
             'x': float(xx), 'y': float(yy), 'sem': np.nan, 'n': np.nan,
             'p_fdr': np.nan, 'p_perm': np.nan, 'verdict': '',
             'balance_p': balance_p, 'balance_stat': balance_stat}
            for xx, yy in zip(x, y)]
    return _upsert(rows, source, [metric])


def load(source=None, metric=None):
    df = _load_all()
    if source is not None:
        df = df[df['source'] == source]
    if metric is not None:
        df = df[df['metric'].astype(str) == str(metric)]
    return df

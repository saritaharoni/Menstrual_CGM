"""Plotting helpers used by Menstrual_CGM.ipynb."""
import pandas as pd

SUBJ = 'RegistrationCode'

GAUSSIAN_METRICS = ('nadir_dip', 'peak_time', 'baseline_glucose')

MEAL_WINDOWS = {'breakfast': (5, 11), 'lunch': (12, 15), 'dinner': (17, 21)}

def select_meal_time(df, which, first_only=True):
    lo, hi = MEAL_WINDOWS[which]
    h = df['meal_hour'] if 'meal_hour' in df else (
        pd.to_datetime(df['meal_datetime']).dt.hour + pd.to_datetime(df['meal_datetime']).dt.minute / 60.0)
    m = df[(h >= lo) & (h < hi)].copy()
    if which == 'breakfast' and first_only and 'is_first_meal' in m:
        m = m[m['is_first_meal'] == 1]
    return m

def binned_means(meal_df, metric, bin_step=5, min_count=5):
    d = meal_df.dropna(subset=[metric, 'cycle_progression']).copy()
    _m, _s = d[metric].mean(), d[metric].std()
    d = d[d[metric] < _m + 3 * _s]
    if metric in GAUSSIAN_METRICS:
        d = d[d[metric] > _m - 3 * _s]
    if 'bin' not in d:
        d['bin'] = (d['cycle_progression'] / bin_step).round() * bin_step
    subj_bin = d.groupby(['bin', SUBJ])[metric].mean().reset_index()
    g = subj_bin.groupby('bin')[metric].agg(['mean', 'sem', 'count']).reset_index()
    g = g[g['count'] > min_count]
    g['smooth'] = g['mean'].rolling(3, center=True, min_periods=1).mean()
    return g

"""Shared dataframe loaders for regression modules (Q1 2018–Q4 2024 panel)."""
import sys
import os

import numpy as np

_FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures_code')


def load_df18():
    if _FIG not in sys.path:
        sys.path.insert(0, _FIG)
    from _shared import df18  # noqa: E402

    return df18


def yoy_elasticity_df(df18):
    """Year-on-year % changes (4-quarter lag) for price–quantity elasticity spec."""
    d = df18.copy()
    d['YoY_ARPU'] = d['Premium ARPU'].pct_change(4) * 100
    d['YoY_Subs'] = d['Premium MAUs'].pct_change(4) * 100
    return d.dropna(subset=['YoY_ARPU', 'YoY_Subs'])


def loglog_df(df18):
    """ln(Premium MAUs) ~ ln(Premium ARPU) + t; positive values only."""
    d = df18[(df18['Premium MAUs'] > 0) & (df18['Premium ARPU'] > 0)].copy()
    d['ln_mau'] = np.log(d['Premium MAUs'])
    d['ln_arpu'] = np.log(d['Premium ARPU'])
    return d

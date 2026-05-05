"""
figure_07 — Part B: consolidated gross margin — in-sample OLS on time, FY2025-anchored organic path and SMART target.

Uses ``part_b_constants`` anchor GM and ``regression/r02``-style spec on ``_shared.df18``. Saves ``figure_07_gross_margin_trend.png``.
"""

import sys
import os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))

from part_b_constants import GM_CONSOL, TARGET_GM
from _shared import df18, FIGS, SPOTIFY_STYLE, BLUE, PINK, GREEN, DARK
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

plt.rcParams.update(SPOTIFY_STYLE)

fig, ax = plt.subplots(figsize=(9.5, 5.8))

Xc = sm.add_constant(df18['t'])
m_gm = sm.OLS(df18['Gross profit margin'], Xc).fit()
beta1 = float(m_gm.params[1])

# In-sample prediction interval
ci_g_in = m_gm.get_prediction(Xc).conf_int()

ax.scatter(
    df18['Date'],
    df18['Gross profit margin'],
    color=PINK,
    s=36,
    zorder=6,
    alpha=0.88,
    label='Actual GM %',
    edgecolors=DARK,
    linewidths=0.35,
)
ax.plot(
    df18['Date'],
    m_gm.fittedvalues,
    color=BLUE,
    lw=2.2,
    ls='--',
    label=f'OLS in-sample (R²={m_gm.rsquared:.2f})',
)
ax.fill_between(
    df18['Date'],
    ci_g_in[:, 0],
    ci_g_in[:, 1],
    alpha=0.12,
    color=BLUE,
)

# Forecast: quarters strictly after last observation, through Q4 2028
last = pd.Timestamp(df18['Date'].iloc[-1])
start_p = pd.Period(last, freq='Q-DEC') + 1
end_p = pd.Period('2028Q4', freq='Q-DEC')
fc_periods = pd.period_range(start=start_p, end=end_p, freq='Q-DEC')
fc_dates = fc_periods.to_timestamp(how='end')
n_fc = len(fc_dates)
# Level anchor: FY2025 consolidated GM; slope from R2
fc_vals = GM_CONSOL + beta1 * np.arange(n_fc, dtype=float)

ax.plot(
    fc_dates,
    fc_vals,
    color=GREEN,
    lw=2.0,
    ls='--',
    label='Forecast: 32% anchor + same β₁ to Q4 2028',
)
ax.axhline(TARGET_GM, color=PINK, lw=1.4, ls='--', alpha=0.85, zorder=4)
ax.text(
    df18['Date'].iloc[2],
    TARGET_GM + 0.35,
    f'Target GM: {TARGET_GM:.0f}%',
    color=PINK,
    fontsize=9,
    style='italic',
)
ax.axhline(GM_CONSOL, color='#888888', lw=1.0, ls=':', alpha=0.75, zorder=3)
ax.text(
    df18['Date'].iloc[-3],
    GM_CONSOL - 0.55,
    f'FY2025 anchor: {GM_CONSOL:.0f}%',
    fontsize=7.5,
    color='#555555',
)

ax.set_ylabel('Gross Margin (%)')
ax.set_title(
    'Gross margin: OLS trend (Q1 2018–sample end) & FY2025-anchored organic forecast to 2028',
    fontweight='bold',
)
ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.14),
    ncol=2,
    fontsize=8.5,
    frameon=False,
)
ax.grid(True, alpha=0.4)
ax.set_xlim(
    left=df18['Date'].iloc[0] - pd.Timedelta(days=45),
    right=pd.Timestamp('2028-12-31') + pd.Timedelta(days=45),
)

fig.autofmt_xdate()
plt.tight_layout(pad=1.5, rect=[0, 0.12, 1, 1])
plt.savefig(
    f'{FIGS}/figure_07_gross_margin_trend.png',
    dpi=150,
    bbox_inches='tight',
    pad_inches=0.35,
)
plt.close()
print('Saved: figure_07_gross_margin_trend.png')

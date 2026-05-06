"""
figure_14 — Part B: Premium ARPU path — actuals, OLS trend, organic extrapolation and Strategy 3 glidepath to FY2028 blended target.

Uses ``part_b_constants`` anchors. Saves ``figure_13_premium_arpu_path.png``.
"""

import sys, os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))

from part_b_constants import ARPU_FY25, S3_TARGET_ARPU_FY28
from _shared import df18, FIGS, SPOTIFY_STYLE, GREEN, BLUE, PINK
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

plt.rcParams.update(SPOTIFY_STYLE)

fig, ax1 = plt.subplots(1, 1, figsize=(7.2, 6.0))

quarters = pd.date_range('2026-03-31', periods=12, freq='QE')
ARPU_GOAL = float(S3_TARGET_ARPU_FY28)

y_arpu = df18['Premium ARPU'].astype(float)
m_a = sm.OLS(y_arpu, sm.add_constant(df18['t'])).fit()
beta1 = m_a.params[1]
r2 = m_a.rsquared

X_ins = sm.add_constant(df18['t'])
ci_ins = m_a.get_prediction(X_ins).conf_int()

anchor = float(ARPU_FY25)
k_fwd = np.arange(1, len(quarters) + 1, dtype=float)
arpu_organic = anchor + beta1 * k_fwd
organic_start = float(arpu_organic[0])
frac = np.linspace(0, 1, len(quarters)) ** 0.82
arpu_s3 = organic_start + (ARPU_GOAL - organic_start) * (frac / frac[-1])

ax1.plot(df18['Date'], y_arpu, color=PINK, lw=2.0,
         marker='o', ms=3.8, label='Actual Premium ARPU (financials CSV)', zorder=6)
ax1.plot(df18['Date'], m_a.fittedvalues, color=BLUE, lw=1.5, ls='--', alpha=0.85,
         label=f'OLS in-sample (R² = {r2:.2f})')
ax1.fill_between(df18['Date'], ci_ins[:, 0], ci_ins[:, 1], alpha=0.12, color=BLUE, zorder=1)
ax1.plot(
    quarters, arpu_organic, color=GREEN, lw=2.0, ls='--',
    label=f'Organic: FY2025 anchor €{anchor:.2f} + β ({beta1:.4f} €/q)',
)
ax1.plot(quarters, arpu_s3, color=GREEN, lw=2.6, ls='-', label='Strategy 3 path (to FY2028 target)')
ax1.fill_between(quarters, arpu_organic, arpu_s3, alpha=0.18, color=GREEN,
                 label='Uplift vs organic (illustrative)')

ax1.axhline(ARPU_GOAL, color=PINK, lw=1.4, ls='--', alpha=0.85, zorder=2)
ax1.text(quarters[0], ARPU_GOAL + 0.06, f'Target ARPU: €{ARPU_GOAL:.2f}/mo', color=PINK, fontsize=8.5,
         fontweight='bold')
ax1.axvline(df18['Date'].iloc[-1], color='grey', lw=0.8, ls=':', alpha=0.55)
ax1.set_ylabel('Premium ARPU (€/month)')
ax1.set_title(
    '(a) ARPU path — actuals, OLS trend, organic & Strategy 3\n'
    f'(FY2025 anchor €{anchor:.2f}; target €{ARPU_GOAL:.2f} ≈ +10%)',
    fontsize=11,
    fontweight='bold',
)
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=2, fontsize=7.6,
           frameon=True, edgecolor='#CCCCCC')
ax1.grid(True, alpha=0.4)
ymin = min(float(y_arpu.min()), anchor) - 0.35
ymax = max(float(y_arpu.max()), ARPU_GOAL, float(arpu_s3.max())) + 0.4
ax1.set_ylim(ymin, ymax)

ax1.axvspan(quarters[0], quarters[3], alpha=0.06, color=PINK)
ax1.axvspan(quarters[4], quarters[7], alpha=0.06, color=BLUE)
ax1.axvspan(quarters[8], quarters[11], alpha=0.06, color=GREEN)

plt.tight_layout(pad=1.6, rect=[0, 0.08, 1, 1])
plt.savefig(f'{FIGS}/figure_14_premium_arpu_path.png', dpi=150, bbox_inches='tight', pad_inches=0.35)
plt.close()
print('Saved: figure_14_premium_arpu_path.png')

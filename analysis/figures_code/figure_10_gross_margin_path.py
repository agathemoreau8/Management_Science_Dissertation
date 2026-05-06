"""
figure_10 — Part B: gross margin path — actuals, OLS trend, organic extrapolation from FY2025 anchor vs robust scenario band.

Uses ``part_b_constants``. Saves ``figure_11_gross_margin_path.png``.
"""

import sys, os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))

from part_b_constants import GM_CONSOL, TARGET_GM, GM_ROBUST_CONSOL_GM_PCT
from _shared import df18, FIGS, SPOTIFY_STYLE, GREEN, BLUE, PINK
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

plt.rcParams.update(SPOTIFY_STYLE)
fig, ax1 = plt.subplots(1, 1, figsize=(7.2, 6.0))

quarters = pd.date_range('2026-03-31', periods=12, freq='QE')
ROBUST_GM_END = float(GM_ROBUST_CONSOL_GM_PCT)

m_gm = sm.OLS(df18['Gross profit margin'].astype(float), sm.add_constant(df18['t'])).fit()
beta1 = m_gm.params[1]
r2 = m_gm.rsquared

X_ins = sm.add_constant(df18['t'])
ci_ins = m_gm.get_prediction(X_ins).conf_int()

GM_ANCHOR = float(GM_CONSOL)
k_fwd = np.arange(1, len(quarters) + 1, dtype=float)
gm_organic = GM_ANCHOR + beta1 * k_fwd
organic_start = float(gm_organic[0])
frac = np.linspace(0, 1, len(quarters)) ** 0.82
gm_robust = organic_start + (ROBUST_GM_END - organic_start) * (frac / frac[-1])

ax1.plot(df18['Date'], df18['Gross profit margin'].astype(float), color=PINK, lw=2.0,
         marker='o', ms=3.8, label='Actual GM % (financials CSV)', zorder=6)
ax1.plot(df18['Date'], m_gm.fittedvalues, color=BLUE, lw=1.5, ls='--', alpha=0.85,
         label=f'OLS in-sample (R² = {r2:.2f})')
ax1.fill_between(df18['Date'], ci_ins[:, 0], ci_ins[:, 1], alpha=0.12, color=BLUE, zorder=1)
ax1.plot(
    quarters, gm_organic, color=GREEN, lw=2.0, ls='--',
    label=f'Organic: FY2025 anchor {GM_ANCHOR:.0f}% + β ({beta1:.3f} pp/q)',
)
ax1.plot(quarters, gm_robust, color=GREEN, lw=2.6, ls='-', label='Robust combined scenario')
ax1.fill_between(quarters, gm_organic, gm_robust, alpha=0.18, color=GREEN,
                 label='Uplift vs organic (illustrative)')

ax1.axhline(TARGET_GM, color=PINK, lw=1.4, ls='--', alpha=0.85, zorder=2)
ax1.text(quarters[0], TARGET_GM + 0.28, f'Target GM: {TARGET_GM:.0f}%', color=PINK, fontsize=8.5,
         fontweight='bold')
ax1.axvline(df18['Date'].iloc[-1], color='grey', lw=0.8, ls=':', alpha=0.55)
ax1.set_ylabel('Gross margin (%)')
ax1.set_title('(a) GM path — actuals, OLS trend, organic & robust', fontsize=11, fontweight='bold')
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=2, fontsize=7.8,
           frameon=True, edgecolor='#CCCCCC')
ax1.grid(True, alpha=0.4)
ax1.set_ylim(22, max(40, ROBUST_GM_END + 2))

ax1.axvspan(quarters[0], quarters[3], alpha=0.06, color=PINK)
ax1.axvspan(quarters[4], quarters[7], alpha=0.06, color=BLUE)
ax1.axvspan(quarters[8], quarters[11], alpha=0.06, color=GREEN)

plt.tight_layout(pad=1.6, rect=[0, 0.08, 1, 1])
plt.savefig(f'{FIGS}/figure_10_gross_margin_path.png', dpi=150, bbox_inches='tight', pad_inches=0.35)
plt.close()
print('Saved: figure_10_gross_margin_path.png')

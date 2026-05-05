"""
figure_08 — Part B: YoY price elasticity — OLS of YoY Premium subs % on YoY Premium ARPU % (4-quarter changes).

Matches ``regression/r03`` specification on ``_shared.df18``. Saves ``figure_08_price_elasticity_yoy.png``.
"""

import sys, os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))
from _shared import df18, FIGS, SPOTIFY_STYLE, GREEN, BLUE
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import statsmodels.api as sm
import numpy as np

plt.rcParams.update(SPOTIFY_STYLE)
fig = plt.figure(figsize=(9.6, 5.7))
gs = gridspec.GridSpec(1, 2, width_ratios=[3.35, 1.05], wspace=0.08)
ax = fig.add_subplot(gs[0, 0])
ax_right = fig.add_subplot(gs[0, 1])
ax_right.set_axis_off()

# ── Elasticity regression ──────────────────────────────────────────────────
elas = df18[df18['t'] >= 4].copy()
elas['YoY_ARPU'] = df18['Premium ARPU'].pct_change(4) * 100
elas['YoY_Subs'] = df18['Premium MAUs'].pct_change(4) * 100
elas = elas.dropna()
Xe = sm.add_constant(elas['YoY_ARPU'])
m_elas = sm.OLS(elas['YoY_Subs'], Xe).fit()
elasticity = m_elas.params[1]

x_range = np.linspace(elas['YoY_ARPU'].min() - 2, elas['YoY_ARPU'].max() + 2, 50)
Xp = sm.add_constant(x_range)
y_hat = m_elas.params[0] + m_elas.params[1] * x_range
pred_ci = m_elas.get_prediction(Xp).conf_int()

ax.scatter(
    elas['YoY_ARPU'], elas['YoY_Subs'], color=GREEN, s=40, zorder=5,
    alpha=0.8, label='Quarterly obs.',
)
ax.plot(
    x_range, y_hat, color=BLUE, lw=2, ls='--',
    label=f'OLS: ε = {elasticity:.3f} (R²={m_elas.rsquared:.2f})',
)
ax.fill_between(x_range, pred_ci[:, 0], pred_ci[:, 1], alpha=0.12, color=BLUE)
ax.axhline(0, color='grey', lw=0.8, ls=':')
ax.axvline(0, color='grey', lw=0.8, ls=':')
ax.set_xlabel('YoY ARPU Change (%)')
ax.set_ylabel('YoY Subscriber Growth (%)')
ax.set_title(
    f'Price elasticity: YoY Premium ARPU vs subscriber growth\n'
    f'ε ≈ {elasticity:.2f} (near-unit elastic)',
    fontweight='bold',
)
ax.grid(True, alpha=0.4)

handles, labels = ax.get_legend_handles_labels()
ax_right.legend(
    handles,
    labels,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.0),
    fontsize=8.5,
    frameon=True,
    framealpha=0.95,
    edgecolor='#CCCCCC',
)

stats_txt = (
    f'Elasticity ε = {elasticity:.3f}\n'
    f'R² = {m_elas.rsquared:.3f},  p = {m_elas.pvalues[1]:.3f}\n'
    f'Interpretation: 1% ARPU rise\n→ {abs(elasticity):.2f}% fewer new subs\n'
    '(near-unit — segmented approach needed)'
)
ax_right.text(
    0.5,
    0.52,
    stats_txt,
    transform=ax_right.transAxes,
    ha='center',
    va='top',
    fontsize=7.5,
    bbox=dict(boxstyle='round', facecolor='#F0F8F4', edgecolor='#CCCCCC', alpha=0.95),
)

plt.savefig(f'{FIGS}/figure_08_price_elasticity_yoy.png', dpi=150, bbox_inches='tight', pad_inches=0.4)
plt.close()
print('Saved: figure_08_price_elasticity_yoy.png')

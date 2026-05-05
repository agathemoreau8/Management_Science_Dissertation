"""
figure_12 — Part B: paired GM waterfalls — robust partial S1 + S2 base vs primary S1 full + S2 conservative.

Steps from ``part_b_constants``. Saves ``figure_12_gross_margin_waterfalls.png``.
"""

import sys, os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))

from part_b_constants import (
    GM_CONSOL,
    S2_DELTA_GM_BASE_PP,
    S2_DELTA_GM_CONS_PP,
    GM_BRIDGE_S1_PARTIAL_PP,
    GM_BRIDGE_ORGANIC_IMPROV_PP,
    GM_BRIDGE_HEADWIND_ROBUST_PP,
    GM_BRIDGE_ROBUST_DELTA_SUM_PP,
    GM_ROBUST_CONSOL_GM_PCT,
    GM_S1_FULL_GM_PP,
    GM_BRIDGE_HEADWIND_PRIMARY_CONS_PP,
    GM_BRIDGE_PRIMARY_CONS_DELTA_SUM_PP,
    GM_PRIMARY_CONS_CONSOL_GM_PCT,
)
from _shared import FIGS, SPOTIFY_STYLE, GREEN, BLUE, PINK, GOLD, DARK
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(SPOTIFY_STYLE)

WIDTH = 0.62


def draw_waterfall(ax, base, steps, xlabels, end_val, title):
    """Stacked waterfall: first bar = baseline GM, middle = steps, last = total height from 0."""
    bottoms = [0.0]
    heights = [base]
    run = base
    for s in steps:
        bottoms.append(run)
        heights.append(s)
        run += s
    bottoms.append(0.0)
    heights.append(end_val)

    n_bars = len(heights)
    x = np.arange(n_bars, dtype=float)

    for k in range(n_bars):
        h = heights[k]
        b = bottoms[k]
        if k == n_bars - 1:
            ax.bar(x[k], h, bottom=b, color=GREEN, alpha=0.32, edgecolor=DARK, lw=1.4, width=WIDTH)
        elif h < 0:
            ax.bar(x[k], h, bottom=b, color=PINK, alpha=0.9, edgecolor='white', lw=1.0, width=WIDTH)
        elif k == 0:
            ax.bar(x[k], h, bottom=b, color='#888888', alpha=0.9, edgecolor='white', lw=1.0, width=WIDTH)
        else:
            c = [GREEN, BLUE, GOLD][k - 1] if k <= 3 else GREEN
            ax.bar(x[k], h, bottom=b, color=c, alpha=0.88, edgecolor='white', lw=1.0, width=WIDTH)

    for k in range(n_bars):
        h = heights[k]
        b = bottoms[k]
        if k == 0:
            ax.text(x[k], b + h + 0.28, f'{h:.2f}%', ha='center', fontsize=9, fontweight='bold')
        elif k == n_bars - 1:
            ax.text(x[k], h + 0.35, f'{end_val:.1f}%', ha='center', fontsize=9.5, fontweight='bold', color=DARK)
        elif h < 0:
            ymid = b + h / 2
            ax.text(x[k], ymid, f'{h:.2f}pp', ha='center', va='center', fontsize=8.5, fontweight='bold',
                    color='white')
        else:
            ax.text(x[k], b + h + 0.18, f'+{h:.2f}pp', ha='center', fontsize=8.5, fontweight='bold')

    for k in range(n_bars - 2):
        y0 = bottoms[k] + heights[k]
        y1 = bottoms[k + 1]
        ax.plot([x[k] + WIDTH / 2, x[k + 1] - WIDTH / 2], [y0, y1], color='#BBBBBB', lw=0.95, zorder=0)

    y_after_step = bottoms[n_bars - 2] + heights[n_bars - 2]
    ax.plot(
        [x[n_bars - 2] + WIDTH / 2, x[n_bars - 1] - WIDTH / 2],
        [y_after_step, end_val],
        color='#BBBBBB', lw=0.95, ls='--', zorder=0,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels, fontsize=6.75, linespacing=1.05)
    ax.tick_params(axis='x', which='major', length=0, pad=4)
    for lab in ax.get_xticklabels():
        lab.set_ha('center')
        lab.set_va('top')
    ax.set_ylabel('Gross margin (%)')
    ax.set_title(title, fontweight='bold', fontsize=10, pad=10)
    ax.grid(True, alpha=0.35, axis='y')
    ax.set_ylim(30, 40.5)


fig, (axL, axR) = plt.subplots(1, 2, figsize=(15.5, 7.2))

BASE = float(GM_CONSOL)

robust_steps = [
    GM_BRIDGE_S1_PARTIAL_PP,
    S2_DELTA_GM_BASE_PP,
    GM_BRIDGE_ORGANIC_IMPROV_PP,
    GM_BRIDGE_HEADWIND_ROBUST_PP,
]
robust_labels = [
    f'Baseline\n{BASE:.1f}%',
    'S1 partial\n+1.17pp\n50% cov.\n2.5pp Δr',
    f'S2 base mix\n+{S2_DELTA_GM_BASE_PP:.2f}pp\nTable S2-1\n(base case)',
    'Organic\nimprovement\n+1.50pp',
    'Headwind\n−0.08pp',
    f'Robust total\n{GM_ROBUST_CONSOL_GM_PCT:.1f}%',
]
draw_waterfall(
    axL,
    BASE,
    robust_steps,
    robust_labels,
    float(GM_ROBUST_CONSOL_GM_PCT),
    '(b) Robust scenario — GM waterfall\n'
    f'(+1.17 +{S2_DELTA_GM_BASE_PP:.2f} +1.50 −0.08 = +{GM_BRIDGE_ROBUST_DELTA_SUM_PP:.2f}pp vs {BASE:.1f}%)',
)

primary_cons_steps = [
    GM_S1_FULL_GM_PP,
    S2_DELTA_GM_CONS_PP,
    GM_BRIDGE_ORGANIC_IMPROV_PP,
    GM_BRIDGE_HEADWIND_PRIMARY_CONS_PP,
]
primary_labels = [
    f'Baseline\n{BASE:.1f}%',
    f'S1 full deal\n+{GM_S1_FULL_GM_PP:.2f}pp\n100% cov.\n3pp Δr',
    f'S2 conservative\n+{S2_DELTA_GM_CONS_PP:.2f}pp\nmusic −3pp\nvs FY25 mix',
    'Organic\nimprovement\n+1.50pp',
    'Headwind\n−0.08pp',
    f'Scenario total\n{GM_PRIMARY_CONS_CONSOL_GM_PCT:.1f}%',
]
draw_waterfall(
    axR,
    BASE,
    primary_cons_steps,
    primary_labels,
    float(GM_PRIMARY_CONS_CONSOL_GM_PCT),
    '(c) Primary: S1 succeeds + S2 conservative\n'
    f'(+{GM_S1_FULL_GM_PP:.2f} +{S2_DELTA_GM_CONS_PP:.2f} +1.50 −0.08 = '
    f'+{GM_BRIDGE_PRIMARY_CONS_DELTA_SUM_PP:.2f}pp vs {BASE:.1f}%)',
)

plt.subplots_adjust(left=0.055, right=0.995, top=0.86, bottom=0.44, wspace=0.26)
plt.savefig(f'{FIGS}/figure_12_gross_margin_waterfalls.png', dpi=150, bbox_inches='tight', pad_inches=0.6)
plt.close()
print('Saved: figure_12_gross_margin_waterfalls.png')

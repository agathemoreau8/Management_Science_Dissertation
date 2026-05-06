"""
figure_18 — Part B: multi-criteria strategy scorecard heatmap (NPV-scaled row + author judgments).

Uses ``part_b_constants`` NPVs for row scaling. Saves ``figure_14_strategy_scorecard.png``.
"""

import os
import sys

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))

from part_b_constants import NPV_S1, NPV_S2, NPV_S3
from _shared import FIGS, SPOTIFY_STYLE, DARK, GREEN
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(SPOTIFY_STYLE)

criteria = [
    'NPV potential\n(3-yr author model)',
    'Speed to cash /\npayback (1–5)',
    'Low execution risk\n(5 = lowest risk)',
    'Empirical / analytical\nevidence (1–5)',
    'SMART fit\n(Table 1 gap closure)',
]
strategies = [
    'S1 Discovery Mode\n(cost / stream)',
    'S2 Content mix\n(diversification)',
    'S3 Revenue / user\n(tier & ARPU)',
]


def _npv_row_1to5() -> np.ndarray:
    """Map S1/S2/S3 model NPV (€M) to integer scores 3–5 — lowest → 3, highest → 5."""
    v = np.array([float(NPV_S1), float(NPV_S2), float(NPV_S3)], dtype=float)
    lo, hi = float(v.min()), float(v.max())
    if hi <= lo:
        return np.array([4, 4, 4], dtype=float)
    scaled = 3.0 + (v - lo) / (hi - lo) * 2.0
    return np.clip(np.round(scaled), 3, 5)


def _speed_from_payback_months() -> np.ndarray:
    """
    Table 6 (generate_part2_final): ~18 mo S1, ~24 mo S2, ~14 mo S3.
    Shorter payback → higher score on [2, 5].
    """
    payback = np.array([18.0, 24.0, 14.0], dtype=float)
    worst, best = payback.max(), payback.min()
    raw = 2.0 + (worst - payback) / (worst - best) * 3.0
    return np.clip(np.round(raw), 2, 5)


# Row 0: data-anchored; rows 1–4: judgment per Sec. 2–4 / Sec. 6.1 (caption in figure)
M = np.vstack(
    [
        _npv_row_1to5(),
        _speed_from_payback_months(),
        np.array([3.0, 2.0, 4.0], dtype=float),  # S2: upfront invest + longest payback
        np.array([5.0, 3.0, 5.0], dtype=float),  # S1 OLS; S2 CM benchmarks; S3 elasticity + Y23 price shock
        np.array([5.0, 4.0, 5.0], dtype=float),  # S1→GM; S2→mix bridge; S3→€5.09 ARPU
    ]
).astype(float)

fig, ax = plt.subplots(figsize=(9.4, 6.45))
im = ax.imshow(M, cmap='RdYlGn', vmin=1, vmax=5, aspect='auto')
ax.set_xticks(np.arange(3))
ax.set_yticks(np.arange(len(criteria)))
ax.set_xticklabels(strategies, fontsize=8.8)
ax.set_yticklabels(criteria, fontsize=8.8)
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        val = int(M[i, j])
        ax.text(
            j,
            i,
            f'{val}',
            ha='center',
            va='center',
            color=DARK,
            fontsize=11.5,
            fontweight='bold',
        )

ax.set_title(
    'Multi-criteria strategy scorecard (1 = weak, 5 = strong)\n'
    f'NPV row (3–5) from model cashflows (S1 €{NPV_S1 / 1000:.2f}B, S2 €{NPV_S2 / 1000:.2f}B, '
    f'S3 €{NPV_S3 / 1000:.2f}B); speed from ~18 / ~24 / ~14 mo payback; '
    'other rows: author judgment (Sections 2–4, Sec. 6.1)',
    fontweight='bold',
    fontsize=10,
    pad=12,
)
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Score (higher = better)', fontsize=9)
ax.spines[:].set_visible(False)
fig.text(
    0.5,
    0.01,
    'Execution-risk row: 5 = lowest risk. Recommended sequencing S3 → S2 → S1 follows state dependence '
    '(ARPU, then mix, then royalty negotiation).',
    ha='center',
    fontsize=7.5,
    color='#444444',
    style='italic',
)
plt.tight_layout(rect=(0, 0.04, 1, 1))
plt.savefig(f'{FIGS}/figure_18_strategy_scorecard.png', dpi=150, bbox_inches='tight', pad_inches=0.38)
plt.close()
print('Saved: figure_18_strategy_scorecard.png')

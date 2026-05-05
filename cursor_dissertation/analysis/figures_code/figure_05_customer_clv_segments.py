"""
figure_05 — Part A: segment mix donut, illustrative CLV by tier and FY2024-style revenue bars.

Uses fixed segment inputs documented in-code (plan mix / GM / churn). Saves ``figure_05_customer_clv_segments.png``.
"""

import sys, os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))
from _shared import FIGS, SPOTIFY_STYLE, GREEN, BLUE, PINK, GOLD, DARK
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(SPOTIFY_STYLE)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18.5, 5.8))

GM_FREE = 0.12
GM_PREMIUM = 0.33
WACC = 0.08
C_MONTHLY = 0.039   # Elad, 2025 — as in Section 6.2


def clv_monthly(arpu_eur: float, gm: float) -> float:
    i = WACC / 12
    return (arpu_eur * gm) / (C_MONTHLY + i)

# Order: Free, Individual, Duo, Family, Student
labels_short = ['Free\n(Ad-sup.)', 'Individual', 'Duo', 'Family', 'Student']
labels_rev   = [
    'Free\n(429.6M MAU)',
    'Individual\n(154.6M)',
    'Duo\n(4.9M)',
    'Family\n(58.9M)',
    'Student\n(27.0M)',
]
# Free MAU = 675M total Q4 headline minus 245.4M premium subs (tier counts); ad ARPU from 425M × 12
users_m = [429.6, 154.6, 4.9, 58.9, 27.0]
arpu_mo = [0.36, 5.83, 4.04, 2.47, 3.14]
rev_bn  = [1.854, 10.81, 0.24, 1.74, 1.02]
clv_vals = [clv_monthly(arpu_mo[0], GM_FREE)] + [
    clv_monthly(a, GM_PREMIUM) for a in arpu_mo[1:]
]

colors = [GOLD + 'DD', GREEN + 'DD', '#2E86AB', BLUE + 'DD', PINK + 'DD']

# ══ (a) Segmentation donut ════════════════════════════════════════════════
wedges, _, autotexts = ax1.pie(
    users_m, labels=None, colors=colors, autopct='%1.1f%%',
    startangle=128, wedgeprops={'linewidth': 1.5, 'edgecolor': 'white'},
    pctdistance=0.72, textprops={'fontsize': 7.8}
)
for at in autotexts:
    at.set_fontweight('bold')
ax1.legend(labels_short, loc='lower center', ncol=3, fontsize=7.6,
           bbox_to_anchor=(0.5, -0.22))
centre = plt.Circle((0, 0), 0.52, color='white')
ax1.add_artist(centre)
ax1.text(0, 0.09, '675M', ha='center', va='center', fontsize=15, fontweight='bold', color=DARK)
ax1.text(0, -0.15, 'MAUs', ha='center', va='center', fontsize=8.5, color='grey')
ax1.set_title('(a) User Mix by Segment (Q4 2024)', fontweight='bold')

# ══ (b) CLV by segment ════════════════════════════════════════════════════
x = np.arange(len(labels_short))
bars2 = ax2.bar(x, clv_vals, color=colors, alpha=0.9, width=0.62)
ax2.set_xticks(x)
ax2.set_xticklabels(labels_short, fontsize=8.2)
ax2.set_ylabel('Estimated CLV (€)')
ax2.set_title('(b) CLV by Segment (GM 12% free, 33% Premium; c 3.9%/mo; WACC 8%)',
              fontweight='bold')
ymax = max(clv_vals) * 1.12
ax2.set_ylim(0, ymax)
for bar, val in zip(bars2, clv_vals):
    lbl = f'€{val:.2f}' if val < 10 else f'€{val:.1f}'
    ax2.text(bar.get_x() + bar.get_width() / 2, val + ymax * 0.015, lbl,
             ha='center', fontsize=9, fontweight='bold')
ax2.grid(True, alpha=0.35, axis='y')

# ══ (c) Annual revenue ════════════════════════════════════════════════════
bars3 = ax3.bar(x, rev_bn, color=colors, alpha=0.9, width=0.62)
ax3.set_xticks(x)
ax3.set_xticklabels(labels_rev, fontsize=7.6)
ax3.set_ylabel('FY2024 revenue (€ billion)')
ax3.set_title('(c) Annual Revenue by Segment', fontweight='bold')
rymax = max(rev_bn) * 1.2
ax3.set_ylim(0, rymax)
for bar, val in zip(bars3, rev_bn):
    ax3.text(bar.get_x() + bar.get_width() / 2, val + rymax * 0.015, f'€{val:.2f}B',
             ha='center', fontsize=8.5, fontweight='bold')
prem = sum(rev_bn[1:])
ax3.axhline(prem, color='#333333', lw=1.0, ls=':', alpha=0.65)
ax3.text(len(x) - 0.45, prem + rymax * 0.025, f'Premium Σ ≈ €{prem:.2f}B',
         fontsize=7.8, color='#333333', ha='right')
ax3.grid(True, alpha=0.35, axis='y')

fig.suptitle('Freemium Segments: Scale, CLV (Illustrative) & FY2024 Revenue',
             fontweight='bold', y=1.01)
plt.tight_layout(pad=1.75)
plt.savefig(f'{FIGS}/figure_05_customer_clv_segments.png', dpi=150, bbox_inches='tight', pad_inches=0.35)
plt.close()
print('Saved: figure_05_customer_clv_segments.png')

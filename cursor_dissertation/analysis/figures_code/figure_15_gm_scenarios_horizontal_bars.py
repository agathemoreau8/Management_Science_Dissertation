"""
figure_15 — Part B: FY2028 consolidated GM scenarios vs 37% target (horizontal bars).

Saves ``figure_15_gm_scenarios_horizontal_bars.png``.
"""

import os
import sys

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))
from _shared import FIGS, SPOTIFY_STYLE, GREEN, PINK, DARK, GOLD
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(SPOTIFY_STYLE)

# Table 10 — FY2028 GM % (short labels)
SCENARIOS = [
    ('Stress B\nS1=0;\nS2 cons.', 34.8, False),
    ('Stress A\nS1=0;\nS2 base', 36.6, False),
    ('Fallback\nS1 weak;\nS2 base', 37.0, True),
    ('Primary\nS1 full;\nS2 cons.', 37.5, True),
    ('Robust\nS1 partial;\nS2 base', 37.6, True),
    ('Best\nboth succeed', 39.2, True),
]
TARGET_GM = 37.0

labels = [t[0] for t in SCENARIOS]
values = [t[1] for t in SCENARIOS]
meets = [t[2] for t in SCENARIOS]
colors = [GREEN if m else PINK for m in meets]

fig, ax = plt.subplots(figsize=(9.2, 5.8))
y = np.arange(len(labels))
ax.barh(y, values, color=colors, alpha=0.88, edgecolor='white', height=0.62)
ax.axvline(TARGET_GM, color=GOLD, ls='--', lw=2.2, label=f'SMART GM target {TARGET_GM:.0f}%')
for yi, v in zip(y, values):
    ax.text(v + 0.15, yi, f'{v:.1f}%', va='center', fontsize=9.5, fontweight='bold', color=DARK)

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=8.5)
ax.set_xlabel('Consolidated gross margin FY2028 (%)')
ax.set_title(
    'Figure B19 — GM scenario ladder vs 37% target\n'
    '(same cases as Table 10; green = meets target)',
    fontweight='bold',
    fontsize=10.5,
    pad=12,
)
ax.set_xlim(33, 40.5)
ax.legend(loc='lower right', fontsize=8.5)
ax.grid(True, axis='x', alpha=0.35)
plt.tight_layout()
plt.savefig(f'{FIGS}/figure_15_gm_scenarios_horizontal_bars.png', dpi=150, bbox_inches='tight', pad_inches=0.35)
plt.close()
print('Saved: figure_15_gm_scenarios_horizontal_bars.png')

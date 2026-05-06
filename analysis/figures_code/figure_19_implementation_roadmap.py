"""
figure_19 — Part B: illustrative Gantt-style roadmap (S3 → S2 → S1 sequencing).

Saves ``figure_10_implementation_roadmap.png``.
"""

import sys, os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))
from _shared import FIGS, SPOTIFY_STYLE, GREEN, BLUE, PINK, GOLD, DARK
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams.update(SPOTIFY_STYLE)
fig, ax = plt.subplots(figsize=(12, 5.2))

# (y, start_month, duration_months, color, label)
tasks = [
    (4, 0, 12, PINK, 'S3: Supremium & geo repricing'),
    (3, 6, 18, BLUE, 'S2: Podcast/audio investment'),
    (2, 12, 24, GREEN, 'S1: Discovery Mode scale-up'),
    (1, 0, 36, GOLD, 'Cross-cutting: KPI reviews & churn programme'),
]
for y, start, dur, col, _ in tasks:
    ax.barh(y, dur, left=start, height=0.55, color=col, alpha=0.85,
            edgecolor='white', lw=1.2)

ax.set_yticks([1, 2, 3, 4])
ax.set_yticklabels(['Portfolio', 'S1 late', 'S2 mid', 'S3 early'], fontsize=9)
ax.set_xlabel('Month from FY2026 start (0 = Jan 2026)')
ax.set_xlim(0, 38)
ax.set_title('Illustrative Sequenced Roadmap: S3 → S2 → S1\n'
             '(overlapping workstreams with review gates)', fontweight='bold')
ax.grid(True, alpha=0.35, axis='x')

# Legend — unique labels only
handles = [
    mpatches.Patch(color=PINK, label='S3 Revenue / User (Months 0–12 core)'),
    mpatches.Patch(color=BLUE, label='S2 Content mix (from M6)'),
    mpatches.Patch(color=GREEN, label='S1 Cost / stream (from M12)'),
    mpatches.Patch(color=GOLD, label='Portfolio monitoring (ongoing)'),
]
ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=2, fontsize=8)

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.savefig(f'{FIGS}/figure_19_implementation_roadmap.png', dpi=150, bbox_inches='tight', pad_inches=0.35)
plt.close()
print('Saved: figure_19_implementation_roadmap.png')

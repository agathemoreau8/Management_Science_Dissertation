"""
figure_16 — Part B: Strategy 3 adoption sensitivity — net blended Premium ARPU uplift vs +10% hurdle.

Uses Table 16 series at base downgrade rate d = 5%. Saves ``figure_16_s3_adoption_net_arpu.png``.
"""

import os
import sys

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))
from _shared import FIGS, SPOTIFY_STYLE, GREEN, GOLD, DARK, BLUE
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(SPOTIFY_STYLE)

# Table 16 — adoption band 15–19%, d = 5%
ADOPT_PCT = np.array([15, 16, 17, 18, 19])
NET_UPLIFT = np.array([0.419, 0.451, 0.483, 0.515, 0.547])
THRESH = 0.463
# first YES at 17% per §4.5 narrative + Table 16

fig, ax = plt.subplots(figsize=(7.8, 5.0))
ax.plot(
    ADOPT_PCT,
    NET_UPLIFT,
    'o-',
    color=GREEN,
    lw=2.4,
    markersize=9,
    markeredgecolor='white',
    markeredgewidth=1.2,
    label='Net ARPU uplift (€/mo)',
)
ax.axhline(THRESH, color=GOLD, ls='--', lw=2, label=f'Table 16 threshold +€{THRESH:.3f}/mo')
ax.axvline(17, color=BLUE, ls=':', lw=1.8, alpha=0.85, label='17%: first “YES” row')

for a, u in zip(ADOPT_PCT, NET_UPLIFT):
    ax.text(a, u + 0.012, f'+€{u:.2f}', ha='center', fontsize=8.5, color=DARK)

ax.set_xlabel('Supremium adoption (% of Individual base)')
ax.set_ylabel('Net blended Premium ARPU uplift (€/month)')
ax.set_title(
    'Figure B21 — S3 adoption sensitivity (d = 5%)\n'
    'Source: Table 16; §4.5 notes threshold first met at 17% (31.1M upgraders)',
    fontweight='bold',
    fontsize=10,
    pad=11,
)
ax.set_xticks(ADOPT_PCT)
ax.set_ylim(0.38, 0.58)
ax.legend(loc='lower right', fontsize=8.5)
ax.grid(True, alpha=0.35)
plt.tight_layout()
plt.savefig(f'{FIGS}/figure_16_s3_adoption_net_arpu.png', dpi=150, bbox_inches='tight', pad_inches=0.32)
plt.close()
print('Saved: figure_16_s3_adoption_net_arpu.png')

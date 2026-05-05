"""
figure_03 — Part A: Porter five forces radar for streaming — Spotify vs ecosystem rivals (author-scored 1–5).

Saves ``figure_03_porters_five_forces.png``.
"""

import sys, os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))
from _shared import FIGS, SPOTIFY_STYLE, GREEN, BLUE, PINK, DARK
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(SPOTIFY_STYLE)

categories = [
    'Threat of\nNew Entrants',
    'Bargaining Power\nof Suppliers',
    'Bargaining Power\nof Buyers',
    'Threat of\nSubstitutes',
    'Industry\nRivalry',
]

# Scores are on a 1–5 scale (higher = stronger competitive pressure on Spotify).
spotify_scores = [1.5, 5.0, 4.2, 4.6, 4.8]
ecosystem_scores = [2.4, 3.6, 2.6, 3.4, 4.0]

angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]
spotify_plot = spotify_scores + spotify_scores[:1]
ecosystem_plot = ecosystem_scores + ecosystem_scores[:1]

fig = plt.figure(figsize=(14.2, 8.2))
fig.patch.set_facecolor('white')
ax = plt.subplot(111, polar=True)
ax.set_facecolor('#FBFBFB')
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=10.5, color=DARK)
ax.set_ylim(0, 5)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=9, color='#666666')
ax.yaxis.grid(True, linestyle='--', linewidth=1.0, color='#C9CED6')
ax.xaxis.grid(True, linestyle='-', linewidth=0.9, color='#D5D9DF')
ax.spines['polar'].set_color('#C9CED6')
ax.spines['polar'].set_linewidth(1.0)

# risk-zone rings to make pressure obvious
theta_full = np.linspace(0, 2*np.pi, 360)
ax.fill_between(theta_full, 4.0, 5.0, color='#FDEBEC', alpha=0.45, zorder=0)
ax.fill_between(theta_full, 3.0, 4.0, color='#FFF7E8', alpha=0.35, zorder=0)
ax.fill_between(theta_full, 0.0, 3.0, color='#EEF9F1', alpha=0.30, zorder=0)

ax.plot(angles, spotify_plot, color=PINK, linewidth=2.8, label='Spotify pressure profile')
ax.fill(angles, spotify_plot, color=PINK, alpha=0.20)
ax.scatter(angles[:-1], spotify_scores, color=PINK, s=44, zorder=5)

ax.plot(angles, ecosystem_plot, color=BLUE, linewidth=2.0, linestyle='--',
        label='Ecosystem rivals (reference)')
ax.fill(angles, ecosystem_plot, color=BLUE, alpha=0.10)
ax.scatter(angles[:-1], ecosystem_scores, color=BLUE, s=36, zorder=5)

ax.set_title("Porter's Five Forces — Pressure on Spotify",
             fontsize=13.5, fontweight='bold', color=DARK, pad=16)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.16), ncol=2,
          frameon=True, edgecolor='#D0D5DC', fontsize=10)

# Competitor context annotations
note_color = '#4F5561'
ax.text(np.deg2rad(54), 5.55, 'Suppliers: UMG, Sony, Warner',
        ha='center', va='center', fontsize=9.2, color=note_color)
ax.text(np.deg2rad(126), 5.45, 'Buyers compare with Apple Music,\nYouTube Music, Amazon Music',
        ha='center', va='center', fontsize=9.0, color=note_color)
ax.text(np.deg2rad(234), 5.42, 'Substitutes: TikTok, YouTube,\nAudible, podcasts',
        ha='center', va='center', fontsize=9.0, color=note_color)

fig.text(
    0.5, 0.05,
    'Scores are author assessments on a 1–5 scale using Spotify (2024), Bernstein Research (2023), and IFPI (2024). '
    'Spotify faces stronger supplier power, buyer pressure, substitutes, and rivalry than ecosystem-backed rivals because '
    'Apple, Amazon, and YouTube can subsidise streaming through broader platforms. '
    'Limitation: Porter’s framework assumes force independence, which is weaker in two-sided platforms.',
    ha='center', va='center', fontsize=8.5, color='#6A6F78'
)

# concise risk cues
fig.text(0.86, 0.88, 'Outer ring = higher\nthreat pressure',
         fontsize=9, color='#60656E', ha='right')

plt.tight_layout(rect=[0, 0.12, 1, 0.96], pad=1.1)
plt.savefig(f'{FIGS}/figure_03_porters_five_forces.png', dpi=150, bbox_inches='tight', pad_inches=0.30)
plt.close()
print('Saved: figure_03_porters_five_forces.png')

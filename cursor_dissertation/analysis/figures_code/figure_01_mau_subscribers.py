"""
figure_01 — Part A: MAUs and Premium subscribers over time plus Premium conversion rate.

Uses quarterly panel from ``_shared.df18`` (Q1 2018–Q4 2024). Saves ``figure_01_mau_subscribers.png``.
"""

import sys, os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))
from _shared import df18, FIGS, SPOTIFY_STYLE, GREEN, BLUE, GOLD, PINK, DARK
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rcParams.update(SPOTIFY_STYLE)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# a) MAU & Premium subscribers
ax1.fill_between(df18['Date'], df18['MAUs'], alpha=0.18, color=GOLD, label='_nolegend_')
ax1.plot(df18['Date'], df18['MAUs'], color=GOLD, lw=2.2, marker='o', ms=3.5, label='Total MAUs')
ax1.fill_between(df18['Date'], df18['Premium MAUs'], alpha=0.25, color=GREEN)
ax1.plot(df18['Date'], df18['Premium MAUs'], color=GREEN, lw=2.2, marker='o', ms=3.5, label='Premium Subscribers')
ax1.set_title('(a) MAU & Premium Subscriber Growth', fontweight='bold')
ax1.set_ylabel('Users (millions)')
ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.0f}M'))
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2,
           fontsize=9, frameon=True, edgecolor='#CCCCCC')
ax1.grid(True, alpha=0.5)
ax1.annotate('675M MAUs\nQ4 2024', xy=(df18['Date'].iloc[-1], df18['MAUs'].iloc[-1]),
             xytext=(-60, -50), textcoords='offset points', fontsize=8.5,
             arrowprops=dict(arrowstyle='->', color=GOLD), color=GOLD, fontweight='bold')
ax1.annotate('263M Premium\nQ4 2024', xy=(df18['Date'].iloc[-1], df18['Premium MAUs'].iloc[-1]),
             xytext=(-75, -35), textcoords='offset points', fontsize=8.5,
             arrowprops=dict(arrowstyle='->', color=GREEN), color=GREEN, fontweight='bold')

# b) Conversion rate
ax2.plot(df18['Date'], df18['Conversion'], color=BLUE, lw=2.2, marker='o', ms=3.5)
ax2.fill_between(df18['Date'], df18['Conversion'], alpha=0.15, color=BLUE)
ax2.axhline(39.0, color=PINK, lw=1.5, ls='--', alpha=0.7)
ax2.text(df18['Date'].iloc[5], 39.6, '~39% ceiling', color=PINK, fontsize=8.5, style='italic')
ax2.set_title('(b) Premium Conversion Rate (%)', fontweight='bold')
ax2.set_ylabel('Premium / MAU (%)')
ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.0f}%'))
ax2.grid(True, alpha=0.5)
ax2.set_ylim(29, 47)

plt.tight_layout(pad=1.8, rect=[0, 0.15, 1, 1])
plt.savefig(f'{FIGS}/figure_01_mau_subscribers.png', dpi=150, bbox_inches='tight', pad_inches=0.35)
plt.close()
print('Saved: figure_01_mau_subscribers.png')

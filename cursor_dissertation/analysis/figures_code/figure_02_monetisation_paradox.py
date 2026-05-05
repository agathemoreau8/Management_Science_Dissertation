"""
figure_02 — Part A: monetisation paradox — MAUs, Premium subs, revenue and ARPU indexed to Q1 2018 = 100.

Shows flat ARPU versus scaled users. Saves ``figure_02_monetisation_paradox.png``.
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
fig, ax = plt.subplots(figsize=(11, 6))

# Calculate indices because data includes different units
base = df18.iloc[0]
mau_idx    = df18['MAUs']          / base['MAUs']          * 100
rev_idx    = df18['Total Revenue'] / base['Total Revenue'] * 100
arpu_idx   = df18['Premium ARPU']  / base['Premium ARPU']  * 100
prem_idx   = df18['Premium MAUs']  / base['Premium MAUs']  * 100

# Plot data
ax.plot(df18['Date'], mau_idx,  color=GOLD,  lw=2.5, marker='o', ms=3, label='Total MAUs')
ax.plot(df18['Date'], prem_idx, color=GREEN, lw=2.5, marker='s', ms=3, label='Premium Subscribers')
ax.plot(df18['Date'], rev_idx,  color=BLUE,  lw=2.5, marker='^', ms=3, label='Total Revenue')
ax.plot(df18['Date'], arpu_idx, color=PINK,  lw=2.5, marker='D', ms=3, label='Premium ARPU')

ax.axhline(100, color='grey', lw=0.8, ls='--', alpha=0.5)

# Annotations at end
last = df18.iloc[-1]
for val, col, lbl, dy in [
    (mau_idx.iloc[-1],  GOLD,  f'{mau_idx.iloc[-1]:.0f}', 4),
    (prem_idx.iloc[-1], GREEN, f'{prem_idx.iloc[-1]:.0f}', -12),
    (rev_idx.iloc[-1],  BLUE,  f'{rev_idx.iloc[-1]:.0f}', 4),
    (arpu_idx.iloc[-1], PINK,  f'{arpu_idx.iloc[-1]:.0f}', -12),
]:
    ax.annotate(f'{val:.0f}', xy=(last['Date'], val),
                xytext=(8, dy), textcoords='offset points',
                fontsize=9, fontweight='bold', color=col)

ax.set_ylabel('Index (Q1 2018 = 100)')
ax.set_title('The Monetisation Paradox: Indexed Growth Comparison\n'
             'Q1 2018 = 100 baseline. ARPU virtually flat despite 3× user growth.',
             fontweight='bold')
ax.legend(fontsize=9.5, loc='upper left')
ax.grid(True, alpha=0.4)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.0f}'))

plt.tight_layout(pad=1.8)
plt.savefig(f'{FIGS}/figure_02_monetisation_paradox.png', dpi=150, bbox_inches='tight', pad_inches=0.35)
plt.close()
print('Saved: figure_02_monetisation_paradox.png')

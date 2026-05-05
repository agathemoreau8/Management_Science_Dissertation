"""
figure_04 — Part A: competitor benchmarking — ARPU, subscribers and monetisation gap vs scale.

Reads ``competitor_stats_2025.xlsx`` from ``analysis/`` or ``data/``.
Saves ``figure_04_competitor_benchmarking.png``.
"""

import sys, os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))
from _shared import FIGS, SPOTIFY_STYLE, GREEN, PINK, GOLD
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams.update(SPOTIFY_STYLE)

# Load benchmark inputs from the user-maintained Excel workbook
_REPO = os.path.normpath(os.path.join(_FCDIR, '..', '..'))
for _xlsx in (
    os.path.join(_FCDIR, '..', 'competitor_stats_2025.xlsx'),
    os.path.join(_REPO, 'data', 'competitor_stats_2025.xlsx'),
):
    if os.path.isfile(_xlsx):
        XLSX = _xlsx
        break
else:
    print('SKIP figure_04: missing workbook (expected one of):')
    print(f'  {os.path.join(_FCDIR, "..", "competitor_stats_2025.xlsx")}')
    print(f'  {os.path.join(_REPO, "data", "competitor_stats_2025.xlsx")}')
    print('  Sheet required: ARPU_Calculations.')
    sys.exit(0)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5.6))

bench = pd.read_excel(XLSX, sheet_name='ARPU_Calculations')
bench = bench[bench['Platform'] != 'TOTAL / WEIGHTED'].copy()

# pandas does not evaluate Excel formulas; mirror workbook logic:
# use FY2024 reported Premium ARPU when supplied (Spotify), else revenue / subs.
rep_col = 'ARPU_Reported_FY24 (input)'
rev_col = 'Revenue_Bn (input)'
sub_col = 'Subscribers_M (input)'

def _monthly_arpu(row) -> float:
    if rep_col in row.index and pd.notna(row[rep_col]):
        return float(row[rep_col])
    return float(row[rev_col]) * 1000.0 / (float(row[sub_col]) * 12.0)

arpu = [_monthly_arpu(row) for _, row in bench.iterrows()]

platforms_raw = bench['Platform'].tolist()
platforms = [p.replace(' ', '\n') if p in ['Apple Music', 'YouTube Premium/Music', 'Tencent Music', 'Amazon Music'] else p for p in platforms_raw]
subs_m = bench['Subscribers_M (input)'].astype(float).tolist()
rev_bn = bench['Revenue_Bn (input)'].astype(float).tolist()
total_rev = sum(rev_bn)
total_subs = sum(subs_m)
rev_share = [(v / total_rev) * 100 for v in rev_bn]
sub_share = [(v / total_subs) * 100 for v in subs_m]
monet_gap = [r - s for r, s in zip(rev_share, sub_share)]  # + means monetizes above scale share

color_map = {
    'Spotify': GREEN,
    'Apple Music': '#999999',
    'Tencent Music': '#A238FF',
    'Amazon Music': GOLD,
    'YouTube Premium/Music': PINK,
}
colors = [color_map.get(p, '#666666') for p in platforms_raw]
x = np.arange(len(platforms))

# ── (a) ARPU comparison ────────────────────────────────────────────────────
bars = ax1.bar(x, arpu, color=colors, alpha=0.85, width=0.62)
ax1.set_xticks(x); ax1.set_xticklabels(platforms, fontsize=8.2)
ax1.set_ylabel('Monthly ARPU (€/month)')
ax1.set_title('(a) Monthly ARPU by Platform', fontweight='bold')
for bar, val in zip(bars, arpu):
    ax1.text(bar.get_x()+bar.get_width()/2, val+0.1, f'€{val:.2f}',
             ha='center', fontsize=9.5, fontweight='bold')
# Dissertation target: +20% on FY2024 reported Spotify Premium ARPU (€4.69).
target_arpu = 4.69 * 1.20
ax1.axhline(target_arpu, color=GREEN, lw=1.5, ls='--', alpha=0.8)
ax1.text(len(platforms)-0.05, target_arpu + 0.24, f'Target ARPU: €{target_arpu:.2f} (+20%)',
         color='#0E7A35', fontsize=9.2, fontweight='bold',
         ha='right', va='bottom',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#B7DEC7', alpha=0.95))
ax1.set_ylim(0, 12)
ax1.grid(True, alpha=0.4, axis='y')

# ── (b) Subscriber base ─────────────────────────────────────────────────────
bars2 = ax2.bar(x, subs_m, color=colors, alpha=0.85, width=0.62)
ax2.set_xticks(x); ax2.set_xticklabels(platforms, fontsize=8.2)
ax2.set_ylabel('Subscribers (Millions)')
ax2.set_title('(b) Subscriber Base by Platform', fontweight='bold')
for bar, v in zip(bars2, subs_m):
    ax2.text(bar.get_x()+bar.get_width()/2, v + max(subs_m)*0.018, f'{v:.0f}M',
             ha='center', fontsize=9, fontweight='bold')
ax2.grid(True, alpha=0.4, axis='y')

# ── (c) Monetization gap ────────────────────────────────────────────────────
bars3 = ax3.bar(x, monet_gap, color=colors, alpha=0.85, width=0.62)
ax3.set_xticks(x); ax3.set_xticklabels(platforms, fontsize=8.2)
ax3.set_ylabel('Revenue Share - Subscriber Share (pp)')
ax3.set_title('(c) Monetization Gap vs Scale', fontweight='bold')
for bar, v in zip(bars3, monet_gap):
    y = v + 0.35 if v >= 0 else v - 0.65
    va = 'bottom' if v >= 0 else 'top'
    ax3.text(bar.get_x()+bar.get_width()/2, y, f'{v:+.1f}pp',
             ha='center', va=va, fontsize=9, fontweight='bold')
ax3.axhline(0, color='#444444', lw=1.0, ls='--', alpha=0.8)
ax3.grid(True, alpha=0.4, axis='y')

fig.suptitle('Competitor Benchmarking: ARPU, Subscriber Scale & Revenue Efficiency',
             fontweight='bold', y=1.02)
plt.tight_layout(pad=1.8)
plt.savefig(f'{FIGS}/figure_04_competitor_benchmarking.png', dpi=150, bbox_inches='tight', pad_inches=0.35)
plt.close()
print('Saved: figure_04_competitor_benchmarking.png')

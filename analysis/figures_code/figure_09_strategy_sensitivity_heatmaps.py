"""
figure_09 — Part B: three-panel sensitivity heatmaps for Strategies 1–3 (CVP coverage × royalty relief; CM mix grid; Supremium adoption × downgrade).

Uses ``part_b_constants`` for FY2025 scales and S3 parameters. Saves ``figure_09_strategy_sensitivity_heatmaps.png``.
"""

import sys, os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))
from part_b_constants import (
    N_PREM,
    ARPU_FY25,
    REV_PREM,
    REV_TOTAL,
    S2_BLENDED_CM_FY25,
    S2_CM_MUSIC_PCT,
    S2_CM_PODCAST_PCT,
    S2_CM_AUDIOBOOK_PCT,
    S2_SHARE_MUSIC_FY25,
    S3_INDIVIDUAL_SHARE_PREM,
    S3_DELTA_P_SUPREMIUM_EUR,
    S3_DELTA_P_DOWNGRADE_EUR,
)
from _shared import FIGS, SPOTIFY_STYLE, GREEN, BLUE, PINK, GOLD
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(SPOTIFY_STYLE)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5.5))

# ── S1: Royalty reduction × effective relief coverage ──────────────────────
royalty_pp = np.array([1.0, 1.5, 2.0, 2.5, 3.0])  # Δr_eff grid (pp); §2.2 / Table 3 (1–5pp sensitivity; plotted to 3pp base)
adoption   = np.array([10, 25, 30, 50, 75, 100])  # Effective coverage %; includes 100% for §2.2 headline; 25–30 / 75–100 for narrative bands
R, A = np.meshgrid(royalty_pp, adoption)
_n_s1_y = len(adoption)
# Annual premium € flow as in §2.2 CVP (N×ARPU×12), not REV_PREM alone — matches €483M / +2.8pp headline
PREM_VOL_CVP = N_PREM * ARPU_FY25 * 12          # €M; part_b_constants N_PREM, ARPU_FY25
# ΔGM(pp) = ΔGP/REV_TOTAL×100 with ΔGP = N×ARPU×12×(R/100)×(A/100)
gm_s1 = (R / 100) * (A / 100) * (PREM_VOL_CVP / REV_TOTAL) * 100

im1 = ax1.imshow(gm_s1, cmap='YlGn', aspect='auto', vmin=0, vmax=gm_s1.max(), zorder=1)
ax1.set_xticks(range(5)); ax1.set_xticklabels([f'{x:.1f}pp' for x in royalty_pp], fontsize=8)
ax1.set_yticks(range(_n_s1_y)); ax1.set_yticklabels([f'{y}%' for y in adoption], fontsize=8)
ax1.set_xlabel('Royalty Rate Reduction', fontsize=9)
ax1.set_ylabel('Effective Relief Coverage %\n(organic opt-in ≈ 25–30%; portfolio deal ≈ 75–100%)', fontsize=8)
ax1.set_title('S1 — GM Impact (pp)\nRoyalty reduction × effective relief coverage', fontweight='bold', fontsize=9)
for i in range(_n_s1_y):
    for j in range(5):
        ax1.text(j, i, f'{gm_s1[i,j]:.2f}pp', ha='center', va='center', fontsize=8.5, fontweight='bold',
                 color='black' if gm_s1[i,j] < gm_s1.max()*0.7 else 'white', zorder=2)
# Organic opt-in ceiling band (rows at 25% and 30% coverage)
ax1.axhspan(0.5, 2.5, color='yellow', alpha=0.08, zorder=0)
ax1.text(-0.45, 1.5, 'organic\nceiling', color='#888800', fontsize=6.5, va='center', ha='left', style='italic', zorder=2)

# Portfolio deal range band (rows 4-5, covering 75-100%)
ax1.axhspan(3.5, 5.5, color='green', alpha=0.08, zorder=0)
ax1.text(-0.45, 4.5, 'portfolio\ndeal', color='darkgreen', fontsize=6.5, va='center', ha='left', style='italic', zorder=2)
plt.colorbar(im1, ax=ax1, label='GM improvement (pp)', shrink=0.85)

# ── S2: CM mix model — Δmusic × FY2028 podcast share (audiobook = residual) ──
shift_pct = np.array([3, 5, 7, 9, 11], dtype=float)
pod_share = np.array([14, 15, 16, 17, 19], dtype=float)
_n2y, _n2x = len(pod_share), len(shift_pct)
gm_s2 = np.zeros((_n2y, _n2x))
for i, sp_28 in enumerate(pod_share):
    for j, dm in enumerate(shift_pct):
        sm_28 = float(S2_SHARE_MUSIC_FY25) - dm
        sa_28 = 100.0 - sm_28 - sp_28
        if sa_28 < 0 or sm_28 < 0 or sp_28 < 0:
            gm_s2[i, j] = np.nan
            continue
        blended_28 = (
            sm_28 * S2_CM_MUSIC_PCT
            + sp_28 * S2_CM_PODCAST_PCT
            + sa_28 * S2_CM_AUDIOBOOK_PCT
        ) / 100.0
        delta_cm = blended_28 - S2_BLENDED_CM_FY25
        gm_s2[i, j] = delta_cm * REV_PREM / REV_TOTAL

gm_s2_ma = np.ma.masked_invalid(gm_s2)
_vmax = float(np.nanmax(gm_s2))
im2 = ax2.imshow(gm_s2_ma, cmap='Blues', aspect='auto', vmin=0, vmax=_vmax)
ax2.set_xticks(range(_n2x))
ax2.set_xticklabels([f'{int(x)}pp' for x in shift_pct], fontsize=8)
ax2.set_yticks(range(_n2y))
ax2.set_yticklabels([f'{int(p)}%' for p in pod_share], fontsize=8)
ax2.set_xlabel('Music share reduction Δmusic (pp)', fontsize=9)
ax2.set_ylabel('Podcast share of FY2028 mix (%)', fontsize=9)
ax2.set_title(
    'S2 — GM Impact (pp)\nCM mix model: music reduction × podcast share',
    fontweight='bold',
    fontsize=9,
)
for i in range(_n2y):
    for j in range(_n2x):
        v = gm_s2[i, j]
        if np.isnan(v):
            continue
        ax2.text(
            j, i, f'{v:.2f}pp', ha='center', va='center', fontsize=8.5,
            fontweight='bold',
            color='black' if v < _vmax * 0.7 else 'white',
        )
plt.colorbar(im2, ax=ax2, label='GM improvement (pp)', shrink=0.85)

# ── S3: Supremium adoption × downgrade rate d (net blended ARPU €/mo) ────
s3_adopt = np.array([15, 16, 17, 18, 19, 20], dtype=float)
s3_d_pct = np.array([3, 4, 5, 6, 7], dtype=float)
_n3y, _n3x = len(s3_d_pct), len(s3_adopt)
s3_net = np.zeros((_n3y, _n3x))
for i, d_pct in enumerate(s3_d_pct):
    d = d_pct / 100.0
    for j, a_pct in enumerate(s3_adopt):
        a = a_pct / 100.0
        gross = S3_INDIVIDUAL_SHARE_PREM * a * S3_DELTA_P_SUPREMIUM_EUR
        drag = S3_INDIVIDUAL_SHARE_PREM * d * (1.0 - a) * S3_DELTA_P_DOWNGRADE_EUR
        s3_net[i, j] = gross - drag

_v3min, _v3max = float(s3_net.min()), float(s3_net.max())
im3 = ax3.imshow(s3_net, cmap='YlGn', aspect='auto', vmin=_v3min, vmax=_v3max)
ax3.set_xticks(range(_n3x))
ax3.set_xticklabels([f'{int(x)}%' for x in s3_adopt], fontsize=8)
ax3.set_yticks(range(_n3y))
ax3.set_yticklabels([f'{int(x)}%' for x in s3_d_pct], fontsize=8)
ax3.set_xlabel('Supremium adoption (% of Individual base)', fontsize=8)
ax3.set_ylabel('Downgrade / cannib. rate d\n(% of non-adopters)', fontsize=8)
ax3.set_title(
    'S3 — Net ARPU uplift (€/mo)\nSupremium adoption × downgrade rate',
    fontweight='bold',
    fontsize=9,
)
# Base-case d = 5% row (Table 6) — faint band only
ax3.axhspan(1.5, 2.5, color='blue', alpha=0.06, zorder=0)
for i in range(_n3y):
    for j in range(_n3x):
        v = s3_net[i, j]
        ax3.text(
            j, i, f'+€{v:.2f}', ha='center', va='center', fontsize=8,
            fontweight='bold',
            color='black' if v < _v3min + 0.65 * (_v3max - _v3min) else 'white',
        )
plt.colorbar(im3, ax=ax3, label='Net ARPU uplift (€/mo)', shrink=0.85)

plt.tight_layout(pad=1.8)
plt.savefig(f'{FIGS}/figure_09_strategy_sensitivity_heatmaps.png', dpi=150, bbox_inches='tight', pad_inches=0.35)
plt.close()
print('Saved: figure_09_strategy_sensitivity_heatmaps.png')

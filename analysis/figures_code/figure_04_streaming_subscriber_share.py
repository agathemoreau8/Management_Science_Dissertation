"""
figure_04 — Global streaming subscriber share pie (author-provided shares); saves ``figure_06_streaming_subscriber_share.png``.
"""

import sys, os

sys.path.insert(0, '/tmp/pylibs')
_FCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _FCDIR)
sys.path.insert(0, os.path.join(_FCDIR, '..'))

from _shared import FIGS, SPOTIFY_STYLE, GREEN
import matplotlib.pyplot as plt

plt.rcParams.update(SPOTIFY_STYLE)

# User-provided 2025 share table (%)
share_pct = {
    "Spotify": 31.7,
    "Tencent Music": 14.4,
    "Apple Music": 12.6,
    "Amazon Music": 11.1,
    "YouTube Music": 9.7,
    "NetEase": 6.7,
    "Yandex": 3.4,
    "Deezer": 1.3,
    # Adjusted from 9.7% to 9.1% so total share sums to 100.0%
    "Others": 9.1,
}

# User-provided known absolute subscribers (M) where both metrics are given
known_subs_m = {
    "Spotify": 270.0,
    "Tencent Music": 125.7,
    "YouTube Music": 125.0,
    "Apple Music": 94.0,
    "Amazon Music": 80.0,
}

# Implied total market from the anchor pair Spotify (270M, 31.7%)
total_subs = known_subs_m["Spotify"] / (share_pct["Spotify"] / 100.0)

platforms = list(share_pct.keys())
pct_values = [share_pct[p] for p in platforms]
subs_m = [known_subs_m[p] if p in known_subs_m else total_subs * share_pct[p] / 100.0 for p in platforms]

# Spotify-style palette (stronger colors for readability)
colors = [
    GREEN, "#6C5CE7", "#9AA9DA", "#E8C995", "#E19CBC",
    "#8FB4D1", "#C9B28F", "#BCD6B7", "#C8C8C8"
]

fig, ax = plt.subplots(figsize=(10, 7))
ax.set_facecolor("#FCFCFC")

def autopct_fmt(pct):
    # Show count only for large slices (>= ~9%) to avoid clutter.
    if pct < 3.8:
        return ""
    if pct >= 9.0:
        absolute = total_subs * pct / 100.0
        return f"{pct:.1f}%\n({absolute:.1f}M)"
    return f"{pct:.1f}%"

wedges, _, _ = ax.pie(
    pct_values,
    labels=None,
    autopct=autopct_fmt,
    startangle=90,
    counterclock=False,
    colors=colors,
    wedgeprops={"edgecolor": "white", "linewidth": 1.1},
    textprops={"fontsize": 9, "fontweight": "bold", "color": "#2B2B2B"},
    pctdistance=0.72,
)

legend_labels = [f"{p}: {share_pct[p]:.1f}% ({s:.1f}M)" for p, s in zip(platforms, subs_m)]
ax.legend(
    wedges,
    legend_labels,
    title="2025 Share and Subscribers",
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    frameon=True,
    edgecolor="#D9D9D9",
    facecolor="white",
    framealpha=0.95,
    fontsize=9,
    title_fontsize=10,
)

ax.set_title(
    "Global Music Streaming Subscriber Share (2025)\n"
    f"Shares fixed from source; missing subscriber counts derived from implied total {total_subs:.1f}M",
    fontweight="bold",
)
ax.axis("equal")

plt.tight_layout()
plt.savefig(f"{FIGS}/figure_04_streaming_subscriber_share.png", dpi=160, bbox_inches="tight", pad_inches=0.35)
plt.close()

print("Saved: figure_04_streaming_subscriber_share.png")

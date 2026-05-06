"""
Run all dissertation figure scripts in order.

Usage (repo root or this folder):
  python3 analysis/figures_code/run_all_figures.py

Outputs PNG files under ``writting/figures/`` with names matching each script
(e.g. ``figure_01_mau_subscribers.png`` from ``figure_01_mau_subscribers.py``).
"""
import os
import subprocess
import sys

os.environ.setdefault('MPLBACKEND', 'Agg')
os.environ.setdefault('MPLCONFIGDIR', '/tmp/mplcache')

HERE = os.path.dirname(os.path.abspath(__file__))
scripts = [
    'figure_01_mau_subscribers.py',
    'figure_02_monetisation_paradox.py',
    'figure_03_porters_five_forces.py',
    'figure_04_streaming_subscriber_share.py',
    'figure_05_competitor_benchmarking.py',
    'figure_06_customer_clv_segments.py',
    'figure_07_gross_margin_trend.py',
    'figure_10_gross_margin_path.py',
    'figure_11_gross_margin_waterfalls.py',
    'figure_12_price_elasticity_yoy.py',
    'figure_multi_strategy_sensitivity_heatmaps.py',
    'figure_14_premium_arpu_path.py',
    'figure_15_gm_scenarios_horizontal_bars.py',
    'figure_16_s3_adoption_net_arpu.py',
    'figure_18_strategy_scorecard.py',
    'figure_19_implementation_roadmap.py',
]

ok, fail = [], []
for s in scripts:
    path = os.path.join(HERE, s)
    result = subprocess.run(
        [sys.executable, path],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        note = ''
        out = (result.stdout or '')
        if 'SKIP figure_05' in out:
            note = '  (skipped — add competitor_stats_2025.xlsx under analysis/ or data/)'
        print(f'  OK  {s}{note}')
        ok.append(s)
    else:
        err = (result.stderr or '').strip()[-240:] or (result.stdout or '').strip()[-240:]
        print(f'  ERR {s}: {err}')
        fail.append(s)

print(f'\n{len(ok)}/{len(scripts)} figures generated successfully.')
if fail:
    print('Failed:', fail)
    sys.exit(1)

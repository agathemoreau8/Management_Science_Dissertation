"""
Run all OLS regression scripts in order and print consolidated output.

Usage (from repo root):
  python3 analysis/regression/run_all.py
"""
import sys
import os

sys.path.insert(0, '/tmp/pylibs')

# Allow imports when executed from any cwd
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from r01_premium_cost_on_premium_revenue import main as main_r01
from r02_gross_margin_on_time import main as main_r02
from r03_yoy_subs_on_yoy_arpu import main as main_r03
from r04_premium_arpu_on_time import main as main_r04
from r05_ln_mau_on_ln_arpu_and_time import main as main_r05


def main():
    from common import load_df18

    df = load_df18()
    print('=' * 65)
    print('  SPOTIFY OLS REGRESSIONS  |  analysis/regression/')
    print(f'  Panel: Q1 2018 – last quarter in file  |  n = {len(df)} quarters')
    print('=' * 65)

    main_r01()
    print()
    main_r02()
    print()
    main_r03()
    print()
    main_r04()
    print()
    main_r05()
    print()
    print('=' * 65)
    print('  All regression modules finished.')
    print('=' * 65)


if __name__ == '__main__':
    main()

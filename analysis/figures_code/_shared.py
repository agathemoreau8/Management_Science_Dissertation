"""
Shared constants and data loading for ``analysis/figures_code/figure_*.py``.

Import with: ``from _shared import df18, FIGS, SPOTIFY_STYLE``

DATA SOURCE
-----------
Primary dataset : data/spotify_financials.csv
    - Spotify quarterly financial statements, Q1 2017 – Q3 2024
    - Columns: Total Revenue, Cost of Revenue, Gross Profit, Premium Revenue,
      Premium Cost of Revenue, Ad Revenue, MAUs, Premium MAUs, Premium ARPU,
      Gross profit margin, Premium Gross profit margin, Ad Gross profit margin
    - All revenue/cost figures in €M; MAUs in millions; ARPU in €/month
    - Source: Spotify Technology S.A. quarterly earnings reports (Spotify, 2024)

Supplementary row (Q4 2024, hardcoded below):
    - Q4 2024 was not yet in the CSV at time of analysis
    - Values taken directly from:
        Spotify Technology S.A. (2024) Q4 2024 Shareholder Letter and
        Financial Supplement. Stockholm: Spotify Technology S.A.
        https://investors.spotify.com/financials/press-releases-and-events/
    - Key Q4 2024 values: MAUs=675M, Premium MAUs=263M, ARPU=€4.85,
      Total Revenue=€4,242M, Gross Profit=€1,368M, GM%=32.2%
    - Note: 32.2% is the Q4 2024 QUARTERLY gross margin.
      FY 2024 full-year GM = 30.1% (sum of all four quarters' GP / Revenue).

Derived columns (added after loading):
    - t          : integer time index (0 = Q1 2018) used as regressor in OLS
    - Conversion : Premium MAUs / MAUs × 100  (Premium conversion rate %)
"""
import sys, os
sys.path.insert(0, '/tmp/pylibs')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statsmodels.api as sm
import warnings; warnings.filterwarnings('ignore')

# Paths 
_HERE = os.path.dirname(os.path.abspath(__file__))
FIGS  = os.path.join(_HERE, '..', '..', 'writting', 'figures')
DATA  = os.path.join(_HERE, '..', '..', 'data', 'spotify_financials.csv')

# Spotify brand colours 
GREEN  = '#1DB954'   # Spotify green
PINK   = '#E8115B'   # Spotify pink/red
BLUE   = '#2D46B9'   # Spotify blue
GOLD   = '#F59B00'   # Accent gold
DARK   = '#191414'   # Spotify dark background
LGREY  = '#FAFAFA'   # Plot background

# Matplotlib style 
SPOTIFY_STYLE = {
    'font.family': 'sans-serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': 'white',
    'axes.facecolor': LGREY,
    'grid.color': '#EEEEEE',
    'grid.linewidth': 0.6,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
}

# Load & clean data 
# Source: data/spotify_financials.csv — Spotify quarterly reports Q1 2017–Q3 2024
df_raw = pd.read_csv(DATA, quotechar='"', skipinitialspace=True)
df_raw.columns = [c.strip() for c in df_raw.columns]
for c in ['Total Revenue','Cost of Revenue','Gross Profit','Premium Revenue',
          'Ad Revenue','MAUs','Premium MAUs','Premium ARPU','Premium Cost of Revenue']:
    df_raw[c] = df_raw[c].astype(str).str.replace(',','').str.replace('"','').astype(float)
for c in ['Gross profit margin','Premium Gross profit margin']:
    df_raw[c] = df_raw[c].astype(str).str.replace('%','').astype(float)
df_raw['Date'] = pd.to_datetime(df_raw['Date'], dayfirst=True)
df_raw = df_raw.sort_values('Date').reset_index(drop=True)

# Filter to Q1 2018 onwards (n=27 quarters from CSV) for regression consistency
df18 = df_raw[df_raw['Date'] >= '2018-01-01'].reset_index(drop=True)

# Append Q4 2024 manually: source: Spotify Q4 2024 Shareholder Letter
# (not in CSV; hardcoded for analytical consistency across all figures)
q4 = {'Date': pd.Timestamp('2024-12-31'), 'Total Revenue': 4242,
      'Cost of Revenue': 2874, 'Gross Profit': 1368, 'Premium Revenue': 3705,
      'Ad Revenue': 537, 'MAUs': 675, 'Premium MAUs': 263,
      'Premium ARPU': 4.85, 'Gross profit margin': 32.2,   # quarterly GM
      'Premium Gross profit margin': 34.7, 'Premium Cost of Revenue': 2419}
df18 = pd.concat([df18, pd.DataFrame([q4])], ignore_index=True)  # n=28 total

# Derived columns used in regressions and figures
df18['t'] = np.arange(len(df18))                          # time index: 0=Q1 2018
df18['Conversion'] = df18['Premium MAUs'] / df18['MAUs'] * 100  # conversion rate %

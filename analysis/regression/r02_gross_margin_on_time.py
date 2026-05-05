"""
R2 — Consolidated gross profit margin (%) on a linear time trend.

What this regression is for (Part B §2.1)
----------------------------------------
After R1 establishes that premium *cost* tracks premium *revenue*, R2 asks a
different question: is **reported consolidated gross margin** improving **over
time** anyway, without attributing that improvement to any single lever? We use
a simple clock index t so each quarter gets one extra “step”—a crude but
transparent **organic trajectory** for gross margin.

Data
----
• Source panel: `data/spotify_financials.csv`, cleaned and extended in
  `figures_code/_shared.py` (incl. Q4 2024 row), via `load_df18()`.
• Frequency: quarterly.
• Window: Q1 2018 – Q4 2024 → n = 28 quarters.
• Dependent variable (y): **Gross profit margin** (%) — consolidated (“company”)
  margin as reported in the financial statements for that quarter (see Spotify’s
  quarterly filings / your CSV column definition).
• Independent variable (x): **t** = 0, 1, 2, … — quarter index with **t = 0**
  at Q1 2018. So β₁ is “percentage points of GM per quarter”.

What we are testing
-------------------
We estimate:  GM_t = β₀ + β₁ × t + u

• H₀ : β₁ = 0  — no systematic linear improvement in gross margin over the
       sample window (after Q1 2018).
• H₁ : β₁ > 0  — gross margin has a positive time slope (structural or
       reporting mix improves on average each quarter in this specification).

If you reject H₀, **R² still matters**: a low R² means the linear trend only
explains part of the variation—quarter-to-quarter noise and other drivers still
dominate. That is exactly why Part B argues **organic drift alone will not
close the full +5pp gap** to the FY2028 target; strategies S1–S3 are still
needed.

Caveats
-------
• **Forecast vs counterfactual**: the +12q illustration at the end is a
  mechanical extrapolation of a **descriptive** trend, not Spotify management’s
  guidance.
• **Quarterly vs FY**: FY headline margins in annual reports can differ from
  averaging quarters; be consistent with what your CSV uses in the narrative.
• Serial correlation in margins may affect inference on β₁; note Durbin–Watson
  if you discuss inference critically.

Usage
-----
From the dissertation project root:

  python3 analysis/regression/r02_gross_margin_on_time.py
"""
import sys
sys.path.insert(0, '/tmp/pylibs')

import numpy as np
import statsmodels.api as sm

from common import load_df18


def fit():
    df = load_df18()
    X = sm.add_constant(df['t'])
    y = df['Gross profit margin']
    return sm.OLS(y, X).fit()


def main():
    df = load_df18()
    r = fit()
    ci = r.conf_int()
    n = len(df)
    beta1_pp_per_q = r.params[1]
    beta1_pp_per_year = beta1_pp_per_q * 4

    print('=' * 65)
    print('R2 — Consolidated Gross Margin % ~ time t')
    print('=' * 65)
    print(
        """
DATA (what goes into the regression)
  • Panel     : Spotify quarterly financials, Q1 2018 – Q4 2024
  • n         : {n} quarters
  • y         : Gross profit margin (%, consolidated as in CSV)
  • x         : t = 0, 1, … (quarters since Q1 2018)
  • Source    : spotify_financials.csv + shared Q4 2024 row (load_df18)

QUESTION UNDER TEST
  Is there evidence of a **positive linear drift** in consolidated gross margin
  over the panel? If yes, how strong is that drift relative to quarter-to-quarter
  volatility (see R²)? Part B uses this as an **organic baseline** against which
  Discovery Mode (S1) and the rest of the programme must add incremental margin.

HYPOTHESES
  H₀ : β₁ = 0   (no trend in GM over t in this window)
  H₁ : β₁ > 0   (GM improves on average each additional quarter)
""".strip().format(n=n)
    )

    print('-' * 65)
    print(r.summary())
    print(
        f"\n  Equation : GM(t) = {r.params[0]:.4f} + {r.params[1]:.4f} × t"
    )
    print(f"  R²       : {r.rsquared:.4f}   Adj-R²: {r.rsquared_adj:.4f}")
    print(f"  p(β₁)    : {r.pvalues[1]:.6f}")
    print(
        f"  95% CI β₁: [{ci.iloc[1, 0]:.4f}, {ci.iloc[1, 1]:.4f}] "
        'percentage points per quarter'
    )
    print(
        f"\n  → Trend speed: about {beta1_pp_per_q:.3f} pp per quarter "
        f"(≈ {beta1_pp_per_year:.2f} pp per year if extrapolated linearly × 4)."
    )
    print(
        f"  → Share of variance explained by this single linear trend: "
       f'{r.rsquared*100:.1f}% (1 − R² is “everything else”).'
    )

    t_future = np.arange(len(df), len(df) + 12)
    gm_fc = r.predict(sm.add_constant(t_future))
    print(
        f"\n  Illustrative extrapolation: GM twelve quarters beyond the sample end "
        f'≈ {gm_fc[-1]:.2f}% (descriptive only — not a management forecast).'
    )
    decision = 'Reject H₀ at 5%' if r.pvalues[1] < 0.05 else 'Cannot reject H₀ at 5%'
    print(f"\n  Decision (one-sided intuition): {decision} for β₁ > 0.")


if __name__ == '__main__':
    main()

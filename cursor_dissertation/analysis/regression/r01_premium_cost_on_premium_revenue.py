"""
R1 — Premium Cost of Revenue on Premium Revenue (quarterly €M).

What this regression is for (Part B §2.1)
----------------------------------------
Spotify reports, each quarter, how much Premium revenue it earns and how much
Premium *cost of revenue* it pays (chiefly royalties and other variable-ish
costs tied to streaming that segment). We regress the latter on the former to
ask: when Premium revenue moves, does cost of revenue move in proportion?

Data
----
• Source panel: `data/spotify_financials.csv`, cleaned and extended in
  `figures_code/_shared.py` with one manually added Q4 2024 row (same convention
  as the rest of Part B).
• Frequency: quarterly.
• Window loaded here: Q1 2018 through Q4 2024 → n = 28 quarters (see `load_df18()`).
• Dependent variable (y): **Premium Cost of Revenue** — € millions per quarter.
• Independent variable (x): **Premium Revenue** — € millions per quarter.
• Both series are as reported in Spotify’s quarterly disclosures (not inflation-
  adjusted; EUR).

What we are testing
-------------------
We estimate:  Premium_CoR = β₀ + β₁ × Premium_Revenue + u

• H₀ : β₁ = 0  — premium revenue tells you nothing about premium cost of revenue
       (no detectable linear co-movement in the sample).
• H₁ : β₁ > 0  — higher premium revenue is associated with higher cost of
       revenue (consistent with royalties and similar costs scaling with revenue).

A slope β₁ close to the blended royalty share (often discussed around ~0.65–0.70
in streaming) supports using **cost–volume–profit (CVP)** logic for Discovery
Mode: a small change in effective royalty *rate* maps mechanically into gross
profit because marginal cost tracks premium revenue.

Caveats (keep in mind when you write up)
---------------------------------------
• Causality: OLS shows association in the time series, not proof that revenue
  “causes” cost in a structural sense.
• The intercept β₀ at **zero** revenue is not economically meaningful (Spotify
  never has zero premium revenue); focus interpretation on **β₁**.
• Residual correlation across quarters (Durbin–Watson) may warrant caution on
  naive standard errors — fine for coursework narrative if you acknowledge it.

Usage
-----
From the dissertation project root:

  python3 analysis/regression/r01_premium_cost_on_premium_revenue.py

"""
import sys
sys.path.insert(0, '/tmp/pylibs')

import statsmodels.api as sm

from common import load_df18


def fit():
    df = load_df18()
    X = sm.add_constant(df['Premium Revenue'])
    y = df['Premium Cost of Revenue']
    return sm.OLS(y, X).fit()


def main():
    df = load_df18()
    r = fit()
    ci = r.conf_int()
    n = len(df)

    print('=' * 65)
    print('R1 — Premium Cost of Revenue ~ Premium Revenue')
    print('=' * 65)
    print("""
DATA (what goes into the regression)
  • Panel     : Spotify quarterly financials, Q1 2018 – Q4 2024
  • n         : {} quarters
  • y         : Premium Cost of Revenue (€M per quarter)
  • x         : Premium Revenue (€M per quarter)
  • Source    : spotify_financials.csv + shared Q4 2024 row (_shared.load / load_df18)

QUESTION UNDER TEST
  Does Premium Cost of Revenue rise in (rough) proportion to Premium Revenue —
  i.e. is β₁ positive and large enough to treat royalty-heavy cost as
  quasi-variable with revenue? That justifies CVP-style margin analysis for
  Strategy 1 (Discovery Mode).

HYPOTHESES
  H₀ : β₁ = 0      (no linear relationship)
  H₁ : β₁ > 0      (cost co-moves with revenue; expect rejection if royalties scale)
""".strip().format(n))

    print('-' * 65)
    print(r.summary())
    print(
        f"\n  Equation : PremCoR = {r.params[0]:.1f} + {r.params[1]:.4f} × Premium_Revenue"
    )
    print(f"  R²       : {r.rsquared:.4f}   Adj-R²: {r.rsquared_adj:.4f}")
    print(f"  p(β₁)    : {r.pvalues[1]:.6f}")
    print(f"  95% CI β₁: [{ci.iloc[1, 0]:.4f}, {ci.iloc[1, 1]:.4f}]")
    print(
        "\n  → Incremental interpretation (both in €M): an extra €1M of Premium"
    )
    print(
        f"     Revenue in a quarter is associated with ~€{r.params[1]*1.0:.2f}M higher"
    )
    print(
        f"     Premium Cost of Revenue (≈{r.params[1]*100:.1f}% marginal pass-through)."
    )
    decision = 'Reject H₀ at 5%' if r.pvalues[1] < 0.05 else 'Cannot reject H₀ at 5%'
    print(f"\n  Decision (one-sided intuition): {decision} for β₁ > 0.")


if __name__ == '__main__':
    main()

"""
Shared FY2025 inputs and NPV/CVP outputs for Part B (figure scripts and quantitative models).

Figures import ``GM_*``, ``NPV_*``, ``S2_*``, ``S3_*``, etc. Update assumptions here only.
"""
ARPU_FY25 = 4.63
ARPU_Q4_25 = 4.70
TARGET_ARPU = round(ARPU_FY25 * 1.15, 2)
DELTA_ARPU = round(TARGET_ARPU - ARPU_FY25, 2)
N_PREM = 290
N_AD = 476
N_MAU = N_PREM + N_AD
REV_PREM = 15_350
REV_AD = 1_836
REV_TOTAL = REV_PREM + REV_AD
AD_ARPU = round(REV_AD / (N_AD * 12), 4)
GM_CONSOL = 32.0
GM_PREM = 34.0
GM_AD = 18.0
TARGET_GM = 37.0

S3_INDIVIDUAL_SHARE_PREM = 0.63
S3_DELTA_P_SUPREMIUM_EUR = 5.00
S3_DELTA_P_DOWNGRADE_EUR = 2.00
S3_TARGET_ARPU_FY28 = 5.09
S3_BASE_DOWNGRADE_RATE = 0.05

R1_PREM_COR_SLOPE = 0.6570
R2_GM_TREND_PP_PER_Q = 0.122
ORGANIC_GM_DRIFT_3Y_PP = 1.5

S2_CM_MUSIC_PCT = 34
S2_CM_PODCAST_PCT = 85
S2_CM_AUDIOBOOK_PCT = 80
S2_SHARE_MUSIC_FY25, S2_SHARE_PODCAST_FY25, S2_SHARE_AUDIOBOOK_FY25 = 85, 13, 2
S2_BLENDED_CM_FY25 = round(
    (
        S2_SHARE_MUSIC_FY25 * S2_CM_MUSIC_PCT
        + S2_SHARE_PODCAST_FY25 * S2_CM_PODCAST_PCT
        + S2_SHARE_AUDIOBOOK_FY25 * S2_CM_AUDIOBOOK_PCT
    )
    / 100.0,
    2,
)

S2_SHARE_CONS_M, S2_SHARE_CONS_P, S2_SHARE_CONS_A = 82, 14, 4
S2_SHARE_BASE_M, S2_SHARE_BASE_P, S2_SHARE_BASE_A = 78, 17, 5
S2_SHARE_OPT_M, S2_SHARE_OPT_P, S2_SHARE_OPT_A = 74, 19, 7


def _s2_blended_cm(music_pct: int, pod_pct: int, audio_pct: int) -> float:
    return (
        music_pct * S2_CM_MUSIC_PCT
        + pod_pct * S2_CM_PODCAST_PCT
        + audio_pct * S2_CM_AUDIOBOOK_PCT
    ) / 100.0


S2_BLENDED_CM_CONS = round(_s2_blended_cm(82, 14, 4), 2)
S2_BLENDED_CM_BASE = round(_s2_blended_cm(78, 17, 5), 2)
S2_BLENDED_CM_OPT = round(_s2_blended_cm(74, 19, 7), 2)

S2_DELTA_BLENDED_CM_CONS_PP = round(S2_BLENDED_CM_CONS - S2_BLENDED_CM_FY25, 2)
S2_DELTA_BLENDED_CM_BASE_PP = round(S2_BLENDED_CM_BASE - S2_BLENDED_CM_FY25, 2)
S2_DELTA_BLENDED_CM_OPT_PP = round(S2_BLENDED_CM_OPT - S2_BLENDED_CM_FY25, 2)

S2_DELTA_GP_CONS_M = round(REV_PREM * S2_DELTA_BLENDED_CM_CONS_PP / 100)
S2_DELTA_GP_BASE_M = round(REV_PREM * S2_DELTA_BLENDED_CM_BASE_PP / 100)
S2_DELTA_GP_OPT_M = round(REV_PREM * S2_DELTA_BLENDED_CM_OPT_PP / 100)

S2_DELTA_GM_CONS_PP = round(S2_DELTA_GP_CONS_M / REV_TOTAL * 100, 2)
S2_DELTA_GM_BASE_PP = round(S2_DELTA_GP_BASE_M / REV_TOTAL * 100, 2)
S2_DELTA_GM_OPT_PP = round(S2_DELTA_GP_OPT_M / REV_TOTAL * 100, 2)

GM_BRIDGE_S1_PARTIAL_PP = 1.17
GM_BRIDGE_ORGANIC_IMPROV_PP = 1.50
GM_BRIDGE_HEADWIND_ROBUST_PP = -0.08
GM_BRIDGE_ROBUST_DELTA_SUM_PP = round(
    GM_BRIDGE_S1_PARTIAL_PP
    + S2_DELTA_GM_BASE_PP
    + GM_BRIDGE_ORGANIC_IMPROV_PP
    + GM_BRIDGE_HEADWIND_ROBUST_PP,
    2,
)
GM_ROBUST_CONSOL_GM_PCT = round(GM_CONSOL + GM_BRIDGE_ROBUST_DELTA_SUM_PP, 2)

S2_DECOMP_MUSIC_PP = round(-7 * S2_CM_MUSIC_PCT / 100, 2)
S2_DECOMP_PODCAST_PP = round(4 * S2_CM_PODCAST_PCT / 100, 2)
S2_DECOMP_AUDIOBOOK_PP = round(3 * S2_CM_AUDIOBOOK_PCT / 100, 2)

WACC = 0.08
C_CHURN = 0.039
I_MONTHLY = WACC / 12
DENOM_CLV = C_CHURN + I_MONTHLY
CLV_PREM = round((ARPU_FY25 * GM_PREM / 100) / DENOM_CLV, 2)
CLV_FREE = round((AD_ARPU * GM_AD / 100) / DENOM_CLV, 2)

PV1, PV2, PV3 = 1 / 1.08, 1 / 1.08 ** 2, 1 / 1.08 ** 3

DGP_S1_Y1 = N_PREM * ARPU_FY25 * 0.015 * 12
DGP_S1_Y2 = N_PREM * ARPU_FY25 * 0.030 * 12
DGP_S1_Y3 = (N_PREM + 20) * ARPU_FY25 * 0.035 * 12
NPV_S1 = round(DGP_S1_Y1 * PV1 + DGP_S1_Y2 * PV2 + DGP_S1_Y3 * PV3)

I0_S2 = 350
DGP_S2_Y1 = REV_TOTAL * 0.05 * 0.15 + 60
DGP_S2_Y2 = REV_TOTAL * 0.10 * 0.15 + 110
DGP_S2_Y3 = REV_TOTAL * 0.12 * 0.15 + 130
NPV_S2 = round(DGP_S2_Y1 * PV1 + DGP_S2_Y2 * PV2 + DGP_S2_Y3 * PV3 - I0_S2)

DGP_S3_Y1 = N_PREM * DELTA_ARPU * (GM_PREM / 100) * 12 * 0.5
DGP_S3_Y2 = N_PREM * DELTA_ARPU * (GM_PREM / 100) * 12
DGP_S3_Y3 = (N_PREM + 20) * DELTA_ARPU * (GM_PREM / 100) * 12
NPV_S3 = round(DGP_S3_Y1 * PV1 + DGP_S3_Y2 * PV2 + DGP_S3_Y3 * PV3)

NPV_COMBINED = round((NPV_S1 + NPV_S2 + NPV_S3) * 1.12)

NPV_SCENARIO_DOWN = round(NPV_COMBINED * 0.58)
NPV_SCENARIO_BASE = NPV_COMBINED
NPV_SCENARIO_UP = round(NPV_COMBINED * 1.14)
P_SCENARIO_DOWN = 0.28
P_SCENARIO_BASE = 0.50
P_SCENARIO_UP = 0.22
ENPV_COMBINED = round(
    P_SCENARIO_DOWN * NPV_SCENARIO_DOWN
    + P_SCENARIO_BASE * NPV_SCENARIO_BASE
    + P_SCENARIO_UP * NPV_SCENARIO_UP
)

DGP_S1_FULL = N_PREM * ARPU_FY25 * 0.03 * 12
GM_PP_S1 = DGP_S1_FULL / REV_TOTAL * 100
GM_S1_FULL_GM_PP = round(GM_PP_S1, 2)

GM_BRIDGE_HEADWIND_PRIMARY_CONS_PP = GM_BRIDGE_HEADWIND_ROBUST_PP
GM_BRIDGE_PRIMARY_CONS_DELTA_SUM_PP = round(
    GM_S1_FULL_GM_PP
    + S2_DELTA_GM_CONS_PP
    + GM_BRIDGE_ORGANIC_IMPROV_PP
    + GM_BRIDGE_HEADWIND_PRIMARY_CONS_PP,
    2,
)
GM_PRIMARY_CONS_CONSOL_GM_PCT = round(GM_CONSOL + GM_BRIDGE_PRIMARY_CONS_DELTA_SUM_PP, 2)

dgp_s1_y1, dgp_s1_y2, dgp_s1_y3 = DGP_S1_Y1, DGP_S1_Y2, DGP_S1_Y3
dgp_s2_y1, dgp_s2_y2, dgp_s2_y3 = DGP_S2_Y1, DGP_S2_Y2, DGP_S2_Y3
i0_s2 = I0_S2
dgp_s3_y1, dgp_s3_y2, dgp_s3_y3 = DGP_S3_Y1, DGP_S3_Y2, DGP_S3_Y3
npv_s1, npv_s2, npv_s3, npv_combined = NPV_S1, NPV_S2, NPV_S3, NPV_COMBINED
npv_scenario_down, npv_scenario_base, npv_scenario_up = (
    NPV_SCENARIO_DOWN, NPV_SCENARIO_BASE, NPV_SCENARIO_UP)
p_scenario_down, p_scenario_base, p_scenario_up = (
    P_SCENARIO_DOWN, P_SCENARIO_BASE, P_SCENARIO_UP)
enpv_combined = ENPV_COMBINED
pv1, pv2, pv3 = PV1, PV2, PV3


def npv_from_params(arpu_mult=1.0, prem_mult=1.0, delta_arpu_mult=1.0,
                    wacc=None, royalty_eff_mult=1.0, s2_invest_mult=1.0):
    if wacc is None:
        wacc = WACC
    pv1, pv2, pv3 = 1 / (1 + wacc), 1 / (1 + wacc) ** 2, 1 / (1 + wacc) ** 3
    arpu = ARPU_FY25 * arpu_mult
    n0 = N_PREM * prem_mult
    d_arpu = DELTA_ARPU * delta_arpu_mult
    s1y1 = n0 * arpu * 0.015 * 12 * royalty_eff_mult
    s1y2 = n0 * arpu * 0.030 * 12 * royalty_eff_mult
    s1y3 = (n0 + 20) * arpu * 0.035 * 12 * royalty_eff_mult
    npv1 = s1y1 * pv1 + s1y2 * pv2 + s1y3 * pv3
    s2y1 = REV_TOTAL * 0.05 * 0.15 + 60
    s2y2 = REV_TOTAL * 0.10 * 0.15 + 110
    s2y3 = REV_TOTAL * 0.12 * 0.15 + 130
    npv2 = s2y1 * pv1 + s2y2 * pv2 + s2y3 * pv3 - I0_S2 * s2_invest_mult
    s3y1 = n0 * d_arpu * (GM_PREM / 100) * 12 * 0.5
    s3y2 = n0 * d_arpu * (GM_PREM / 100) * 12
    s3y3 = (n0 + 20) * d_arpu * (GM_PREM / 100) * 12
    npv3 = s3y1 * pv1 + s3y2 * pv2 + s3y3 * pv3
    return round((npv1 + npv2 + npv3) * 1.12)


def tornado_sensitivity(pct=0.10):
    rows = []
    rows.append(('Premium subs ±10%', npv_from_params(prem_mult=1 - pct),
                 npv_from_params(prem_mult=1 + pct)))
    rows.append(('FY25 ARPU ±10%', npv_from_params(arpu_mult=1 - pct),
                 npv_from_params(arpu_mult=1 + pct)))
    rows.append(('ARPU target gap ±10%', npv_from_params(delta_arpu_mult=1 - pct),
                 npv_from_params(delta_arpu_mult=1 + pct)))
    rows.append(('Royalty relief (S1) ±10%', npv_from_params(royalty_eff_mult=1 - pct),
                 npv_from_params(royalty_eff_mult=1 + pct)))
    rows.append(('S2 upfront invest ±10%', npv_from_params(s2_invest_mult=1 + pct),
                 npv_from_params(s2_invest_mult=1 - pct)))
    rows.append(('WACC −1pp / +1pp', npv_from_params(wacc=WACC - 0.01),
                 npv_from_params(wacc=WACC + 0.01)))
    return rows

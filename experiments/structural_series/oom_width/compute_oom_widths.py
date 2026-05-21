#!/usr/bin/env python3
"""
OOM corridor-width test — compute the log-width (decades) of every corridor the
framework has empirically measured, and apply the pre-registered cluster
criterion.

Pre-registration: PREREGISTRATION.md (committed before this script ran).

Width definition (pre-registered):
  - corridor on a multiplicative axis (g/J ratio, k_eff): log10(upper/lower).
  - corridor as a rho-band [rho_lo, rho_hi]: primary width = log10(rho_hi/rho_lo)
    -- the k_eff-axis log-width via the Kish asymptotic k_eff -> 1/rho.
    finite-k companion: log10(k_eff(k,rho_lo)/k_eff(k,rho_hi)) where k known.

Cluster criterion (pre-registered, on coordinated-substrate primary widths):
  CLUSTERED iff  every width in [0.6, 1.5] decades  AND  std(widths) < 0.30.
"""
import json
import math
import statistics
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SS = os.path.normpath(os.path.join(HERE, ".."))          # structural_series/
ROOT = os.path.normpath(os.path.join(SS, "..", ".."))    # repo root


def k_eff(k, rho):
    return k / (1.0 + rho * (k - 1.0))


def log_width_ratio(lo, hi):
    """log10 of a multiplicative span, lo<hi (both > 0)."""
    return math.log10(hi / lo)


# ---------------------------------------------------------------------------
# Collect corridors. Each entry:
#   name, kind ('coordinated' | 'falsifier' | 'reference'),
#   bounds, axis description, source, finite-k companion (or None).
# ---------------------------------------------------------------------------
corridors = []

# 1. LLM within-layer rho (E1) -- structural_series/NOTES.md, exp_E1_llm_corridor.py
#    "Debiased rho [0.046, 0.218], mean 0.091 over 48 layers" -- 3 architectures.
rho_lo, rho_hi = 0.046, 0.218
corridors.append(dict(
    name="LLM within-layer rho (E1)",
    kind="coordinated",
    rho=(rho_lo, rho_hi),
    primary=log_width_ratio(rho_lo, rho_hi),
    axis="rho-band -> k_eff via 1/rho asymptotic",
    source="structural_series/NOTES.md (exp_E1_llm_corridor.py); debiased rho [0.046,0.218], 48 layers",
    finite_k=None,  # k (units per layer) ~ hidden width; estimated, not measured
    note="chaos-side edge; framework calls this WEAK support, not a clean mid-corridor band",
))

# 2. fMRI functional-connectivity rho -- data_fmri/RESULTS.md
#    primary: p5-p95 band [0.168, 0.464] (the source's own corridor band).
#    companion: full debiased range [0.156, 0.645].
corridors.append(dict(
    name="fMRI FC rho (human neural)",
    kind="coordinated",
    rho=(0.168, 0.464),
    primary=log_width_ratio(0.168, 0.464),
    axis="rho-band (p5-p95) -> k_eff via 1/rho asymptotic",
    source="data_fmri/RESULTS.md; ABIDE-PCP n=139 controls; rho_debiased p5 0.168, p95 0.464",
    finite_k=("k=200 (CC200 parcellation)", 200),
    companion_full=("full range [0.156,0.645]", log_width_ratio(0.156, 0.645)),
))

# 3. TCGA healthy-tissue rho -- data_tcga/RESULT.md
#    pooled 6 primary cancers, 300 pathway-values: median 0.338, range [0.159, 0.625].
#    no clean pre-registered percentile band pooled; use the IQR-style p10/p90?
#    RESULT.md gives per-cancer p10/p90; pooled gives IQR [0.285,0.388] + range.
#    Primary: pooled full range [0.159, 0.625] is the only pooled two-bound band
#    explicitly stated. Companion: pooled IQR [0.285, 0.388].
corridors.append(dict(
    name="TCGA healthy-tissue rho (cellular)",
    kind="coordinated",
    rho=(0.159, 0.625),
    primary=log_width_ratio(0.159, 0.625),
    axis="rho-band (pooled range) -> k_eff via 1/rho asymptotic",
    source="data_tcga/RESULT.md; 6 primary cancers, 300 pathway-values; pooled range [0.159,0.625]",
    finite_k=("k~40-60 genes per Hallmark pathway; use k=50", 50),
    companion_full=("pooled IQR [0.285,0.388]", log_width_ratio(0.285, 0.388)),
))

# 4. Allen mouse-cortex rho -- data_allen/NOTES.md -- FALSIFIER
#    pooled debiased rho [0.008, 0.161], median 0.023; 60% sessions chaos-pinned.
#    Pre-registered falsifier. Excluded from the cluster statistic; reported.
corridors.append(dict(
    name="Allen mouse-cortex rho",
    kind="falsifier",
    rho=(0.008, 0.161),
    primary=log_width_ratio(0.008, 0.161),
    axis="rho-band -> k_eff via 1/rho asymptotic (FALSIFIER -- no corridor)",
    source="data_allen/NOTES.md; pooled debiased rho [0.008,0.161]; 60% sessions chaos-pole-pinned",
    finite_k=None,
    note="FALSIFIER: substrate sits AT the chaos pole, not in a corridor. "
         "The [0.008,0.161] span is a pole-pinned scatter, not a corridor band. "
         "Excluded from the cluster statistic per pre-registration.",
))

# 5. C. elegans rho -- corridor_dynamics/celegans/results_corridor_relaxation.json
#    30s window, 12 worms, per-worm rho_mean spans [0.264, 0.382].
celp = os.path.join(SS, "corridor_dynamics/celegans/results_corridor_relaxation.json")
with open(celp) as f:
    cel = json.load(f)
cel_rhos = sorted(v["rho_mean"] for v in cel["windows"]["30s"]["per_worm"].values())
corridors.append(dict(
    name="C. elegans rho (whole-brain neural)",
    kind="coordinated",
    rho=(cel_rhos[0], cel_rhos[-1]),
    primary=log_width_ratio(cel_rhos[0], cel_rhos[-1]),
    axis="rho-band (per-worm spread) -> k_eff via 1/rho asymptotic",
    source=("corridor_dynamics/celegans/results_corridor_relaxation.json; "
            f"30s window, {len(cel_rhos)} worms, rho_mean span "
            f"[{cel_rhos[0]:.3f},{cel_rhos[-1]:.3f}]"),
    finite_k=("k~107-125 neurons per worm; use k=115", 115),
    note="the relaxation-RATE measurement was a window-dominated null; the "
         "per-worm rho band is still a clean two-bound corridor measurement",
))

# 6. CMB shape-sector rho_l -- open_system_pomega/cmb_corridor_prediction.py
#    The corridor here is PREDICTED per-multipole from the A3+ k_eff band
#    [2.8, 4.8]; the natural multiplicative quantity is k_eff itself.
KEFF_LO, KEFF_HI = 2.8, 4.8
corridors.append(dict(
    name="CMB shape-sector corridor (k_eff)",
    kind="coordinated",
    rho=None,
    primary=log_width_ratio(KEFF_LO, KEFF_HI),
    axis="k_eff band directly (the corridor IS specified in k_eff)",
    source=("open_system_pomega/cmb_corridor_prediction.py; A3+-calibrated "
            f"k_eff corridor [{KEFF_LO}, {KEFF_HI}]"),
    finite_k=None,
    note="the CMB rho_l corridor is per-multipole (k=2l+1 varies); its "
         "substrate-independent specification is exactly the A3+ k_eff band",
))

# 7. A3+ within-rung corridor (recalibrated) -- open_system_pomega/corridor_recalculation.py
#    "CORRIDOR: |rho| ~ 0.16-0.35" and "k_eff ~ 2.5-5". rho-band primary;
#    k_eff band is the companion (and matches CMB's [2.8,4.8] within rounding).
corridors.append(dict(
    name="A3+ within-rung corridor (recalibrated)",
    kind="coordinated",
    rho=(0.16, 0.35),
    primary=log_width_ratio(0.16, 0.35),
    axis="rho-band -> k_eff via 1/rho asymptotic",
    source=("open_system_pomega/corridor_recalculation.py; 5 A3+ substrates; "
            "corridor |rho| ~ 0.16-0.35, k_eff ~ 2.5-5"),
    finite_k=None,
    companion_full=("stated k_eff band [2.5,5.0]", log_width_ratio(2.5, 5.0)),
    note="this is a cross-substrate ENVELOPE, not a single-substrate corridor; "
         "the rho-band and the k_eff-band log-widths are reported and differ "
         "(rho 0.16-0.35 are CENTRE values' span; k_eff 2.5-5 a corner band)",
))

# 8. Cross-rung g/J band -- open_system_pomega/crossrung_oom_band.py
#    OOM_BAND = (0.3, 3.0) -- already multiplicative.
corridors.append(dict(
    name="Cross-rung coupling g/J",
    kind="coordinated",
    rho=None,
    primary=log_width_ratio(0.3, 3.0),
    axis="g/J coupling ratio directly (already multiplicative)",
    source="open_system_pomega/crossrung_oom_band.py; OOM_BAND g/J = (0.3, 3.0)",
    finite_k=None,
    note="this is the corridor that motivated the hypothesis -- the cleanest "
         "exact-decade case; Path1 real systems sit mid-band g/J~0.7-1.15",
))

# 9. GPU substrate corridor -- CLAUDE.md -- the original anchor.
#    rho (0.10, 0.43); k_eff (2.33, 10).
corridors.append(dict(
    name="GPU substrate corridor (original anchor)",
    kind="reference",
    rho=(0.10, 0.43),
    primary=log_width_ratio(0.10, 0.43),
    axis="rho-band -> k_eff via 1/rho asymptotic",
    source="CLAUDE.md; original GPU calibration rho (0.10,0.43), k_eff (2.33,10)",
    finite_k=None,
    companion_full=("stated k_eff band [2.33,10]", log_width_ratio(2.33, 10.0)),
    note="single-substrate calibration; reported as the reference anchor. "
         "rho-axis and k_eff-axis log-widths differ -- see RESULT.md discussion",
))

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
print("=" * 78)
print("OOM CORRIDOR-WIDTH TEST -- per-corridor log-widths (decades)")
print("=" * 78)
print()
for c in corridors:
    print(f"  {c['name']}")
    print(f"    kind        : {c['kind']}")
    if c.get("rho"):
        print(f"    rho band    : [{c['rho'][0]:.3f}, {c['rho'][1]:.3f}]")
    print(f"    axis        : {c['axis']}")
    print(f"    PRIMARY width = {c['primary']:.3f} decades")
    if c.get("finite_k"):
        desc, k = c["finite_k"]
        lo, hi = c["rho"]
        fk = log_width_ratio(k_eff(k, hi), k_eff(k, lo))
        print(f"    finite-k    : {desc} -> finite-k k_eff width = {fk:.3f} decades")
    if c.get("companion_full"):
        desc, w = c["companion_full"]
        print(f"    companion   : {desc} -> width = {w:.3f} decades")
    if c.get("note"):
        print(f"    note        : {c['note']}")
    print(f"    source      : {c['source']}")
    print()

# ---------------------------------------------------------------------------
# Cluster criterion -- coordinated substrates only (pre-registered exclusion of
# the falsifier; the GPU 'reference' is reported but the criterion is applied
# to coordinated empirical corridors; GPU shown alongside).
# ---------------------------------------------------------------------------
coord = [c for c in corridors if c["kind"] == "coordinated"]
widths = [c["primary"] for c in coord]

print("=" * 78)
print("CLUSTER CRITERION (pre-registered)")
print("=" * 78)
print()
print("  Coordinated-substrate corridors entering the test:")
for c in coord:
    print(f"    {c['name']:<42} {c['primary']:.3f} decades")
print()
gpu = [c for c in corridors if c["kind"] == "reference"][0]
fal = [c for c in corridors if c["kind"] == "falsifier"][0]
print(f"  Reference (reported, not in statistic):")
print(f"    {gpu['name']:<42} {gpu['primary']:.3f} decades")
print(f"  Falsifier  (excluded per pre-registration -- pole-pinned, no corridor):")
print(f"    {fal['name']:<42} {fal['primary']:.3f} decades")
print()

wmin, wmax = min(widths), max(widths)
wmean = statistics.mean(widths)
wstd = statistics.stdev(widths)
all_in_band = all(0.6 <= w <= 1.5 for w in widths)
std_ok = wstd < 0.30

print(f"  n corridors          : {len(widths)}")
print(f"  width range          : [{wmin:.3f}, {wmax:.3f}] decades")
print(f"  width mean           : {wmean:.3f} decades")
print(f"  width sample std     : {wstd:.3f} decades")
print()
print(f"  (a) all widths in [0.6, 1.5] : {'PASS' if all_in_band else 'FAIL'}")
print(f"  (b) std < 0.30 decade        : {'PASS' if std_ok else 'FAIL'}")
print()
clustered = all_in_band and std_ok
verdict = "CLUSTERED at ~1 OOM" if clustered else "SCATTER"
print(f"  VERDICT: {verdict}")
print()
if clustered:
    print("  -> One order of magnitude IS a characteristic corridor width of the")
    print("     framework: every coordinated corridor measured is ~one decade wide.")
else:
    print("  -> The corridor log-widths do NOT cluster at one OOM. One-OOM is a")
    print("     property of specific corridors, not a framework-wide law.")
    out_of_band = [(c['name'], c['primary']) for c in coord
                   if not (0.6 <= c['primary'] <= 1.5)]
    if out_of_band:
        print("     out-of-band corridors:")
        for nm, w in out_of_band:
            print(f"       {nm}: {w:.3f} decades")
print()

# Dump machine-readable result
result = dict(
    corridors=[dict(name=c["name"], kind=c["kind"],
                    primary_width_decades=round(c["primary"], 4),
                    rho_band=c.get("rho"), source=c["source"])
               for c in corridors],
    coordinated_widths=[round(w, 4) for w in widths],
    width_range=[round(wmin, 4), round(wmax, 4)],
    width_mean=round(wmean, 4),
    width_std=round(wstd, 4),
    criterion_a_all_in_0p6_1p5=all_in_band,
    criterion_b_std_below_0p3=std_ok,
    verdict=verdict,
)
with open(os.path.join(HERE, "results_oom_widths.json"), "w") as f:
    json.dump(result, f, indent=1)
print(f"  machine-readable result -> results_oom_widths.json")

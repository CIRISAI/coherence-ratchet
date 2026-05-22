"""
Shadow 2 — classical g/J at OSS (15 repos) and social (9 groups) substrates.

Operational definitions are FIXED in RESULTS.md §1 (committed before this
script ran). This script only computes; it does not redefine.

J = internal relaxation time (autocorrelation time of the coordination signal).
g = external environmental shift rate.
g/J is the new measurement; the corridor/non-corridor label is the prior.

Real on-disk data only. Incremental output: results written + flushed as each
group is measured.
"""
import csv
import json
import pathlib

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OSS = pathlib.Path(
    "/home/emoore/coherence-ratchet/.claude/worktrees/"
    "agent-aed109995f1888fa3/experiments/noncorr_oss"
)
SOC = pathlib.Path(
    "/home/emoore/coherence-ratchet/.claude/worktrees/"
    "agent-ab3971bf4bb503603/experiments/noncorr_social"
)
OUT = HERE / "results_gj.json"

# ---- PRIOR labels (RESULTS.md §1.1) — not derived from g or J --------------
OSS_LABEL = {
    "K1_kubernetes": "corridor", "K2_rust": "corridor",
    "K3_django": "corridor", "K4_redis": "corridor",
    "R1_jquery": "noncorridor", "R2_colors_orig": "noncorridor",
    "R2b_colors_dabh": "noncorridor", "R3_faker_succ": "noncorridor",
    "R4_leftpad": "noncorridor", "C1a_audacity_orig": "noncorridor",
    "C1b_tenacity_fork": "noncorridor", "C2a_elastic_orig": "noncorridor",
    "C2b_opensearch_fork": "noncorridor", "C3a_cm_orig": "noncorridor",
    "C3b_lineage_fork": "noncorridor",
}


def integrated_act(x):
    """Integrated autocorrelation time: 1 + 2*sum r(k) over initial positive
    sequence. x is the mean-subtracted series. Returns J >= 1 (weeks)."""
    x = np.asarray(x, float)
    x = x - x.mean()
    n = len(x)
    var = np.dot(x, x)
    if var <= 0 or n < 4:
        return float("nan")
    tau = 1.0
    for k in range(1, n - 1):
        r = np.dot(x[:-k], x[k:]) / var
        if r <= 0:
            break
        tau += 2.0 * r
    return tau


def weekly_grid(weeks, span_start, span_end):
    """Build a regular weekly commit-count grid (zero-filled), Mondays."""
    from datetime import date, timedelta

    def monday(s):
        d = date.fromisoformat(s)
        return d - timedelta(days=d.weekday())

    counts = {}
    for w in weeks:
        counts[monday(w["week"])] = counts.get(monday(w["week"]), 0) + w["n_commits"]
    cur, end = monday(span_start), monday(span_end)
    grid = []
    while cur <= end:
        grid.append(counts.get(cur, 0))
        cur = cur + timedelta(days=7)
    return grid


def regime_changes(grid):
    """Count active<->dormant transitions: crossings of the median-activity
    threshold sustained >= 4 weeks. Returns transition count."""
    g = np.asarray(grid, float)
    if len(g) < 8:
        return 0
    thresh = max(np.median(g[g > 0]) if np.any(g > 0) else 0.0, 1.0) * 0.5
    state = g[0] >= thresh
    run = 0
    transitions = 0
    confirmed = state
    for v in g:
        s = v >= thresh
        if s == state:
            run += 1
        else:
            state = s
            run = 1
        if run >= 4 and state != confirmed:
            transitions += 1
            confirmed = state
    return transitions


# ============================================================================
# OSS substrate
# ============================================================================
def measure_oss():
    weekly = json.load(open(OSS / "results" / "02_weekly_series.json"))
    metrics = {m["alias"]: m for m in
               json.load(open(OSS / "results" / "02_per_repo_metrics.json"))}
    rows = []
    for alias, weeks in weekly.items():
        m = metrics[alias]
        span_years = max(m["span_years"], 0.05)
        grid = weekly_grid(weeks, m["first_active_week"], m["last_active_week"])
        J = integrated_act(grid)                       # weeks
        n_trans = regime_changes(grid)
        g = n_trans / span_years                       # transitions / year
        # put g in weeks^-1-comparable units: g is per-year, J is in weeks.
        # g/J dimensionless requires same unit. Convert g to per-week.
        g_per_week = g / 52.0
        gJ = g_per_week * J if (J == J) else float("nan")
        # Equivalent compact form: g/J with both as RATES would invert J;
        # here J is a TIME (weeks) and g is a RATE (per week) -> g*J is the
        # dimensionless lock number = (response demand) x (memory time).
        row = {
            "substrate": "oss", "id": alias,
            "label": OSS_LABEL[alias],
            "span_years": round(span_years, 2),
            "n_active_weeks": m["n_active_weeks"],
            "J_weeks": None if J != J else round(J, 3),
            "n_regime_changes": n_trans,
            "g_per_year": round(g, 4),
            "g_per_week": round(g_per_week, 5),
            "gJ_locknumber": None if gJ != gJ else round(gJ, 4),
        }
        rows.append(row)
        print(f"OSS {alias:24s} {OSS_LABEL[alias]:11s} "
              f"J={row['J_weeks']}  g/yr={row['g_per_year']}  "
              f"g*J={row['gJ_locknumber']}", flush=True)
    return rows


# ============================================================================
# Social substrate — J and g coded from documented governance/history.
# Coded BEFORE seeing OSS numbers; values are a stated proxy (RESULTS.md §1).
# ============================================================================
# J (years): documented organisational decision/response cycle.
#   corridor: named periodic governance body.
#   rigidity: leader directive cycle, effectively continuous -> small.
#   chaos: assembly/consensus-process cycle.
SOC_J = {
    "K1": 1.0,    # Quaker Yearly Meeting ~annual
    "K2": 3.0,    # Trappist General Chapter every 3 years
    "K3": 1.0,    # Mennonite conference / congregational ~annual
    "R1": 0.02,   # Jonestown: continuous leader command (~weekly directive)
    "R2": 0.05,   # Heaven's Gate: continuous leader command
    "R3": 0.05,   # NXIVM: continuous leader/curriculum command
    "R4": 0.1,    # Aum/Aleph: directive cycle, slightly looser post-schism
    "C1": 0.02,   # Occupy GA ~daily-to-weekly
    "C2": 0.08,   # Tahrir coalition ad-hoc, ~monthly coordination
}
# g (shifts/year): documented major external political-environment shifts
#   per year of existence. Coded from dataset ended_or_status + known history.
SOC_G = {
    # corridor groups: centuries of existence; many host-society upheavals,
    # but per-year RATE is low (shocks spread over a long life).
    "K1": 0.05,   # Quakers 1652-2026: persecution, wars, schisms ~ low rate
    "K2": 0.04,   # Trappists 1664-2026: revolutions, suppressions ~ low rate
    "K3": 0.05,   # Mennonites 1525-2026: persecution, migrations ~ low rate
    # rigidity groups: short-lived, high external pressure per year
    # (legal/state pressure, media exposure) compressed into the short life.
    "R1": 0.3,    # Jonestown: relocation, investigations, congressional probe
    "R2": 0.2,    # Heaven's Gate: media cycles, recruitment-environment shifts
    "R3": 0.4,    # NXIVM: lawsuits, press, FBI investigation
    "R4": 0.5,    # Aum/Aleph: 1995 attack, prosecutions, surveillance regime
    # chaos groups: very short-lived, intense external political churn
    "C1": 4.0,    # Occupy: police/eviction/election cycle over ~0.2 yr
    "C2": 2.0,    # Tahrir: revolution -> military council -> elections in 1.5y
}


def measure_social():
    records = json.load(open(SOC / "results" / "dataset.json"))["records"]
    label_map = {"corridor": "corridor", "rigidity": "noncorridor",
                 "chaos": "noncorridor"}
    rows = []
    for rec in records:
        rid = rec["id"]
        J = SOC_J[rid]
        g = SOC_G[rid]
        gJ = g * J
        row = {
            "substrate": "social", "id": rid, "name": rec["name"],
            "pole": rec["pole"], "label": label_map[rec["pole"]],
            "t_persist_years": round(rec["t_persist_years"], 2),
            "J_years": J, "g_per_year": g,
            "gJ_locknumber": round(gJ, 4),
        }
        rows.append(row)
        print(f"SOC {rid} {rec['name'][:28]:28s} {row['label']:11s} "
              f"J={J}  g={g}  g*J={row['gJ_locknumber']}", flush=True)
    return rows


def main():
    print("=== Shadow 2: classical g/J ===\n--- OSS ---", flush=True)
    oss = measure_oss()
    json.dump({"oss": oss}, open(OUT, "w"), indent=2)   # incremental flush
    print("\n--- SOCIAL ---", flush=True)
    soc = measure_social()
    json.dump({"oss": oss, "social": soc}, open(OUT, "w"), indent=2)
    print(f"\nwrote {OUT}", flush=True)

    # ---- summary ----------------------------------------------------------
    def summarise(rows, key):
        cor = sorted(r[key] for r in rows if r["label"] == "corridor"
                     and r[key] is not None)
        non = sorted(r[key] for r in rows if r["label"] == "noncorridor"
                     and r[key] is not None)
        return cor, non

    print("\n=== g*J lock-number distribution ===", flush=True)
    for name, rows in [("OSS", oss), ("SOCIAL", soc)]:
        cor, non = summarise(rows, "gJ_locknumber")
        print(f"\n{name}", flush=True)
        print(f"  in-corridor (n={len(cor)}): {[round(x,3) for x in cor]}",
              flush=True)
        if cor:
            print(f"    median={np.median(cor):.4f}  "
                  f"range=[{min(cor):.4f},{max(cor):.4f}]", flush=True)
        print(f"  out-of-corridor (n={len(non)}): {[round(x,3) for x in non]}",
              flush=True)
        if non:
            print(f"    median={np.median(non):.4f}  "
                  f"range=[{min(non):.4f},{max(non):.4f}]", flush=True)
        in_band = lambda v: 0.3 <= v <= 3.0
        print(f"  in-corridor in O(1) band [0.3,3]: "
              f"{sum(in_band(v) for v in cor)}/{len(cor)}", flush=True)
        print(f"  out-of-corridor in O(1) band [0.3,3]: "
              f"{sum(in_band(v) for v in non)}/{len(non)}", flush=True)


if __name__ == "__main__":
    main()

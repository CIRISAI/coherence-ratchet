# Fine-cadence galaxy subbox for the baryon-cycle detailed-balance test

**Goal:** find a fine-time-cadence open galaxy simulation so the baryon-cycle
detailed-balance test can run with `T >> dynamics timescale`. The prior gas run
(`spectral_galaxy_gas.py`, CAMELS IllustrisTNG CV_0) had only **T=16** usable
snapshots — even an *injected* driven NESS only reached z≈3.0 at that count, so a
genuine but modest cycle would sit below detection. The whole point was to escape
that.

**Outcome: no fine-cadence open gas time series is fetchable autonomously.** The
test was **not run** — this is the "valid outcome: report the precise data gap"
branch of the task. The estimator and the gas-matrix builder are ready; only
credentialed data is missing.

## What exists, its cadence, and why each is blocked

| Dataset | Fine cadence? | Cadence | Gas fields | Access | Blocker |
|---|---|---|---|---|---|
| **IllustrisTNG subboxes** (TNG50/100) | **yes (ideal)** | ~2400–7900 subbox snaps, **Δt ≈ 1–8 Myr** | PartType0, full | **gated** | `tng-project.org/api/` → HTTP 403; subbox endpoint → `"Failed session auth (and no API-Key sent)"`. Needs a free registered account + emailed **API key**. No key on disk/env; can't self-register + confirm email. |
| **FIRE-2 DR2** ("core" suite) | **yes (ideal)** | **601 snaps/sim**, z=99→0, **≈25 Myr** (MW-mass) | PartType0, full | **gated for download** | Directory *listing* is anonymous (601 snapdirs visible), but **every file returns HTTP 403** (any extension, Referer, UA). Real download is the **Globus** endpoint `d41e7ead-…` → needs Globus auth. Whole-snapshot-only granularity (no server-side gas/region cutout). |
| **CAMELS** IllustrisTNG (prior source) | no | **34 snaps total** | PartType0, full | **fully open** (anon HTTP, already used) | Cadence — this *is* the coarse limitation we're escaping. No finer CAMELS variant; CAMELS has no subboxes. |
| **AGORA** isolated disk | no | **2 outputs** (0 & 500 Myr) | yes | public | Only two time outputs — cannot test detailed balance. |

## The core obstruction

The two datasets with the cadence we need (TNG subboxes at ~1–8 Myr; FIRE-2 DR2 at
~25 Myr, 601 snapshots) both put the **actual particle/cell files behind
credentials** — TNG behind a per-account API key, FIRE-2 behind Globus
authentication (its plain-HTTP mirror lets you *browse* the 601 snapdirs but 403s
every download). The one fully-open source, CAMELS, tops out at 34 snapshots,
which is the exact coarse-cadence problem this task was meant to fix.

Local free disk is **43 GB**, so even if FIRE-2 files were HTTP-downloadable, a
Milky-Way-mass (m12) run's 601 whole snapshots would overflow it — a **dwarf**
(`m10q_res30`, `m09_res30`) plus a snapshot stride would fit, and FIRE dwarfs'
bursty inflow→burst→feedback→outflow→recycle is arguably the *cleanest* place to
look for a broken-DB baryon cycle. But the blocker there is **access, not size**.

## What would unblock it (analysis code already validated & ready)

1. **TNG (finest cadence, preferred):** user registers free at `tng-project.org`,
   provides the API key. Then fetch **only the target galaxy's gas cutout** per
   subbox snapshot for a few hundred subbox snapshots (region cutout keeps size
   modest), build the Eulerian disk-aligned gas-cell matrix, and run
   `ep.entropy_production` on the top collective modes **plus** the direct
   (log-density, log-T) configuration-plane winding.
2. **FIRE-2:** user authenticates Globus for endpoint
   `d41e7ead-0fca-4715-bc72-24630cebe04b`, then pull a **dwarf** (`m10q_res30`)
   gas at a snapshot stride (e.g. every 3rd → ~200 snapshots) to local disk. The
   existing Eulerian gas-cell builder in `spectral_galaxy_gas.py` runs unchanged
   on the longer snapshot list.

Either path drops straight into the validated pipeline
(`entropy_production.py`: null |z|≈1.5, limit cycle z=16.6, driven z=41; plus the
`spectral_galaxy.py` saturation core). The only missing ingredient is
credentialed access to fine-cadence gas.

**Artifacts:** `spectral_results_subbox.json`, `spectral_subbox_summary.md`.

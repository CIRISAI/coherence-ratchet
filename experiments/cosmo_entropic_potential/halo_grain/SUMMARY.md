# Halo-grain S(a): does the evolving coordinating-unit set flip the DESI sign?

Companion to `../s_of_a.py`. That calculation graded the cosmic entropic potential
`S(a) = -ln det C(a)` over a **fixed** set of comoving Eulerian **cells** and found
`S` **falling** (`w ~ -0.90`, thawing, `w >= -1` everywhere) -- in tension with DESI's
phantom-past CPL fit (`w0 = -0.838`, `wa = -0.62`).

**Hypothesis tested here (from the brief).** Fixed cells violate the framework's own
complete-unit discipline. The cosmic coordinating units are **halos**, and the halo
set **evolves**: halos form and **merge**. A merger is the rigidity direction -- unit
count `k` drops, survivors more correlated -- so a halo-grain `S(a)` might **rise**
where the cell-grain `S` falls, flipping `w(z)` toward the DESI (phantom) direction.

We tested this on **real N-body halo catalogs**, not a toy.

---

## Data

- **TNG www API: gated** (`www.tng-project.org/api/` returns HTTP 403 without a key --
  none available). **Fallback used: the public CAMELS Flatiron mirror**
  (`users.flatironinstitute.org/~camels/.../IllustrisTNG/CV/`), which serves the
  FoF/Subfind **group catalogs** (`groups_0XX.hdf5`) with no key. Same IllustrisTNG
  galaxy-formation physics; this is **real halo data, not a toy**.
- **Box:** 25 Mpc/h; **CAMELS CV fiducial cosmology** (Om=0.3, h=0.671, s8=0.8, ns=0.962).
- **10 snapshots**, z = 3.0 -> 0.0 (a = 0.25 -> 1.0).
- **Fields only** (ranged HDF5 reads): `GroupPos`, `Group_M_Crit200`, `Group_R_Crit200`.
- **Robustness:** headline variants re-run across **6 independent-phase boxes** (CV_0..CV_5)
  -- the decisive guard against 25-Mpc/h cosmic variance.

## Design choices

**One pipeline.** We monkeypatch the parent's tested `PowerSpectrum` / `xi_R` / `entropy_S`
machinery to the CAMELS cosmology, so halo grain and cell grain share one code path.

**The governing theoretical point (controls the result):** In the **normalized**
correlation matrix, **linear halo bias `b` cancels exactly**
(`delta_halo = b*delta_m => C_ij = b^2 xi_m/(b^2 sig^2) = xi_m/sig^2`), and the **growth
factor `D(a)` cancels** too. So a halo-grain `S(a)` can depart from the a-constant
linear-matter value **only** through: (1) **discreteness / shot noise**; (2) the **evolving
point set** -- unit count `k(a)` and separations `r_ij(a)`; (3) nonlinear/scale-dependent
bias (2nd order). This is why the bias-model choice (guard #5) does not move `C`: we report
Sheth-Tormen `b(M_thr,z)` (1e11: 1.83->0.96) for context, but it is projected out by
construction. Only channels (1)-(3) can rescue the hypothesis.

**Two operationalizations, both computed, x three thresholds (1e11, 1e12, 1e13 Msun/h):**

- **(A) Halos-as-tracers on fixed cells.** Field = halo-count contrast (unweighted and
  mass-weighted) in an 8^3 fixed comoving grid. `C_ij = A(a)*rho(r_ij)` off-diagonal,
  `C_ii = 1`, where `rho = xi_R/sig^2_R` is the fixed PSD cell shape and `A(a)` is the
  **clustering fraction** `(Var_total - shot)/Var_total` measured directly from the catalog
  at each snapshot. PSD-safe by construction (`C = A*rho + (1-A)*I`). Isolates how much of
  the unit field is genuine clustering vs Poisson discreteness.
- **(B) Units-as-units.** `k(a)` = number of halos above threshold; `C_ij = xi_R(r_ij)/sig^2_R`
  over the **actual halo positions** (PSD-safe: `xi_R` is the FT of a non-negative P(k), the
  model-xi route flagged in the brief). Report `S` **and** `S/k` (T-E3). Two variants:
  **B-total** (all halos, `k` grows with time) and **B-fixedk** (common subsample size across
  snapshots -> isolates geometry), averaged over random subsamples.

**Guards.** Min eigenvalue + condition number per snapshot; shot noise measured and
subtracted (A); numerical cap + averaged random draws (B); jackknife on `A`; 1e13 flagged
**volume-limited** (<=9 halos). Pointwise `dlnS/dlna` on 10 noisy points is unreliable, so
the headline uses a **robust global-slope** OLS fit of `ln S` vs `ln a` and its **spread
across 6 boxes**.

---

## The merger premise, checked against the actual mass function

The hypothesis needs `k` to **drop** through mergers. It does **not** at these thresholds
(z = 3.0 -> 0.0):

| threshold | k(z=3) -> k(z=0) | behaviour |
|-----------|-----------------|-----------|
| >1e11 Msun/h | 217 -> 398 (peak z~0.8) -> **364** | rises then mild ~9% late decline |
| >1e12 Msun/h | 11 -> **53** | rises, plateaus |
| >1e13 Msun/h | 0 -> **9** | rises monotonically (volume-limited) |

Meanwhile the most-massive halo grows **10x** (4.3e12 -> 4.5e13 Msun/h). Mergers
**concentrate mass**, but the cumulative unit count above a fixed threshold **grows or
plateaus** -- the "rigidity: k drops" premise is empirically **false** here.

## Per-variant sign table (multi-box, the robust view)

Global slope `dlnS/dlna` (mean +/- std over CV_0..CV_5); `w = -1 - slope/3`. Phantom <=> slope > 0.

| variant | thr | mean dlnS/dlna | mean w | across 6 boxes | phantom? |
|---------|-----|----------------|--------|----------------|----------|
| A halos-as-tracers (S) | 1e11 | -0.08 +/- 0.12 | **-0.973** | straddles 0 | no (~LCDM) |
| A halos-as-tracers (S) | 1e12 | -0.10 +/- 0.61 | -0.967 | undersampled | no (noisy) |
| B fixed-k geometry (S) | 1e11 | -0.24 +/- 0.08 | **-0.919** | **all 6 falling** | **no** |
| B fixed-k geometry (S) | 1e12 | -0.46 +/- 0.50 | -0.848 | undersampled | no (noisy) |
| B **total**, extensive in k (S) | 1e11 | +0.31 +/- 0.13 | **-1.103** | **all 6 rising** | **yes** |

Single-box pointwise `w0/wa` for every variant x weight x threshold are in
`results.json -> sign_table`; they are noise-dominated and not the basis of the verdict.

---

## Verdict

**The halo grain does NOT rescue the DESI phantom direction. It confirms the cell-grain
no-phantom (`w >= -1`) result.**

1. The merger premise (`k` drops) is **false** in the data (table above).
2. **Every intensive / fixed-unit measure** gives `w >= -1` **robustly across 6
   independent-phase boxes**: op A field `w ~ -0.97` (~ LCDM), op B fixed-k geometry
   `w ~ -0.92` with **all six boxes S-falling**. Same direction as the cell grain.
3. The **only** robustly S-rising variant is **B-total**, whose `S` is **extensive in the
   growing unit count `k`** (`w ~ -1.10`, all six boxes). Holding `k` fixed **reverses the
   sign**. So this "phantom" is **unit-counting bookkeeping, not increased coordination** --
   exactly what T-E3's intensive `S/k` is meant to strip out.

**Honest interpretive fork.** If one *insists* that `S_total` with a time-growing `k` is the
physical potential, then `w ~ -1.1` (mild phantom) *does* appear, robustly. Reasons we read
it as an artifact: the sign law was derived at **fixed k** (the cell grain); `-ln det` is
monotone in dimension for any correlated set, so comparing it across different `k` is not
apples-to-apples; and both the intensive `S/k` and the fixed-k geometry reverse it. A reader
who rejects the intensive convention could keep the hypothesis alive on this one channel --
we flag it rather than bury it.

## Caveats (honest)

- **Proxy.** `C` here is a modeled/measured **2-point** correlation matrix, not the
  framework's true coordination operator. Inherits the parent calculation's proxy disclaimer.
- **Volume.** The robust statement rests on the **1e11 threshold** -- the 25-Mpc/h box has
  too few >1e12 halos (1e13 volume-limited, <=9) to grain the merger-**dominated** regime the
  hypothesis actually targets. A larger box (TNG300 / big-volume sim) is the proper test of
  the high-threshold corner; unreachable without the gated API.
- **Halo definition dependence.** FoF + M200c + hard mass threshold; SO vs FoF or a
  merger-tree unit definition could shift amplitudes (not, we expect, the sign of the
  intensive measures).
- **Extensive/intensive convention** does real work in the verdict, as flagged above.

## Files
`halo_grain.py` . `results.json` . `figures/fig1_units_kz.png` (k(z) + Mmax(z)) .
`figures/fig2_opA.png` (clustering fraction & S) . `figures/fig3_opB.png` (S_total & S/k).

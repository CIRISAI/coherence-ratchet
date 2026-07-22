#!/usr/bin/env python3
import json, os, glob
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
def L(n): return json.load(open(os.path.join(HERE,n)))

print("="*78)
print("K4 DISCRIMINATOR SUMMARY  (R=8 Mpc/h, the clean scale)")
print("="*78)

# ---- COUNT field vs shot surrogates (poisson_results.json)
P=L("poisson_results.json")["snapshots"]
print("\n[1] COUNT field copula skew vs shot-noise surrogates (all 26 snaps), R8:")
print("     real_count | S0(cont) | S1(Poiss) | S1b(shotsub) | S2(lognorm) | z_vs_S1")
rc=[s["real"]["count_ngp_pos"]["8.0"] for s in P]
s0=[s["surr_mean"]["S0"]["8.0"] for s in P]; s1=[s["surr_mean"]["S1"]["8.0"] for s in P]
s1b=[s["surr_mean"]["S1b"]["8.0"] for s in P]; s2=[s["surr_mean"]["S2"]["8.0"] for s in P]
zc=[s["z_vs"]["S1"]["8.0"] for s in P]
print(f"     mean: {np.mean(rc):+.3f}   {np.mean(s0):+.3f}    {np.mean(s1):+.3f}     "
      f"{np.mean(s1b):+.3f}      {np.mean(s2):+.3f}     {np.mean(zc):+.2f}")
print(f"     z_vs_S1 range [{np.min(zc):+.2f},{np.max(zc):+.2f}]  "
      f"# snaps real MORE negative than S1: {sum(1 for s in P if s['real']['count_ngp_pos']['8.0']<s['surr_mean']['S1']['8.0'])}/26")
# fraction of real signal explained by S1 (relative to S0~0)
frac=np.mean([abs(s1[i])/abs(rc[i]) for i in range(len(rc))])
print(f"     S1 reproduces {100*frac:.0f}% of the count copula skew (S0 baseline ~0)")

# ---- MASS field vs its proper null (mass_results.json)  [the FROZEN measurement]
M=L("mass_results.json")["snapshots"]
print("\n[2] MASS-weighted field (THE FROZEN MEASUREMENT) vs mass-weighted shot null, R8:")
print("     real_mass | S0m(cont) | S1m(Poiss+randmass) | z_vs_S1m")
rm=[s["real"]["8.0"] for s in M]; s0m=[s["S0m_mean"]["8.0"] for s in M]
s1m=[s["S1m_mean"]["8.0"] for s in M]; zm=[s["z_vs_S1m"]["8.0"] for s in M]
print(f"     mean: {np.mean(rm):+.3f}   {np.mean(s0m):+.3f}     {np.mean(s1m):+.3f}          {np.mean(zm):+.2f}")
print(f"     z_vs_S1m range [{np.min(zm):+.2f},{np.max(zm):+.2f}]  "
      f"# snaps real MORE negative than S1m: {sum(1 for i in range(len(rm)) if rm[i]<s1m[i])}/26")
fracm=np.mean([abs(s1m[i])/abs(rm[i]) for i in range(len(rm))])
print(f"     S1m reproduces {100*fracm:.0f}% of the frozen copula skew (S0m baseline ~0)")

# combined-signal significance: mean z over snaps / (1/sqrt as independent-ish, but snaps correlated)
print(f"\n     [detection-vs-shot] mean z_vs_S1m (mass) = {np.mean(zm):+.2f} +- {np.std(zm)/np.sqrt(len(zm)):.2f} (SEM)")
print(f"     [detection-vs-shot] mean z_vs_S1  (count)= {np.mean(zc):+.2f} +- {np.std(zc)/np.sqrt(len(zc)):.2f} (SEM)")
print("     (positive/near-zero => real does NOT exceed the shot null => collapses)")

# ---- Tie-break control
print("\n[3] TIE-BREAK control (R8): positional (frozen) vs random")
cp=[s["real"]["count_ngp_pos"]["8.0"] for s in P]; cr=[s["real"]["count_ngp_rand"]["8.0"] for s in P]
mp=[s["real"]["mass_ngp_pos"]["8.0"] for s in P]; mr=[s["real"]["mass_ngp_rand"]["8.0"] for s in P]
print(f"     count: positional {np.mean(cp):+.3f}  random {np.mean(cr):+.3f}  (delta {np.mean(cr)-np.mean(cp):+.3f})")
print(f"     mass : positional {np.mean(mp):+.3f}  random {np.mean(mr):+.3f}  (delta {np.mean(mr)-np.mean(mp):+.3f})")

# ---- Assignment control NGP vs CIC
print("\n[4] ASSIGNMENT control (R8 and R4): NGP vs CIC (real fields)")
for R,lab in [("8.0","R8"),("4.0","R4"),("16.0","R16")]:
    cn=[s["real"]["count_ngp_pos"][R] for s in P]; cc=[s["real"]["count_cic_pos"][R] for s in P]
    mn=[s["real"]["mass_ngp_pos"][R] for s in P]; mc=[s["real"]["mass_cic_pos"][R] for s in P]
    print(f"   {lab}: count NGP {np.mean(cn):+.3f} CIC {np.mean(cc):+.3f} | mass NGP {np.mean(mn):+.3f} CIC {np.mean(mc):+.3f}")

# ---- also compare CIC-real vs S1: does anti-aliasing change the collapse verdict?
print("\n[5] Does CIC (anti-alias) change the picture? mass CIC vs S1m/S0m per snap (R8):")
mcic=[s["real"]["mass_cic_pos"]["8.0"] for s in P]
print(f"     mass CIC mean {np.mean(mcic):+.3f}  vs S1m mean {np.mean(s1m):+.3f} (S1m is count-based null; indicative)")
print("="*78)

"""Multi-box robustness of the B-total S(a) peak — my check, halo_grain.py's exact pipeline."""
import sys, numpy as np
sys.path.insert(0, "/home/emoore/coherence-ratchet/experiments/cosmo_entropic_potential/halo_grain")
sys.path.insert(0, "/home/emoore/coherence-ratchet/experiments/cosmo_entropic_potential")
import halo_grain as hg
import s_of_a as S

ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
THR = 1e11
peaks, w_tod = [], []
for cv in range(6):
    snaps = [hg.load_snapshot(s, cv=cv) for s in hg.SNAPS]
    recs = hg.op_B(ps, snaps, THR)           # B-total: k grows, exact same code path
    av = np.array([r["a"] for r in recs]); Sa = np.array([r["S"] for r in recs])
    ok = ~np.isnan(Sa); av, Sa = av[ok], Sa[ok]
    pk = av[np.argmax(Sa)]
    late = (np.log(Sa[-1]) - np.log(Sa[-2])) / (np.log(av[-1]) - np.log(av[-2]))
    peaks.append(pk); w_tod.append(-1 - late/3)
    print(f"CV_{cv}: peak a={pk:.3f} (z={1/pk-1:.2f})  S_end/S_peak={Sa[-1]/Sa.max():.3f}  w_today={-1-late/3:+.3f}")
peaks, w_tod = np.array(peaks), np.array(w_tod)
print(f"\ninterior peak (a<1): {(peaks<0.999).sum()}/6 boxes | peak z: {np.round(1/peaks-1,2)}")
print(f"w_today mean {w_tod.mean():+.3f} ± {w_tod.std():.3f} | boxes w_today>-1: {(w_tod>-1).sum()}/6")

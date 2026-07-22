#!/usr/bin/env bash
# PREDICTION 4 — wait for all chunk pulls to finish, then combine -> measure -> analyze.
# Detached-safe: every stage writes incrementally, so a kill only loses the current stage.
set -u
cd "$(dirname "$0")"
SIM=${P4_SIM:-TNG100-3}; SNAP=${P4_SNAP:-99}
P4=${P4_SCRATCH:-/tmp/claude-1000/-home-emoore-coherence-ratchet/047db89f-06e6-45f4-a014-34f932c0bc32/scratchpad/p4}
NF=$(python3 -c "import fetch_grid as F; print(F.NFILES)")

echo "[pipeline] waiting for $NF chunks of $SIM snap $SNAP ..."
while :; do
  n=$(python3 - <<PY
import numpy as np, glob
c=0
for f in glob.glob("$P4/part_${SIM}_$(printf %03d $SNAP)_*.npz"):
    try:
        if bool(np.load(f)["done"]): c+=1
    except Exception: pass
print(c)
PY
)
  echo "[pipeline] $(date +%H:%M:%S)  chunks done: $n/$NF"
  [ "$n" -ge "$NF" ] && break
  sleep 120
done

echo "[pipeline] combining ..."
P4_SIM=$SIM P4_SNAP=$SNAP python3 fetch_grid.py combine || exit 1
echo "[pipeline] measuring ..."
P4_SIM=$SIM P4_SNAP=$SNAP python3 measure.py || exit 1
echo "[pipeline] analyzing ..."
P4_SIM=$SIM P4_SNAP=$SNAP python3 analyze.py "results_${SIM}_$(printf %03d $SNAP).json"
echo "[pipeline] DONE"

#!/bin/bash
cd /home/emoore/coherence-ratchet/experiments/cosmo_entropic_potential/proxy_upgrade
# 1. wait for measured-C GPU job (PID passed as $1) to finish
while ps -p $1 >/dev/null 2>&1; do sleep 20; done
echo "[chain] s_measured_gpu exited $(date +%H:%M:%S)"
# 2. run comparison analysis (CPU)
python3 analyze_measured.py > analyze_measured.log 2>&1
echo "[chain] analyze done $(date +%H:%M:%S)"
# 3. run Abacus pipeline (acquires flock itself)
python3 abacus_run.py > abacus_run.log 2>&1
echo "[chain] abacus_run done $(date +%H:%M:%S)"
echo "[chain] ALL DONE"

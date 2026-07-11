#!/bin/bash
cd /home/emoore/coherence-ratchet/experiments/cosmo_entropic_potential/proxy_upgrade
while ps -p 3328031 >/dev/null 2>&1; do sleep 20; done
echo "[final] cpu_fallback done $(date +%H:%M:%S)"
python3 abacus_run_cpu.py > abacus_run_cpu.log 2>&1
echo "[final] abacus_cpu done $(date +%H:%M:%S)"
echo "[final] ALL DONE"

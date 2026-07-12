#!/usr/bin/env python3
"""CALIBRATION PROBE (no bet-relevant numbers): measure real GPU-timing-jitter
harvest throughput and low-bit entropy. Sizes the noise budget for the bench.
Real noise only: entropy is the timing jitter of a tiny GPU kernel launch+sync."""
import time, math
import numpy as np
import cupy as cp

# tiny timing kernel (same pattern as CIRISArray src/strain_gauge.py TimingKernel)
_mod = cp.RawModule(code=r'''
extern "C" __global__ void tk(float* d, int n, int it){
  int i = blockIdx.x*blockDim.x+threadIdx.x; if(i>=n) return;
  float x=d[i]; for(int k=0;k<it;k++){ x=x*0.99f+0.01f; } d[i]=x;
}''')
_k = _mod.get_function('tk')
_d = cp.random.randn(64, dtype=cp.float32)


def measure_ns():
    s = time.perf_counter_ns()
    _k((1,), (64,), (_d, cp.int32(64), cp.int32(10)))
    cp.cuda.Stream.null.synchronize()
    return time.perf_counter_ns() - s


N = 200000
t0 = time.perf_counter()
raw = np.empty(N, dtype=np.int64)
for i in range(N):
    raw[i] = measure_ns()
dt = time.perf_counter() - t0
rate = N / dt
print(f"harvested {N} timing samples in {dt:.2f}s  ->  {rate:.0f} samples/s")
print(f"timing ns: median={np.median(raw):.0f}  mean={raw.mean():.0f}  min={raw.min()}  p1={np.percentile(raw,1):.0f}  p99={np.percentile(raw,99):.0f}")

# low-bit entropy per bit position
for nb in (1, 2, 3, 4, 5, 6, 8):
    lsb = raw & ((1 << nb) - 1)
    vals, cnts = np.unique(lsb, return_counts=True)
    p = cnts / cnts.sum()
    H = -np.sum(p * np.log2(p))
    Hmin = -np.log2(p.max())
    print(f"  low {nb} bits: Shannon={H:.3f}/{nb}  min-entropy={Hmin:.3f}/{nb}  ({H/nb*100:.1f}% eff)")

# autocorrelation of low-4-bit stream (whiteness of raw physical stream)
lsb4 = (raw & 0xF).astype(np.float64)
lsb4 -= lsb4.mean()
ac1 = np.corrcoef(lsb4[:-1], lsb4[1:])[0, 1]
ac2 = np.corrcoef(lsb4[:-2], lsb4[2:])[0, 1]
print(f"  low-4-bit lag-1 autocorr={ac1:+.4f}  lag-2={ac2:+.4f}")

# normals throughput estimate: 32 bits/normal via Box-Muller from 4-bit chunks
bits_per_s = rate * 4  # using 4 low bits
normals_per_s = bits_per_s / 32.0
print(f"est real-jitter throughput: {bits_per_s/1000:.1f} kbps ; ~{normals_per_s:.0f} N(0,1)/s (32 bits each)")

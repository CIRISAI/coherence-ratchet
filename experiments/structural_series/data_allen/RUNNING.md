# How to reproduce this run

## Environment

`allensdk` (the Allen Brain Observatory client) does not build or import under
Python 3.12 — it needs `pkg_resources` (removed from setuptools >= 81) and old
build tooling. It installs cleanly under Python 3.10.

```sh
python3.10 -m venv --without-pip /tmp/allenenv
curl -s https://bootstrap.pypa.io/get-pip.py | /tmp/allenenv/bin/python -
/tmp/allenenv/bin/pip install allensdk "setuptools<81"
```

`setuptools<81` is mandatory — allensdk 2.16.2 imports `pkg_resources` at
module load time.

## Run

```sh
/tmp/allenenv/bin/python exp_allen_corridor.py
```

Downloads ~32 NWB session files (~13 GB total) into `/tmp/allen_data/` via the
Allen API (`api.brain-map.org`), then computes per-session within-rung ρ.
Results to `results.json`; verdict to stdout. ~10-15 min on a warm cache,
longer cold (download-bound).

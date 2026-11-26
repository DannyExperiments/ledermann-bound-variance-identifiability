# Reproducibility

Run from the repository root with Python 3.11 or later and Git.

~~~sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
~~~

The replay uses exact rational arithmetic to construct two PSD rank-r matrices at (p,r) = (10,6) and (15,10). It checks that the off-diagonals match, both kernels satisfy the regularity tests, the leading blocks admit the triangular normalization, and the positive variance vectors can produce identical covariances. It also verifies the projector and the exact worked noise slice. [Expected output](verification/logs/replay.txt)

[Build the manuscript](paper/BUILD.md) · [Rebuild the figure and offline explorer](visualization/README.md)

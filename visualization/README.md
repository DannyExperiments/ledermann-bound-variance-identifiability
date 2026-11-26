# Worked variance tradeoff

The ten-variable witness supplies two rank-six PSD signal matrices A and B. The matrix B − A is diagonal, with six entries equal to +1 followed by four equal to −1. In the covariance slice Σ = A + sI, the variances for A are all s. The variances for B are six copies of s − 1 and four copies of s + 1. Both decompositions have strictly positive variances for s > 1. At s = 1/2 one of the two chosen decompositions remains admissible.

The illustration tests the two chosen witnesses. The paper proves global uniqueness in a separate small-noise region and does not specify its endpoint. The [exact replay](../verification/src/replay.py) verifies the matrix identity, signs and strict positivity boundaries.

Extract the [offline explorer](variance-tradeoff-explorer.zip) and open index.html. Rebuild the ZIP and 704 × 830 GIF by running python3 visualization/render.py from the root with Python 3.11 or later, Pillow 13 and the Arial faces supplied with macOS. The optional --output argument writes the rebuilt files to another folder.

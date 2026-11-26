# Problem and proof

Which Ledermann equality pairs allow the real factor model to identify its positive diagonal variances for almost every parameter choice? The remaining cases have p = m(m + 1)/2 observed variables, r = p − m factors and m ≥ 4.

**Result.** Every remaining pair has an open region of ambiguity and an open region of uniqueness. Generic global identification fails, including in a fixed full triangular normalization up to column signs.

**Regularity.** At a rank-r PSD matrix A, project to its off-diagonal entries. If K is a kernel frame, the derivative is invertible exactly when the map h ↦ Kᵀ Diag(h) K is invertible. The rank-one matrices from coordinate rows and pairwise sums of coordinate rows certify generic invertibility.

**Ambiguity.** Choose a diagonal form with at least m positive and m negative directions. Its orthogonal positive and negative m-planes can both be chosen regular. On their direct sum with the orthogonal complement, build a PSD form vanishing on the first plane, while adding the diagonal form gives a second PSD form vanishing on the second plane. Both have rank r, and they share off-diagonal data. The inverse function theorem keeps both solutions under small perturbations. Choose the observed diagonal high enough that both variance diagonals are strictly positive.

**Uniqueness.** Use the orthogonal projector P onto the kernel of one regular completion A. Because every coordinate occurs in the kernel, η = minᵢ Pᵢᵢ is positive. Testing any nearby PSD competitor C against normalized vectors P eᵢ bounds its distance to A by (1 + 1/η) times the covariance perturbation. A sufficiently small covariance perturbation puts all rank-at-most-r competitors in the same local injectivity neighborhood. Strictly positive noise can be chosen there.

**Triangular form.** Nonsingular last kernel rows ensure a positive definite leading Gram block. Use its Cholesky factor to recover the triangular loadings up to column signs.

[Full proof](../paper/manuscript.pdf) · [Exact replay](../verification/src/replay.py)

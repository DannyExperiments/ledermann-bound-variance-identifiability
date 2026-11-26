"""Construct exact rational witnesses for the first two remaining Ledermann pairs."""

from fractions import Fraction
from itertools import combinations_with_replacement
from random import Random


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def multiply(left, right):
    columns = transpose(right)
    return [[sum(a * b for a, b in zip(row, column)) for column in columns] for row in left]


def diagonal(entries):
    return [[value if i == j else 0 for j in range(len(entries))]
            for i, value in enumerate(entries)]


def eliminate(matrix):
    result = [[Fraction(entry) for entry in row] for row in matrix]
    pivots = []
    for col in range(len(result[0])):
        i = len(pivots)
        pivot = next((j for j in range(i, len(result)) if result[j][col]), None)
        if pivot is None:
            continue
        result[i], result[pivot] = result[pivot], result[i]
        divisor = result[i][col]
        result[i] = [value / divisor for value in result[i]]
        for j, row in enumerate(result):
            if j != i and row[col]:
                coefficient = row[col]
                result[j] = [a - coefficient * b for a, b in zip(row, result[i])]
        pivots.append(col)
        if len(pivots) == len(result):
            break
    return result, pivots


def rank(matrix):
    return len(eliminate(matrix)[1])


def inverse(matrix):
    size = len(matrix)
    augmented = [a + b for a, b in zip(matrix, diagonal([1] * size))]
    reduced, pivots = eliminate(augmented)
    assert pivots == list(range(size))
    return [row[size:] for row in reduced]


def nullspace(matrix):
    reduced, pivots = eliminate(matrix)
    size = len(matrix[0])
    basis = []
    for free in sorted(set(range(size)) - set(pivots)):
        vector = [0] * size
        vector[free] = 1
        for i, pivot in enumerate(pivots):
            vector[pivot] = -reduced[i][free]
        basis.append(vector)
    return transpose(basis)


def positive_definite(matrix):
    if matrix != transpose(matrix):
        return False
    remaining = [[Fraction(entry) for entry in row] for row in matrix]
    while remaining:
        pivot = remaining[0][0]
        if pivot <= 0:
            return False
        remaining = [[row[j] - row[0] * remaining[0][j] / pivot
                      for j in range(1, len(remaining))]
                     for row in remaining[1:]]
    return True


def gram(matrix, form):
    return multiply(multiply(transpose(matrix), form), matrix)


def good(frame, m):
    pairs = tuple(combinations_with_replacement(range(m), 2))
    powers = [[row[i] * row[j] for i, j in pairs] for row in frame]
    return rank(frame[-m:]) == m and rank(powers) == len(powers)


def regular_frames(m, signs, rng):
    p = len(signs)
    form = diagonal(signs)
    for _ in range(250):
        k = [[100 * (i == j) + rng.randint(-3, 3) for j in range(m)] for i in range(p)]
        if not good(k, m):
            continue
        positive = gram(k, form)
        if not positive_definite(positive):
            continue
        last = [[100 * (i == p - m + j) + rng.randint(-3, 3) for j in range(m)] for i in range(p)]
        correction = multiply(multiply(k, inverse(positive)), multiply(multiply(transpose(k), form), last))
        ell = [[a - b for a, b in zip(row, delta)] for row, delta in zip(last, correction)]
        negative = gram(ell, diagonal([-sign for sign in signs]))
        if positive_definite(negative) and good(ell, m):
            assert multiply(multiply(transpose(k), form), ell) == [[0] * m for _ in range(m)]
            return k, ell, positive, negative
    raise AssertionError('no exact regular frame pair')


def check(m, rng):
    p = m * (m + 1) // 2
    r = p - m
    signs = [1] * r + [-1] * m
    form = diagonal(signs)
    k, ell, positive, negative = regular_frames(m, signs, rng)
    orthogonal_rows = multiply(transpose(k), form) + multiply(transpose(ell), form)
    u = nullspace(orthogonal_rows)
    frame = [a + b + c for a, b, c in zip(k, ell, u)]
    inverse_frame = inverse(frame)
    residual = gram(u, form)
    t = 1 + sum(abs(value) for row in residual for value in row)
    a_blocks = diagonal([0] * (2 * m) + [t] * (p - 2 * m))
    for i, row in enumerate(negative):
        for j, value in enumerate(row):
            a_blocks[m + i][m + j] = value
    a = gram(inverse_frame, a_blocks)
    b = [[value + (signs[i] if i == j else 0) for j, value in enumerate(row)]
         for i, row in enumerate(a)]
    block_check = gram(frame, b)
    remaining = [[(t if i == j else 0) + residual[i][j] for j in range(p - 2 * m)]
                 for i in range(p - 2 * m)]
    expected = diagonal([0] * p)
    for offset, block in ((0, positive), (2 * m, remaining)):
        for i, row in enumerate(block, offset):
            expected[i][offset:offset + len(row)] = row
    assert block_check == expected and positive_definite(remaining)
    assert rank(a) == rank(b) == r
    assert multiply(a, k) == multiply(b, ell) == [[0] * m for _ in range(p)]
    assert positive_definite([row[:r] for row in a[:r]])
    assert positive_definite([row[:r] for row in b[:r]])
    assert all(a[i][j] == b[i][j] for i in range(p) for j in range(p) if i != j)

    projector = multiply(multiply(k, inverse(multiply(transpose(k), k))), transpose(k))
    eta = min(projector[i][i] for i in range(p))
    assert projector == transpose(projector) and multiply(projector, projector) == projector
    assert multiply(a, projector) == diagonal([0] * p)
    assert 0 < eta <= 1
    for s in (Fraction(1, 2), Fraction(1), Fraction(2)):
        diagonal_a = [s] * p
        diagonal_b = [s - sign for sign in signs]
        sigma_a = [[value + (diagonal_a[i] if i == j else 0) for j, value in enumerate(row)]
                   for i, row in enumerate(a)]
        sigma_b = [[value + (diagonal_b[i] if i == j else 0) for j, value in enumerate(row)]
                   for i, row in enumerate(b)]
        assert sigma_a == sigma_b
        assert (min(diagonal_b) > 0) == (s > 1)
        if s > 1:
            assert max(diagonal_b) * eta <= s  # The projector bound with ||Delta||_2 = s.
    assert [2 - sign for sign in signs] == [1] * r + [3] * m
    print(f'p={p}, r={r}: two regular PSD completions, exact covariance match, and eta > 0.')


def main():
    rng = Random(404)
    for m in (4, 5):
        check(m, rng)
    print('Exact worked slice: both witnesses admissible at s=2, only witness A at s=1/2.')
    print('This slice check concerns the chosen pair; the proof establishes open global uniqueness.')


if __name__ == '__main__':
    main()

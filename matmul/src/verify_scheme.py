"""Independent exact verifier for bilinear matrix multiplication schemes.

Reads a scheme in the FastMatrixMultiplication / ternary_flip_graph JSON
format: n = [n1, n2, n3], m = rank, and coefficient matrices
  u: m x (n1*n2)   linear form in A (row-major a_ij),
  v: m x (n2*n3)   linear form in B (row-major b_jk),
  w: m x (n3*n1)   contribution of m_r to C^T (row-major over (k, i)).
The scheme is correct iff the Brent equations hold exactly over the integers:
  sum_r u[r][i,j] * v[r][j',k] * w[r][k',i'] = [j=j'][k=k'][i=i'].
Also multiplies random integer matrices as an end-to-end check.

Uses exact integer (or Fraction) arithmetic; no floating point.
Only checks schemes whose coefficients are integers or fractions ("z2": false).

usage: verify_scheme.py scheme.json [...]
"""
import json
import random
import sys
from fractions import Fraction


def as_num(x):
    return Fraction(x) if isinstance(x, str) else x


def brent_ok(n1, n2, n3, u, v, w):
    m = len(u)
    # group nonzeros for speed
    U = [[(idx, c) for idx, c in enumerate(row) if c] for row in u]
    V = [[(idx, c) for idx, c in enumerate(row) if c] for row in v]
    W = [[(idx, c) for idx, c in enumerate(row) if c] for row in w]
    T = {}
    for r in range(m):
        for a, cu in U[r]:
            for b, cv in V[r]:
                cuv = cu * cv
                for c, cw in W[r]:
                    key = (a, b, c)
                    T[key] = T.get(key, 0) + cuv * cw
    target = {}
    for i in range(n1):
        for j in range(n2):
            for k in range(n3):
                target[(i * n2 + j, j * n3 + k, k * n1 + i)] = 1
    keys = set(T) | set(target)
    bad = [key for key in keys if T.get(key, 0) != target.get(key, 0)]
    return not bad, len(bad)


def multiply_check(n1, n2, n3, u, v, w, trials=3):
    rng = random.Random(0)
    for _ in range(trials):
        A = [[rng.randint(-9, 9) for _ in range(n2)] for _ in range(n1)]
        B = [[rng.randint(-9, 9) for _ in range(n3)] for _ in range(n2)]
        C = [[0] * n3 for _ in range(n1)]
        for r in range(len(u)):
            la = sum(u[r][i * n2 + j] * A[i][j] for i in range(n1) for j in range(n2))
            lb = sum(v[r][j * n3 + k] * B[j][k] for j in range(n2) for k in range(n3))
            p = la * lb
            if p:
                for k in range(n3):
                    for i in range(n1):
                        c = w[r][k * n1 + i]
                        if c:
                            C[i][k] += c * p
        true = [[sum(A[i][j] * B[j][k] for j in range(n2)) for k in range(n3)] for i in range(n1)]
        if C != true:
            return False
    return True


def verify(path):
    d = json.load(open(path))
    n1, n2, n3 = d["n"]
    if d.get("z2"):
        return f"{path}: SKIPPED (Z2 scheme; lift it first)"
    u = [[as_num(x) for x in row] for row in d["u"]]
    v = [[as_num(x) for x in row] for row in d["v"]]
    w = [[as_num(x) for x in row] for row in d["w"]]
    m = len(u)
    assert m == d["m"] == len(v) == len(w), "rank mismatch"
    assert all(len(r) == n1 * n2 for r in u) and all(len(r) == n2 * n3 for r in v) \
        and all(len(r) == n3 * n1 for r in w), "shape mismatch"
    ok, nbad = brent_ok(n1, n2, n3, u, v, w)
    mult = multiply_check(n1, n2, n3, u, v, w)
    coeffs = sorted({x for M in (u, v, w) for row in M for x in row})
    status = "VALID" if ok and mult else "INVALID"
    return (f"{path}: {status}  format {n1}x{n2}x{n3}, rank {m}, Brent "
            f"{'ok' if ok else f'FAILS ({nbad} equations)'}, random multiply "
            f"{'ok' if mult else 'FAILS'}, coefficients {coeffs[:8]}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(verify(p))

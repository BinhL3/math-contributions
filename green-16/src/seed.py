"""Seeds for x + 3y = 2z + 2w, following Hametner-Solymosi (arXiv 2609.13972).

We write the equation as L(x, y, z, w) = x + 3y - 2z - 2w = 0.  Its only
trivial solutions are x = y = z = w (no proper sub-block of the coefficients
1, 3, -2, -2 sums to 0, and that stays true mod m when gcd(m, 6) = 1).

A seed is a set A in G = (Z_m)^r with weight functions f1..f4 : A -> R
such that
    f1(a) + f2(a) + f3(a) + f4(a) = 0          for every a in A,
    f1(x) + f2(y) + f3(z) + f4(w) >= 1          for every solution in A^4
                                                that is not all-equal.
A seed of size k in (Z_m)^r gives good sets of size N^(alpha - o(1)) with
alpha = log(k) / (r * log(m)).  Being a seed is hereditary (subsets of seeds
are seeds), and existence of the weights is a linear program.
"""
import itertools
import math

import numpy as np
from scipy.optimize import linprog

RECORD = math.log(15) / (3 * math.log(5))  # 0.5608687...


def exponent(k, m, r):
    return math.log(k) / (r * math.log(m))


def solutions(A, m):
    """Non-all-equal solutions of x + 3y = 2z + 2w (mod m, coordinatewise)
    with x, y, z, w in A, as index tuples."""
    A = [tuple(a) for a in A]
    index = {a: i for i, a in enumerate(A)}
    inv2 = pow(2, -1, m)
    sols = []
    for (i, x), (j, y), (k, z) in itertools.product(enumerate(A), repeat=3):
        w = tuple(((xi + 3 * yi - 2 * zi) * inv2) % m for xi, yi, zi in zip(x, y, z))
        l = index.get(w)
        if l is not None and not (i == j == k == l):
            sols.append((i, j, k, l))
    return sols


def seed_weights(A, m):
    """Return weights (4 x |A| array) proving A is a seed, or None."""
    k = len(A)
    sols = solutions(A, m)
    if not sols:
        return np.zeros((4, k))
    # variables: f[v][a] at column v*k + a
    A_ub = np.zeros((len(sols), 4 * k))
    for row, s in enumerate(sols):
        for v, a in enumerate(s):
            A_ub[row, v * k + a] -= 1  # -(f1(x)+f2(y)+f3(z)+f4(w)) <= -1
    A_eq = np.zeros((k, 4 * k))
    for a in range(k):
        for v in range(4):
            A_eq[a, v * k + a] = 1
    res = linprog(np.zeros(4 * k), A_ub=A_ub, b_ub=-np.ones(len(sols)),
                  A_eq=A_eq, b_eq=np.zeros(k), bounds=(None, None),
                  method="highs")
    return res.x.reshape(4, k) if res.status == 0 else None


def is_seed(A, m):
    return seed_weights(A, m) is not None


def verify_exact(A, m, f):
    """Check integer weights exactly (no floating point)."""
    for a in range(len(A)):
        if sum(f[v][a] for v in range(4)) != 0:
            return False
    return all(sum(f[v][s[v]] for v in range(4)) > 0 for s in solutions(A, m))


# The 15-point seed in (Z_5)^3 from Hametner-Solymosi, with their f.
# In their notation L = 3x + y - 2z - 2w and f1 = f3 = f4 = f, f2 = -3f;
# in ours the coefficient-3 variable is y, so f2 = f3 = f4 = f, f1 = -3f.
PAPER_SEED = {
    (1, 0, 1): 183, (0, 1, 1): 61, (3, 3, 2): 23, (0, 3, 4): 8, (1, 1, 4): 8,
    (4, 4, 2): 2, (2, 0, 0): 3, (1, 4, 0): 2, (1, 1, 3): 3, (4, 0, 1): 1,
    (0, 1, 2): 1, (3, 3, 3): 0, (2, 0, 3): 1, (0, 2, 2): 2, (0, 3, 1): 0,
}

if __name__ == "__main__":
    A = list(PAPER_SEED)
    f = [PAPER_SEED[a] for a in A]
    weights = [[-3 * v for v in f], f, f, f]
    print("paper seed, their weights, exact check:", verify_exact(A, 5, weights))
    print("paper seed, LP check:", is_seed(A, 5))
    print(f"exponent {exponent(15, 5, 3):.7f}")
    parabola = [(x, x * x % 5) for x in range(5)]
    print("Ruzsa parabola in (Z_5)^2 has no solutions:", not solutions(parabola, 5))

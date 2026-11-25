"""Quick, dependency-free check of the new A398785 terms.

For each n, checks that the witness is an n-subset of {1..a(n)} with no
pairwise distinct solution to x + 3y = 2z + 2w.  (The matching lower bounds,
that no n-subset of {1..a(n)-1} works, are the DRAT certificates produced by
certify.py.)
"""
from check import bad_witness

TERMS = {
    16: (82, [1, 2, 3, 4, 14, 15, 16, 17, 66, 67, 71, 72, 76, 77, 81, 82]),
    17: (91, [1, 2, 3, 4, 5, 17, 18, 19, 20, 74, 76, 79, 81, 84, 86, 89, 91]),
    18: (97, [1, 2, 6, 7, 11, 12, 16, 17, 21, 77, 81, 82, 86, 87, 91, 92, 96, 97]),
}

if __name__ == "__main__":
    for n, (N, A) in TERMS.items():
        assert len(set(A)) == n and min(A) >= 1 and max(A) == N
        w = bad_witness(A)
        assert w is None, (n, w)
        print(f"a({n}) = {N}: witness OK ({n} elements, no solution)")

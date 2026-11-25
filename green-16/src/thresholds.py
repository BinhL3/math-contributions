"""Compute a(n) = least N such that some n-element subset of {1..N} is good
(OEIS A398785) with a SAT solver.

At N = a(n) every witness contains both 1 and N (otherwise it shifts into
{1..N-1}), so we force those two in.  The equation is also invariant under
x -> N+1-x, which we use for a light symmetry break.

usage: thresholds.py [max_n] [start_n start_N]
"""
import sys
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

from check import forbidden_quads, is_good

OEIS = [1, 2, 3, 4, 5, 8, 14, 17, 20, 22, 32, 37, 55, 64, 73]


def solve(n, N):
    clauses = [[-v for v in q] for q in forbidden_quads(N)]
    card = CardEnc.atleast(lits=list(range(1, N + 1)), bound=n,
                           top_id=N, encoding=EncType.seqcounter)
    s = Cadical195(bootstrap_with=clauses + card.clauses)
    assumptions = [1, N] if n >= 2 else [1]
    ok = s.solve(assumptions=assumptions)
    model = [v for v in s.get_model()[:N] if v > 0] if ok else None
    s.delete()
    return model


def main():
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    while n <= max_n:
        t = time.time()
        A = solve(n, N)
        dt = time.time() - t
        if A is None:
            print(f"  n={n} N={N} UNSAT ({dt:.1f}s)", flush=True)
            N += 1
            continue
        assert len(A) >= n and is_good(A), A
        tag = ""
        if n <= len(OEIS):
            tag = "matches OEIS" if OEIS[n - 1] == N else f"MISMATCH (OEIS {OEIS[n-1]})"
        print(f"a({n}) = {N}  {tag}  witness={A}  ({dt:.1f}s)", flush=True)
        n += 1
        N += 1


if __name__ == "__main__":
    main()

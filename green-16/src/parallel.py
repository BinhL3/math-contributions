"""Decide, for one n and a range of N, whether a good n-set in {1..N}
containing 1 and N exists. Each N runs in its own process.
a(n) = smallest SAT N, once every smaller N (>= a(n-1)+1) is UNSAT.

usage: parallel.py n N_lo N_hi [workers]
"""
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from check import is_good
from thresholds import solve


def job(args):
    n, N = args
    t = time.time()
    A = solve(n, N)
    if A is not None:
        assert len(A) >= n and is_good(A)
    return N, A, time.time() - t


def main():
    n, lo, hi = map(int, sys.argv[1:4])
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 12
    with ProcessPoolExecutor(workers) as ex:
        futs = [ex.submit(job, (n, N)) for N in range(lo, hi + 1)]
        for f in as_completed(futs):
            N, A, dt = f.result()
            res = f"SAT witness={A}" if A else "UNSAT"
            print(f"n={n} N={N} {res} ({dt:.0f}s)", flush=True)


if __name__ == "__main__":
    main()

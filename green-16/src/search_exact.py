"""Exhaustive search for the largest seed in (Z_m)^r (small groups only).

Depth-first over sets in a fixed element order, pruning any set that is not
a seed (seeds are hereditary).  By translation invariance we fix 0 in A.

usage: search_exact.py m r [target]
  stops early once a seed of size `target` is found.
"""
import itertools
import sys
import time

from seed import RECORD, exponent, is_seed


def main():
    m, r = int(sys.argv[1]), int(sys.argv[2])
    target = int(sys.argv[3]) if len(sys.argv) > 3 else None
    G = [g for g in itertools.product(range(m), repeat=r)]
    zero = G[0]
    rest = G[1:]
    best = [[zero]]
    t0 = time.time()
    nodes = 0

    def dfs(A, start):
        nonlocal nodes
        nodes += 1
        if len(A) > len(best[0]):
            best[0] = list(A)
            e = exponent(len(A), m, r)
            flag = "  BEATS RECORD" if e > RECORD else ""
            print(f"  size {len(A)} (exponent {e:.4f}){flag}: {A}  [{time.time()-t0:.0f}s]",
                  flush=True)
            if target and len(A) >= target:
                raise StopIteration
        for i in range(start, len(rest)):
            if len(A) + len(rest) - i <= len(best[0]):
                return
            A.append(rest[i])
            if is_seed(A, m):
                dfs(A, i + 1)
            A.pop()

    try:
        dfs([zero], 0)
        status = "exhaustive: this is the maximum"
    except StopIteration:
        status = "stopped at target"
    print(f"m={m} r={r}: best size {len(best[0])}, {status}, {nodes} nodes, "
          f"{time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()

"""Check every connected graph on n vertices (nauty geng), split res/mod.

Connected graphs suffice: tau adds over components, and H is subadditive
(H(a+b) <= H(a)+H(b), via disjoint unions of triangle-free graphs), so
n - H(n) >= sum (n_i - H(n_i)) and a disconnected counterexample would have a
counterexample component.

usage: exhaustive.py n workers
"""
import subprocess
import sys
import time
from pathlib import Path
from collections import Counter
from multiprocessing import Pool

from e151 import bound, decode_g6, tau


def job(args):
    n, res, mod = args
    b = bound(n)
    p = subprocess.Popen(["geng", "-cq", str(n), f"{res}/{mod}"],
                         stdout=subprocess.PIPE, text=True)
    dist, tight, bad = Counter(), [], []
    for line in p.stdout:
        adj = decode_g6(line)
        t = tau(adj, cap=b)  # returns b+1 if tau > b
        dist[t] += 1
        if t == b:
            tight.append(line.strip())
        if t > b:
            bad.append(line.strip())
    return dist, tight, bad


def main():
    n, workers = int(sys.argv[1]), int(sys.argv[2])
    mod = workers * 8
    t0 = time.time()
    total, tight, bad = Counter(), [], []
    with Pool(workers) as pool:
        for d, t, b in pool.imap_unordered(job, [(n, r, mod) for r in range(mod)]):
            total += d
            tight += t
            bad += b
    print(f"n={n}: {sum(total.values())} connected graphs, bound n-H(n)={bound(n)}, "
          f"{time.time()-t0:.0f}s")
    print("  tau distribution:", dict(sorted(total.items())))
    out = Path(__file__).parent.parent / "results" / f"tight_n{n}.g6"
    out.parent.mkdir(exist_ok=True)
    out.write_text("".join(g + "\n" for g in sorted(tight)))
    print(f"  {len(tight)} graphs at the bound saved to {out.name}")
    print("  COUNTEREXAMPLES:" if bad else "  no counterexample", bad[:20])


if __name__ == "__main__":
    main()

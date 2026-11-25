"""Randomized local search for large seeds in (Z_m)^r.

Iterated greedy: grow a seed by adding random points that keep it a seed;
when stuck, remove a few random points and regrow.  Keeps the best seed seen.
Independent workers use different random streams.

usage: search_local.py m r seconds workers [kick]
"""
import itertools
import json
import random
import sys
import time
from multiprocessing import Pool
from pathlib import Path

from seed import RECORD, exponent, is_seed

OUT = Path(__file__).parent.parent / "results" / "seed-search"


def grow(S, G, m, rng):
    cand = [g for g in G if g not in S]
    rng.shuffle(cand)
    for g in cand:
        if is_seed(S + [g], m):
            S = S + [g]
    return S


def worker(args):
    m, r, seconds, seed_no, kick = args
    rng = random.Random(seed_no)
    G = list(itertools.product(range(m), repeat=r))
    start = [G[0]]
    if m == 5 and r == 4:
        # product of the paper's 15-point seed with the 2-point seed {0, 1}
        # in Z_5 is a 30-point seed; grow from it
        from seed import PAPER_SEED
        start = [a + (b,) for a in PAPER_SEED for b in (0, 1)]
        assert is_seed(start, m)
    S = grow(start, G, m, rng)
    best = list(S)
    t_end = time.time() + seconds
    while time.time() < t_end:
        T = list(S)
        for _ in range(rng.randint(1, kick)):
            T.pop(rng.randrange(len(T)))
        T = grow(T, G, m, rng)
        if len(T) >= len(S):  # accept sideways moves to drift on plateaus
            S = T
        if len(S) > len(best):
            best = list(S)
            e = exponent(len(best), m, r)
            print(f"[w{seed_no}] size {len(best)} exp {e:.4f}"
                  f"{'  BEATS RECORD' if e > RECORD else ''}", flush=True)
            OUT.mkdir(exist_ok=True)
            with open(OUT / f"best_m{m}_r{r}.jsonl", "a") as fh:
                fh.write(json.dumps({"m": m, "r": r, "size": len(best),
                                     "set": best}) + "\n")
    return len(best), best


if __name__ == "__main__":
    m, r, seconds, workers = map(int, sys.argv[1:5])
    kick = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    with Pool(workers) as p:
        results = p.map(worker, [(m, r, seconds, i, kick) for i in range(workers)])
    sizes = sorted(s for s, _ in results)
    print(f"m={m} r={r}: best sizes per worker {sizes}; overall max {sizes[-1]} "
          f"(exponent {exponent(sizes[-1], m, r):.4f}, record {RECORD:.4f})")

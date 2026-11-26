"""Option A: local search for graphs with large tau(G), seeded from
extremal triangle-free (Ramsey) graphs.

Score = (tau(G) - bound(n)) * 1000 + number of triangles (capped).  tau is the
main objective; among graphs at the bound we drift toward more triangles, to
probe whether triangles can ever push tau past the bound.

Moves: flip one or two random pairs.  Accept if score does not drop, or with
small probability anyway (annealing).  Every graph reaching tau > bound is
re-checked with the brute-force tau and saved.

usage: search.py n seconds workers [seed]
  seed: "random" (default) or a circulant "C13:1,5"
"""
import json
import math
import random
import sys
import time
from multiprocessing import Pool
from pathlib import Path

from e151 import bound, edge_cliques, tau
from fast import tau_exact
from families import circulant

OUT = Path(__file__).parent.parent / "results"


def triangles(adj):
    return sum(1 for c in edge_cliques(adj) if bin(c).count("1") >= 3)


def score(adj, b):
    t = tau_exact(adj, b + 1)
    return (t - b) * 1000 + min(triangles(adj), 200), t


def to_g6(adj):
    n = len(adj)
    bits = [(adj[i] >> j) & 1 for j in range(1, n) for i in range(j)]
    bits += [0] * (-len(bits) % 6)
    return chr(n + 63) + "".join(chr(63 + int("".join(map(str, bits[k:k + 6])), 2))
                                 for k in range(0, len(bits), 6))


def start_graph(n, seed, rng):
    if seed.startswith("C"):
        m, S = seed[1:].split(":")
        g = circulant(int(m), [int(s) for s in S.split(",")])
        # pad with new vertices (or drop) to reach n
        g = g[:n] + [0] * max(0, n - len(g))
        mask = (1 << n) - 1
        return [x & mask for x in g]
    p = rng.uniform(0.15, 0.5)
    adj = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
    return adj


def worker(args):
    n, seconds, wid, seed = args
    rng = random.Random(wid * 7919 + n)
    b = bound(n)
    g = start_graph(n, seed, rng)
    s, t = score(g, b)
    best = (s, t, list(g))
    temp = 30.0
    t_end = time.time() + seconds
    found = []
    steps = 0
    while time.time() < t_end:
        steps += 1
        h = list(g)
        for _ in range(rng.choice((1, 1, 2))):
            i, j = rng.sample(range(n), 2)
            h[i] ^= 1 << j
            h[j] ^= 1 << i
        s2, t2 = score(h, b)
        if s2 >= s or rng.random() < math.exp((s2 - s) / temp):
            g, s, t = h, s2, t2
            if s > best[0]:
                best = (s, t, list(g))
            if t > b:
                assert tau(g) > b, "fast tau disagrees with brute force"
                found.append(to_g6(g))
                print(f"[w{wid}] COUNTEREXAMPLE n={n} tau={t} > {b}: {to_g6(g)}", flush=True)
        temp = max(1.0, temp * 0.9995)
        if steps % 20000 == 0:  # restart from the best, re-heat
            g, s, t = list(best[2]), best[0], best[1]
            temp = 30.0
    s, t, g = best
    return {"worker": wid, "tau": t, "bound": b, "triangles": triangles(g),
            "steps": steps, "g6": to_g6(g), "counterexamples": found}


def main():
    n, seconds, workers = map(int, sys.argv[1:4])
    seed = sys.argv[4] if len(sys.argv) > 4 else "random"
    with Pool(workers) as p:
        res = p.map(worker, [(n, seconds, w, seed) for w in range(workers)])
    b = bound(n)
    taus = sorted(r["tau"] for r in res)
    tight = [r for r in res if r["tau"] == b]
    max_tri = max((r["triangles"] for r in tight), default=None)
    bad = [g for r in res for g in r["counterexamples"]]
    print(f"n={n} seed={seed}: bound {b}; best tau per worker {taus}; "
          f"most triangles in a graph at the bound: {max_tri}; "
          f"counterexamples: {len(bad)}", flush=True)
    OUT.mkdir(exist_ok=True)
    with open(OUT / "search_runs.jsonl", "a") as fh:
        fh.write(json.dumps({"n": n, "seed": seed, "seconds": seconds,
                             "results": res}) + "\n")


if __name__ == "__main__":
    main()

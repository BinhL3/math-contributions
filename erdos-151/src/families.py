"""Option C: test structured graph families against tau(G) <= n - H(n).

Families: all circulant graphs C_n(S) for n <= NMAX, Paley graphs, Kneser
graphs K(m, k), and Mycielski iterates of small graphs.  Prints the slack
bound(n) - tau(G) for the tightest members, and any counterexample.

usage: families.py NMAX
"""
import itertools
import sys
from collections import defaultdict

from e151 import H, bound
from fast import tau_exact, tau_le


def circulant(n, S):
    adj = [0] * n
    for v in range(n):
        for s in S:
            for u in ((v + s) % n, (v - s) % n):
                if u != v:
                    adj[v] |= 1 << u
    return adj


def paley(q):
    sq = {(x * x) % q for x in range(1, q)}
    return circulant(q, sorted(s for s in sq if s <= q // 2))


def kneser(m, k):
    V = [frozenset(c) for c in itertools.combinations(range(m), k)]
    n = len(V)
    adj = [0] * n
    for i, j in itertools.combinations(range(n), 2):
        if not V[i] & V[j]:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    return adj


def mycielski(adj):
    n = len(adj)
    N = 2 * n + 1
    new = [0] * N
    for v in range(n):
        for u in range(n):
            if (adj[v] >> u) & 1:
                new[v] |= 1 << u
                new[v] |= 1 << (n + u)      # v ~ shadow of u
                new[n + u] |= 1 << v
        new[n + v] |= 1 << (2 * n)          # shadow ~ apex
        new[2 * n] |= 1 << (n + v)
    return new


def connected(adj):
    seen, stack = 1, [0]
    while stack:
        v = stack.pop()
        nb = adj[v] & ~seen
        seen |= nb
        while nb:
            u = (nb & -nb).bit_length() - 1
            nb &= nb - 1
            stack.append(u)
    return seen == (1 << len(adj)) - 1


def report(name, adj, stats):
    n = len(adj)
    if n >= 40 or not connected(adj):
        return
    b = bound(n)
    if not tau_le(adj, b):
        print(f"COUNTEREXAMPLE {name}: n={n}, tau > {b}", flush=True)
        stats["bad"].append(name)
        return
    t = tau_exact(adj, b)
    stats[n].append((b - t, name))


def summarize(stats, n):
    if stats[n]:
        best = sorted(stats[n])[:3]
        print(f"n={n:2d} bound={bound(n):2d} H={H(n)}: {len(stats[n])} graphs, "
              f"min slack {best[0][0]} e.g. {[x[1] for x in best]}", flush=True)


def main():
    NMAX = int(sys.argv[1])
    stats = defaultdict(list)
    stats["bad"] = []
    for n in range(5, NMAX + 1):
        half = list(range(1, n // 2 + 1))
        for r in range(1, len(half) + 1):
            for S in itertools.combinations(half, r):
                report(f"C{n}{list(S)}", circulant(n, S), stats)
        summarize(stats, n)
    print("--- other families", flush=True)
    done = set(stats) - {"bad"}
    for q in (5, 13, 17, 29, 37):
        report(f"Paley({q})", paley(q), stats)
    for m, k in ((5, 2), (6, 2), (7, 2), (7, 3), (8, 2), (8, 3)):
        report(f"Kneser({m},{k})", kneser(m, k), stats)
    g = circulant(5, [1])
    for i in range(2):
        g = mycielski(g)
        report(f"Mycielski^{i+1}(C5)", g, stats)
    for n in sorted(k for k in stats if k != "bad"):
        extra = [x for x in stats[n] if not x[1].startswith("C")]
        if extra:
            print(f"n={n}: " + ", ".join(f"{nm} slack {sl}" for sl, nm in sorted(extra)), flush=True)
    print("counterexamples:", stats["bad"] or "none")


if __name__ == "__main__":
    main()

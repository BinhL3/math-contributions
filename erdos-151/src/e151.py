"""Erdős Problem 151: is tau(G) <= n - H(n) for every graph G on n vertices?

tau(G): fewest vertices meeting every maximal clique of G with >= 2 vertices.
H(n):   largest k such that every triangle-free graph on n vertices has an
        independent set of size k, i.e. H(n) = max{k : R(3,k) <= n}.

Graphs are adjacency bitmasks: adj[v] has bit u set iff uv is an edge.
"""
from itertools import combinations

# Ramsey numbers R(3,k), k = 1..9 (R(3,10) is unknown: 40..41).
R3 = [1, 3, 6, 9, 14, 18, 23, 28, 36]


def H(n):
    if n >= 40:
        raise ValueError("H(n) unknown for n >= 40")
    return max(k + 1 for k, r in enumerate(R3) if r <= n)


def bound(n):
    return n - H(n)


def decode_g6(s):
    data = [ord(c) - 63 for c in s.strip()]
    n = data[0]
    bits = []
    for d in data[1:]:
        bits += [(d >> (5 - b)) & 1 for b in range(6)]
    adj = [0] * n
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            k += 1
    return adj


def maximal_cliques(adj):
    """Bron-Kerbosch with pivoting; cliques as bitmasks."""
    n = len(adj)
    out = []

    def bk(R, P, X):
        if not P and not X:
            out.append(R)
            return
        u = (P | X).bit_length() - 1
        cand = P & ~adj[u]
        while cand:
            v = (cand & -cand).bit_length() - 1
            cand &= cand - 1
            bk(R | (1 << v), P & adj[v], X & adj[v])
            P &= ~(1 << v)
            X |= 1 << v

    bk(0, (1 << n) - 1, 0)
    return out


def edge_cliques(adj):
    """Maximal cliques with at least 2 vertices."""
    return [c for c in maximal_cliques(adj) if c & (c - 1)]


def tau(adj, cap=None):
    """Exact clique transversal number (or cap+1 if it exceeds cap)."""
    n = len(adj)
    cl = edge_cliques(adj)
    if not cl:
        return 0
    cap = n if cap is None else cap
    for size in range(1, cap + 1):
        for S in combinations(range(n), size):
            m = 0
            for v in S:
                m |= 1 << v
            if all(c & m for c in cl):
                return size
    return cap + 1


def hits_all(cl, m):
    return all(c & m for c in cl)


if __name__ == "__main__":
    # sanity: triangle-free graphs have tau = n - alpha
    c5 = decode_g6("Dhc")  # 5-cycle
    assert tau(c5) == 3 == bound(5)
    print("ok", [bound(n) for n in range(2, 16)])

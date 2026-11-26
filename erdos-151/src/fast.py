"""Faster decision procedure: is tau(G) <= b?  (branch and bound hitting set)"""
from e151 import edge_cliques


def tau_le(adj, b):
    """True iff some set of <= b vertices meets every maximal clique of size >= 2."""
    cl = edge_cliques(adj)
    if not cl:
        return True
    # greedy upper bound first: usually settles it
    if greedy_hitting(cl) <= b:
        return True
    return _hit(cl, 0, b)


def tau_exact(adj, cap):
    """tau(G) if <= cap, else cap + 1."""
    cl = edge_cliques(adj)
    if not cl:
        return 0
    g = greedy_hitting(cl)
    lo = 1
    hi = min(g, cap + 1)
    # smallest t with a hitting set of size t
    for t in range(lo, hi):
        if _hit(cl, 0, t):
            return t
    return hi if g <= cap else (cap + 1 if not _hit(cl, 0, cap) else _search_down(cl, cap))


def _search_down(cl, cap):
    t = cap
    while t > 0 and _hit(cl, 0, t - 1):
        t -= 1
    return t


def greedy_hitting(cl):
    rem = list(cl)
    k = 0
    while rem:
        cnt = {}
        for c in rem:
            x = c
            while x:
                v = (x & -x).bit_length() - 1
                x &= x - 1
                cnt[v] = cnt.get(v, 0) + 1
        v = max(cnt, key=cnt.get)
        rem = [c for c in rem if not (c >> v) & 1]
        k += 1
    return k


def _hit(cl, chosen, budget):
    """Can we extend `chosen` with <= budget vertices to hit all of cl?"""
    unhit = [c for c in cl if not c & chosen]
    if not unhit:
        return True
    if budget == 0:
        return False
    # lower bound: greedy disjoint packing of unhit cliques
    pack, used = 0, 0
    for c in sorted(unhit, key=lambda c: bin(c).count("1")):
        if not c & used:
            used |= c
            pack += 1
    if pack > budget:
        return False
    c = min(unhit, key=lambda c: bin(c).count("1"))
    x = c
    while x:
        v = (x & -x).bit_length() - 1
        x &= x - 1
        if _hit(cl, chosen | (1 << v), budget - 1):
            return True
    return False

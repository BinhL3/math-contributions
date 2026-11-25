"""Exact checker for Green's Problem 16 (Ruzsa).

A set A of integers is *good* if there are no pairwise distinct x, y, z, w in A
with x + 3y = 2z + 2w.  `bad_witness` returns such a quadruple, or None.
Runs in O(|A|^2) time and memory.
"""
from collections import defaultdict


def bad_witness(A):
    A = sorted(set(A))
    # left side: x + 3y with x != y
    left = defaultdict(list)
    for x in A:
        for y in A:
            if x != y:
                left[x + 3 * y].append((x, y))
    # right side: 2z + 2w with z < w (z, w interchangeable)
    for i, z in enumerate(A):
        for w in A[i + 1:]:
            for x, y in left.get(2 * (z + w), ()):
                if x not in (z, w) and y not in (z, w):
                    return (x, y, z, w)
    return None


def is_good(A):
    return bad_witness(A) is None


def forbidden_quads(N):
    """All 4-element subsets of {1..N} that contain a distinct solution."""
    quads = set()
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if y == x:
                continue
            for z in range(1, N + 1):
                t = x + 3 * y - 2 * z
                if t % 2:
                    continue
                w = t // 2
                if z < w <= N and len({x, y, z, w}) == 4:
                    quads.add(tuple(sorted((x, y, z, w))))
    return quads


if __name__ == "__main__":
    assert is_good([1, 2, 4, 5, 7, 8])
    assert not is_good([1, 2, 3, 4, 5, 6, 7])
    print("ok")

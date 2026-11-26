# Erdős Problem 151: clique transversals

**Question.** For a graph G on n vertices, let tau(G) be the fewest vertices
meeting every maximal clique with at least 2 vertices, and H(n) the largest k
such that every triangle-free graph on n vertices has an independent set of
size k (so H(n) = max{k : R(3,k) <= n}). Is tau(G) <= n - H(n) always?
([erdosproblems.com/151](https://www.erdosproblems.com/151); Erdős called it
"perhaps completely wrongheaded".)

**Status:** open. No counterexample found.

## Results (2026-11-26)

### Exhaustive: every connected graph with n <= 11 satisfies the bound

Disconnected graphs follow from connected ones (tau adds over components;
H is subadditive). Graph counts match OEIS A001349.

| n | connected graphs | bound n-H(n) | max tau | graphs at the bound | ...with a triangle |
|---|---|---|---|---|---|
| 8 | 11,117 | 5 | 5 | 3 | 0 |
| 9 | 261,080 | 5 | 5 | 596 | 320 |
| 10 | 11,716,571 | 6 | 6 | 414 | 105 |
| 11 | 1,006,700,565 | 7 | 7 | 120 | 15 |

n = 11 tau distribution: {1: 12005168, 2: 155468528, 3: 503855900,
4: 306381484, 5: 28658085, 6: 331280, 7: 120}. n = 10 was computed on two
machines with identical output.

### Structured families: no counterexample

- All connected circulant graphs C_n(S), 5 <= n <= 20: every one satisfies the
  bound; the minimum slack is 0 except at n = 15 and 17 (slack 1).

### Local search (simulated annealing on tau, tie-break toward more triangles)

18 workers × 20 min per run. Best tau found:

| n | bound | seed | best tau | most triangles at the bound |
|---|---|---|---|---|
| 13 | 9 | random | 9 | 0 |
| 13 | 9 | Paley C13(1,5) | 9 | 0 |
| 14 | 9 | random / C14(1,4,7) / C13(1,5) | 9 | 4 |
| 17 | 12 | random | 11 | — |
| 18 | 12 | random | 12 | 7 |
| 22 | 16 | random | 13 | — |
| 23 | 16 | random | 12 | — |

The search is weak for n >= 17 (it does not reach the bound that circulants
reach), so those rows are weak evidence.

## Code

- `src/e151.py` — definitions, brute-force tau.
- `src/fast.py` — branch-and-bound tau (cross-checked against brute force).
- `src/exhaustive.py` — all connected graphs via nauty `geng`.
- `src/families.py` — circulant, Paley, Kneser, Mycielski graphs.
- `src/search.py` — local search.

# Green's Problem 16: sets avoiding x + 3y = 2z + 2w

**Problem** (Ruzsa; Problem 16 in Ben Green's
[100 open problems](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf)).
Let f(N) be the size of the largest A ⊆ {1, …, N} containing no pairwise
distinct x, y, z, w with x + 3y = 2z + 2w. Is f(N) ≤ N^(1−c) for some c > 0?

Known: N^0.5608687 ≲ f(N) ≲ N·exp(−c(log N)^(1/7)). The lower bound is
Hametner–Solymosi ([arXiv:2609.13972](https://arxiv.org/abs/2609.13972), 2026);
the upper bound is Schoen–Sisask (2016).

**Status:** the problem remains open. This folder contributes exact small values
and a reproducible seed-search setup.

## Contribution 1: new terms of OEIS A398785

[A398785](https://oeis.org/A398785): a(n) is the least N such that f(N) = n.
OEIS lists n ≤ 15. New terms:

| n | a(n) | Witness (n-subset of {1..a(n)}) |
|---|---|---|
| 16 | 82 | {1,2,3,4,14,15,16,17,66,67,71,72,76,77,81,82} |
| 17 | 91 | {1,2,3,4,5,17,18,19,20,74,76,79,81,84,86,89,91} |
| 18 | 97 | {1,2,6,7,11,12,16,17,21,77,81,82,86,87,91,92,96,97} |

**Method.** At N = a(n) every witness contains 1 and N (otherwise it shifts into
{1..N−1}). So a(n) is the least N ≥ a(n−1)+1 for which this CNF is satisfiable:
one variable per integer; one clause ¬x∨¬y∨¬z∨¬w per 4-set containing a distinct
solution; a sequential-counter encoding of "at least n true"; unit clauses for 1
and N.

**Certification.** For every N from a(n−1)+1 to a(n)−1, CaDiCaL 3.1.0 reports
UNSAT and emits a DRAT proof. Each proof was checked with
[drat-trim](https://github.com/marijnheule/drat-trim). The log is in
[`results/logs/run_certify1{6,7,8}.log`](results/logs/). Proofs were 29–604 MB
each and are not stored; `certify.py` regenerates them. The witnesses are checked
by `verify_terms.py`.

**Trusted components.** The CNF generator (`check.forbidden_quads` and the
pysat cardinality encoding), cross-validated by reproducing all 15 published
terms. The shift argument above.

**Partial.** The uncertified solver run gives a(19) ≥ 102.

## Contribution 2: seed search (no improvement yet)

Hametner–Solymosi show that a *seed* of size k in (Z_m)^r gives
f(N) ≥ N^(log k/(r log m) − o(1)). Their 15-point seed in (Z_5)^3, found with
AlphaEvolve, gives 0.5608687. `seed.py` re-verifies it with their weights. Our
seed test is an LP over general weights f1..f4; theirs fixes the form (−3f, f, f, f).

| Group | Size needed to beat 0.5609 | Best found | Search |
|---|---|---|---|
| Z_m, m ≤ 35 | — | below record | exhaustive |
| (Z_5)^2 | 7 | 5 (maximum) | exhaustive |
| (Z_7)^2 | 9 | 7 (maximum) | exhaustive |
| (Z_11)^2 | 15 | 12 | exhaustive, timed out |
| (Z_5)^3 | 16 | 15 (ties record) | local search, 12 × 30 min |
| (Z_5)^4 | 37 | 35 | local search from product seed, 10 × 40 min |

## Reproduce

```sh
cd green-16
uv venv && uv pip install -r requirements.txt   # python-sat, scipy, numpy
cd src
python verify_terms.py                  # check the witnesses (seconds)
python thresholds.py 15                 # reproduce OEIS a(1..15)
python parallel.py 16 74 89             # find a(16)
brew install cadical                    # and build drat-trim; set DRAT_TRIM=path
python certify.py 16 74 81              # certify a(16) > 81
python seed.py                          # check the paper's seed
python search_local.py 5 3 600 8        # seed search in (Z_5)^3
```

## Files

| File | Purpose |
|---|---|
| `src/check.py` | exact O(\|A\|²) checker; enumerates forbidden 4-sets |
| `src/verify_terms.py` | checks the new witnesses |
| `src/thresholds.py` | computes a(n) sequentially with SAT |
| `src/parallel.py` | runs one n over many N in parallel |
| `src/certify.py` | CaDiCaL + drat-trim certification |
| `src/seed.py` | seed definition, LP test, the paper's seed |
| `src/search_exact.py` | exhaustive seed search |
| `src/search_local.py` | randomized local seed search |
| `OEIS_SUBMISSION.md` | text to paste into the OEIS edit form |

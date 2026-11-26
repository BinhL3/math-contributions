# Erdős Problem 151: clique transversals

Work in progress. Is tau(G) <= n - H(n) for every graph G on n vertices?

- Exhaustive check of all connected graphs: n <= 10 done, no counterexample (`src/exhaustive.py`).
- Graphs meeting the bound exactly: `results/tight_n*.g6` (graph6 format).

Requires nauty (`geng`).

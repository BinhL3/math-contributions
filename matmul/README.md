# Small matrix multiplication ranks

Goal: beat best-known ranks (number of multiplications) for small formats
<n1, n2, n3>, starting with records that are only products or splits of smaller
schemes. Current records: [FastMatrixMultiplication](https://github.com/dronperminov/FastMatrixMultiplication)
`docs/ranks.md` and the [fmm catalogue](https://fmm.univ-lille.fr/).

First targets: 4x6x6 (record 105 = 2x2x2 ⊗ 2x3x3) and 3x6x6 (record 80 over Q,
82 over Z).

Search: [ternary_flip_graph](https://github.com/dronperminov/ternary_flip_graph)
(MIT). Every claimed scheme is checked independently with `src/verify_scheme.py`
(exact Brent equations over the integers plus random integer multiplication).

# Math contributions

Computational contributions to open problems in mathematics. Every result
here comes with code that reproduces it and, where possible, an independently
checked certificate.

| Project | Problem | Result | Status |
|---|---|---|---|
| [green-16](green-16/) | Green's Problem 16 (Ruzsa): largest A ⊆ [N] avoiding x + 3y = 2z + 2w | New terms a(16)–a(18) of [OEIS A398785](https://oeis.org/A398785), certified by DRAT proofs. Seed search ties the 2026 record exponent but does not beat it. | OEIS submission pending |

## Conventions

- Each project gets its own folder: `README.md` (problem, results, method, what is trusted), `src/`, `results/`.
- Claims are marked as **certified** (independently checked proof), **verified** (witness checked by code), or **computed** (solver output only).
- Large proof files are not committed. The code regenerates them.

## License

MIT. See [LICENSE](LICENSE).

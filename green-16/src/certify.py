"""Certify 'no good n-set in {1..N} containing 1 and N' with a DRAT proof.

Writes the CNF to certs/, solves it with the CaDiCaL binary (which emits a
DRAT proof), and checks that proof with drat-trim, an independent checker.

usage: certify.py n N_lo N_hi [workers]
"""
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF

from check import forbidden_quads

HERE = Path(__file__).parent
# drat-trim: https://github.com/marijnheule/drat-trim (build with `cc -O2 -o drat-trim drat-trim.c`)
DRAT_TRIM = os.environ.get("DRAT_TRIM", "drat-trim")
CERTS = HERE.parent / "certs"  # regenerated CNFs (git-ignored)


def certify(args):
    n, N = args
    CERTS.mkdir(exist_ok=True)
    cnf_path = CERTS / f"n{n}_N{N}.cnf"
    proof_path = CERTS / f"n{n}_N{N}.drat"
    clauses = [[-v for v in q] for q in forbidden_quads(N)]
    card = CardEnc.atleast(lits=list(range(1, N + 1)), bound=n,
                           top_id=N, encoding=EncType.seqcounter)
    CNF(from_clauses=clauses + card.clauses + [[1], [N]]).to_file(str(cnf_path))
    solve = subprocess.run(["cadical", "-q", str(cnf_path), str(proof_path)],
                           capture_output=True, text=True)
    if solve.returncode != 20:  # 20 = UNSAT
        return N, f"NOT UNSAT (cadical exit {solve.returncode})"
    check = subprocess.run([DRAT_TRIM, str(cnf_path), str(proof_path), "-t", "20000"],
                           capture_output=True, text=True)
    verified = "s VERIFIED" in check.stdout
    size_mb = proof_path.stat().st_size / 1e6
    if verified:
        proof_path.unlink()  # proofs are large; the CNF + rerun reproduces them
    return N, ("UNSAT, proof VERIFIED by drat-trim" if verified
               else "UNSAT but proof NOT verified") + f" ({size_mb:.0f} MB proof)"


if __name__ == "__main__":
    n, lo, hi = map(int, sys.argv[1:4])
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    with ProcessPoolExecutor(workers) as ex:
        for N, msg in ex.map(certify, [(n, N) for N in range(lo, hi + 1)]):
            print(f"n={n} N={N}: {msg}", flush=True)

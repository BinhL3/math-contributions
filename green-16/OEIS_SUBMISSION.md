# OEIS A398785: proposed extension

1. Open https://oeis.org/draft/A398785. If someone has already added a(16), stop.
2. Log in, open https://oeis.org/A398785 and click **edit**.
3. Make the changes below, then submit for review.

## DATA

```
1, 2, 3, 4, 5, 8, 14, 17, 20, 22, 32, 37, 55, 64, 73, 82, 91, 97
```

## COMMENTS (append)

```
For n = 16..18 the terms were found by SAT solving: at N = a(n) a witness must contain both 1 and N, and for every N from a(n-1)+1 to a(n)-1 the corresponding instance is unsatisfiable, certified by CaDiCaL DRAT proofs checked with drat-trim. Witnesses: a(16) = 82: {1,2,3,4,14,15,16,17,66,67,71,72,76,77,81,82}; a(17) = 91: {1,2,3,4,5,17,18,19,20,74,76,79,81,84,86,89,91}; a(18) = 97: {1,2,6,7,11,12,16,17,21,77,81,82,86,87,91,92,96,97}.
```

## LINKS (add)

```
<Your Name>, <a href="https://github.com/BinhL3/math-contributions/tree/main/green-16">SAT code and certificates for a(16)-a(18)</a>
```

## EXTENSIONS

```
a(16)-a(18) from <Your Name>, Nov 25 2026
```

## b-file (optional)

Append to the existing b-file (n = 1..15):

```
16 82
17 91
18 97
```

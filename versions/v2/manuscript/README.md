# A negative answer to Delgado, Süer and Yeşil's symmetrization question

Haobo Ma — ChronoAI Pte Ltd, Singapore  
Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore

The note answers the question in the final paragraph of Section 5, p. 9, of
[Delgado, Süer and Yeşil, arXiv:2611.14268v1](https://arxiv.org/abs/2611.14268v1).
Every output of pseudo-Frobenius row deletion on a proper numerical semigroup
omits 1. Hence the symmetric numerical set with gaps {2,3} is not an output.
The note also proves that at least half of the symmetric targets at each odd
Frobenius number at least 3 are excluded, and that every symmetric numerical
semigroup is fixed by the map.
Conversely these are the only fixed points among proper numerical semigroups.
The fiber over the target with sole gap 1 consists exactly of the ordinary
semigroups `{0} union {m,m+1,...}` for `m >= 2`, so it is infinite and contains
exactly one source of each positive Frobenius number. For source Frobenius `F`,
the number of distinct images is at most `2^(floor((F+1)/2)-1)`.

## Contents

- `note.tex`: self-contained mathematical statements and proofs, with embedded bibliography.
- `note.pdf`: readable typeset note, supplied alongside the source archive.
- `metadata.json`: authors, license, abstract, coverage identifier, and formal-source link.
- `verify.py`: dependency-free exact finite checks, requiring Python 3.9 or later.
- `verification.json`: deterministic output of `python3 verify.py`.

## Rebuild

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, use a standard TeX distribution:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is embedded in `note.tex`; BibTeX and external figures are not needed.

## Exact checks and mathematical scope

```sh
python3 verify.py > verification-rebuilt.json
cmp verification.json verification-rebuilt.json
```

The script enumerates all proper numerical semigroups of source Frobenius number
1 through 18 (1,654 semigroups, including 367 almost symmetric ones). Each is
encoded by its complete finite gap set. The tests for additive closure and
pseudo-Frobenius gaps are exact: a sum larger than the Frobenius number is
automatically a member. Every proper numerical semigroup omits 1, so enumerating
all subsets of the other positive integers below the prescribed largest gap
exhausts the stated range. Two implementations compute row deletion: shifted
original gap labels, and deletion from the ordered boundary-step sequence.
The three numerical columns in Table 1 of the posing paper agree for source
Frobenius numbers 1 through 18. Symmetric targets of odd Frobenius numbers 1
through 17 are enumerated separately; these are not the fixed-source image
sets used in that table.

The statements for arbitrary Frobenius number are proved in `note.tex`;
finite enumeration is supporting evidence, not an extrapolation. In the
[pinned Lean file](https://github.com/the-omega-institute/trureturing/blob/f960cb09514c99f42fd07398f5240a77378ea4db/D5/S3/Combinatorics/Partitions/DelgadoSuerYesilPhiRefutation.lean),
`D5.S3.Combinatorics.Partitions.DelgadoSuerYesilPhiRefutation.phi_omits_one`
states the universal obstruction, and `result` states the failure of unrestricted
surjectivity with witness gaps {2,3}. All four corollaries (the half-of-targets
exclusion, fixed-point characterization, ordinary fiber and fixed-source bound)
have written proofs in this note. The checker verifies the additional finite
instances, including exactly one ordinary source per positive Frobenius number
and the fixed-source image bound. A full image description and general counting
asymptotics are not asserted.

## License

Copyright 2026 Haobo Ma and Wenlin Zhang.
Creative Commons Attribution 4.0 International, `cc-by-4.0`:
<https://creativecommons.org/licenses/by/4.0/>.

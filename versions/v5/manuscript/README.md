# Obstructions to row-deletion symmetrization

Haobo Ma — ChronoAI Pte Ltd, Singapore.  
Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

Stable note ID: `delgado-suer-yesil-2026-symmetrization-surjectivity`.  
Revision 5, 25 November 2026. License: CC BY 4.0.

## Mathematical coverage

`note.tex` is the sole main manuscript. Its diagram is drawn directly in LaTeX,
and its bibliography is included in the same file.

- Theorem 1: original-label pseudo-Frobenius row deletion omits 1 for every proper numerical semigroup; hence the unrestricted surjectivity question of Delgado, Süer and Yeşil has a negative answer.
- Corollaries 2–5: half-target exclusion at each odd target Frobenius number at least 3, the symmetric-semigroup fixed points, the exact ordinary fiber, and the fixed-source image bound.
- Theorem 6 and Corollary 7: the prefix inequality `b_i >= 2i` and the smallest excluded reduced symmetric target, with gaps `{1,4,5,7}` and Frobenius number 7. Section 3 also gives the binomial exclusion bound and an excluded family for every least positive element at least 2.
- Theorem 8: image targets containing 2 are precisely the even-prefix symmetric semigroups.
- Lemma 9 and Theorem 10: the full-cell convention is equivalent to the prefix inequality but is not sufficient for membership in the image; the least Frobenius number of an excluded full-cell target is 9, and an excluded family occurs at every odd Frobenius number at least 9.

The diagram of the Frobenius-9 example is attributed to Bras-Amorós and de Mier,
Remark 2.5; the same numerical set appears explicitly in Yeşil, Example 5.3.
The total symmetric-target count is attributed to Marzuola and Miller.
The omission obstruction and Corollaries 2–5 are also in the earlier note,
revision 2, DOI `10.5281/zenodo.24391331`.

- Section 7 characterizes multiplicity-three targets: the two explicit families coincide for `h = 3, 4, 5` and differ for every `h >= 6`, at output Frobenius `2h - 1`. It also gives a least-Frobenius multiplicity-three nonimage satisfying the prefix bound.
- For output multiplicity `r` and Frobenius `2h - 1` with `h > r`, every source has multiplicity at most `2r - 2` and Frobenius in `[2h - 1, 2h + 2r - 5]`. The boundary targets are handled separately, giving an exact finite membership test without claiming a closed classification at higher multiplicity.

## Build the manuscript

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively run `pdflatex note.tex` twice. The required packages are
`fontenc`, `lmodern`, `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`,
`geometry`, `hyperref`, `xurl`, `tabularx` and `needspace`.

## Reproduce the finite checks

Python 3 and its standard library suffice:

```sh
python3 verify.py
python3 verify_multiplicity3.py --output multiplicity3_checks.rerun.json
```

The first command produces four detailed JSON outputs and `verification.json`. The file from the second command can be compared with `multiplicity3_checks.json`.
The programs use exact finite sets, integer bit masks and integer arithmetic.

| Program | Complete finite domain | Main checks |
| --- | --- | --- |
| `verify_base.py` | All 1,654 proper numerical semigroups with source Frobenius 1–18, including 367 almost symmetric sources; all 511 symmetric targets with odd Frobenius 1–17 | Original-label deletion, omission of 1, all four corollaries, and the first 18 rows of the posing paper's Table 1 |
| `verify_prefix.py` | All 840,170 proper numerical semigroups with source Frobenius at most 35, including 17,842 almost symmetric sources | Prefix inequality, rigidity for targets containing 2, and zero preimages of the Frobenius-7 target |
| `verify_independent.py` | All 65,535 membership masks through source Frobenius 16; 784 numerical semigroups, including 226 almost symmetric sources | Direct closure and pseudo-Frobenius tests, symmetry iff almost symmetry, prefix inequality and rigidity |
| `verify_diagonal.py` | All 4,095 symmetric targets with odd Frobenius 1–23; family parameters 5–100; all numerical-semigroup sources through Frobenius 18 | Full-cell/prefix equivalence, complete small-target lists, the excluded family and source-image assertions |

| `verify_multiplicity3.py` | All 840,170 proper sources through Frobenius 35; separate subset enumeration through 18; constructions for 3 ≤ h ≤ 100 | Exact cutoff and multiplicity-three checks; completeness for multiplicity-three targets through output Frobenius 33 |

The bounded source-image counts are unions over sources with Frobenius at most
35, grouped by output Frobenius. They are not unrestricted image cardinalities,
nor counts at one fixed source Frobenius. The multiplicity-three cutoff gives completeness within its separately stated output range. The finite checks supplement the
written proofs for all parameters and do not establish ratio asymptotics or
a closed-form classification at every multiplicity.

## Formal statements

The public, pinned Lean source is:

`https://github.com/the-omega-institute/trureturing/blob/f960cb09514c99f42fd07398f5240a77378ea4db/D5/S3/Combinatorics/Partitions/DelgadoSuerYesilPhiRefutation.lean`

In namespace `D5.S3.Combinatorics.Partitions.DelgadoSuerYesilPhiRefutation`,
`phi_omits_one` states the universal omission of 1 and `result` states the
failure of unrestricted surjectivity. `deleteRows` and `phi` encode the
original-label gap formula, and `AlmostSymmetric` includes additive closure
and the genus/type identity. The other results have written proofs in the
manuscript, with the finite supporting domains specified above.

`MANIFEST.json` lists the sizes and SHA-256 values of the scientific source
members. It does not list itself.

Copyright © 2026 Haobo Ma and Wenlin Zhang.
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).

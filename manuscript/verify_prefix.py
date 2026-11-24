import argparse
import json
from math import comb
from pathlib import Path


def semigroups(maximum):
    stack = [(2, 1, 1)]
    while stack:
        gaps, frobenius, genus = stack.pop()
        yield gaps, frobenius, genus
        positive = ((1 << (frobenius + 1)) - 1) & ~gaps & ~1
        multiplicity = (positive & -positive).bit_length() - 1 if positive else frobenius + 1
        for candidate in range(frobenius + 1, min(maximum, frobenius + multiplicity) + 1):
            if all((gaps >> summand) & 1 or (gaps >> (candidate - summand)) & 1
                   for summand in range(1, candidate // 2 + 1)):
                stack.append((gaps | (1 << candidate), candidate, genus + 1))


def pseudo_frobenius(gaps, frobenius):
    positive = ((1 << (frobenius + 1)) - 1) & ~gaps & ~1
    return [gap for gap in range(1, frobenius + 1)
            if gaps & (1 << gap) and not ((gaps >> gap) & positive)]


def symmetrize(gaps, frobenius, pseudo):
    deleted = set(pseudo) - {frobenius}
    shift = 0
    result = []
    for position in range(1, frobenius + 1):
        if position in deleted:
            shift += 1
        elif gaps & (1 << position):
            result.append(position - shift)
    return tuple(result)


def targets(frobenius):
    half = (frobenius + 1) // 2
    if half == 1:
        return [(1,)]
    result = []
    for mask in range(1 << (half - 2)):
        gaps = [1, frobenius]
        for position in range(2, half):
            gaps.append(position if mask & (1 << (position - 2)) else frobenius - position)
        result.append(tuple(sorted(gaps)))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--maximum', type=int, default=25)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    counts = {}
    almost_counts = {}
    images = {}
    checked = 0
    counterexample = (1, 4, 5, 7)
    counterexample_hits = 0
    midpoint_checks = 0
    for gaps, frobenius, genus in semigroups(args.maximum):
        checked += 1
        counts[frobenius] = counts.get(frobenius, 0) + 1
        pseudo = pseudo_frobenius(gaps, frobenius)
        if 2 * genus != frobenius + len(pseudo):
            continue
        almost_counts[frobenius] = almost_counts.get(frobenius, 0) + 1
        output = symmetrize(gaps, frobenius, pseudo)
        counterexample_hits += output == counterexample
        output_frobenius = output[-1]
        assert output_frobenius == frobenius - len(pseudo) + 1
        assert 1 in output
        assert all(((position in output) != (output_frobenius - position in output))
                   for position in range(output_frobenius + 1))
        half = (output_frobenius + 1) // 2
        small_elements = tuple(position for position in range(output_frobenius + 1) if position not in output)
        assert all(position >= 2 * index for index, position in enumerate(small_elements))
        if 2 not in output:
            assert small_elements == tuple(range(0, output_frobenius, 2))
        lower_positive = sum(position not in output for position in range(1, half))
        assert 2 * lower_positive + 1 <= half
        midpoint_checks += 1
        if output not in images:
            images[output] = {'frobenius': frobenius, 'gaps': [position for position in range(1, frobenius + 1) if gaps & (1 << position)], 'pseudo_frobenius': pseudo}
    coverage = []
    for frobenius in range(1, args.maximum + 1, 2):
        target_list = targets(frobenius)
        attained = [target for target in target_list if target in images]
        missing = [list(target) for target in target_list if target not in images]
        half = (frobenius + 1) // 2
        excluded = sum(comb(half - 2, size) for size in range((half + 1) // 2, half - 1)) if half >= 2 else 0
        coverage.append({'output_frobenius': frobenius, 'reduced_targets': len(target_list),
                         'attained': len(attained), 'missing_count': len(missing),
                         'first_missing_gaps': missing[0] if missing else None,
                         'excluded_by_midpoint_bound': excluded})
    result = {'maximum_source_frobenius': args.maximum, 'proper_semigroups_checked': checked,
              'semigroups_by_frobenius': counts, 'almost_symmetric_by_frobenius': almost_counts,
              'almost_symmetric_total': midpoint_checks, 'counterexample_gaps': list(counterexample),
              'counterexample_hits': counterexample_hits,
              'coverage': coverage, 'small_witnesses': [{'target_gaps': list(target), 'source': witness} for target, witness in sorted(images.items()) if target[-1] <= 9]}
    assert counterexample_hits == 0
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ['maximum_source_frobenius', 'proper_semigroups_checked', 'almost_symmetric_by_frobenius']}))
    print(json.dumps([{key: row[key] for key in ['output_frobenius', 'reduced_targets', 'attained']} for row in coverage]))


if __name__ == '__main__':
    main()

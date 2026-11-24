import argparse
import json
from pathlib import Path


def calculate(maximum):
    counts = {}
    almost_counts = {}
    masks = 0
    checked = 0
    almost_total = 0
    nonimages = 0
    for frobenius in range(1, maximum + 1):
        counts[str(frobenius)] = 0
        almost_counts[str(frobenius)] = 0
        for mask in range(1 << (frobenius - 1)):
            masks += 1
            elements = {0} | {position for position in range(1, frobenius)
                              if mask & (1 << (position - 1))}
            positives = elements - {0}
            if any(left + right <= frobenius and left + right not in elements
                   for left in positives for right in positives):
                continue
            gaps = set(range(1, frobenius + 1)) - elements
            pseudo = {gap for gap in gaps
                      if all(gap + positive > frobenius or gap + positive in elements
                             for positive in positives)}
            checked += 1
            counts[str(frobenius)] += 1
            retained = sorted(set(range(frobenius + 1)) - (pseudo - {frobenius}))
            output_gaps = [index for index, label in enumerate(retained) if label in gaps]
            output_elements = [index for index, label in enumerate(retained) if label in elements]
            output_frobenius = output_gaps[-1]
            symmetric = all((position in output_gaps) != (output_frobenius - position in output_gaps)
                            for position in range(output_frobenius + 1))
            almost = 2 * len(gaps) == frobenius + len(pseudo)
            assert symmetric == almost
            if output_gaps == [1, 4, 5, 7]:
                nonimages += 1
            if not almost:
                continue
            almost_total += 1
            almost_counts[str(frobenius)] += 1
            assert all(position >= 2 * index for index, position in enumerate(output_elements))
            if 2 not in output_gaps:
                assert output_elements == list(range(0, output_frobenius, 2))
    assert nonimages == 0
    return {
        'maximum_source_frobenius': maximum,
        'membership_masks_checked': masks,
        'proper_semigroups_checked': checked,
        'almost_symmetric_total': almost_total,
        'counterexample_hits': nonimages,
        'semigroups_by_frobenius': counts,
        'almost_symmetric_by_frobenius': almost_counts,
        'checks': ['closure by all positive sums', 'defining pseudo-Frobenius condition',
                   'rank relabeling after original-row deletion', 'symmetry iff almost symmetry',
                   'prefix inequality', 'rigidity for targets containing 2'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--maximum', type=int, default=16)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    if not 1 <= arguments.maximum <= 20:
        parser.error('Select a maximum between 1 and 20')
    result = calculate(arguments.maximum)
    arguments.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ['maximum_source_frobenius',
                     'membership_masks_checked', 'proper_semigroups_checked',
                     'almost_symmetric_total', 'counterexample_hits']}))


if __name__ == '__main__':
    main()

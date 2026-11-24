import argparse
import json
from pathlib import Path


def symmetric(elements, frobenius):
    return all((value in elements) != (frobenius - value in elements)
               for value in range(frobenius + 1))


def closed(elements, frobenius):
    return all(left + right > frobenius or left + right in elements
               for left in elements for right in elements)


def cells(elements, frobenius):
    horizontal = 0
    vertical = 0
    lower_edges = []
    for value in range(frobenius + 1):
        if value in elements:
            lower_edges.append(vertical)
            horizontal += 1
        else:
            vertical += 1
    occupied = [(column, row) for column, lower in enumerate(lower_edges)
                for row in range(lower, vertical)]
    forbidden = [(column, row) for column, row in occupied if row + 1 <= column]
    return occupied, forbidden


def calculate(maximum_source):
    target_counts = {}
    small_targets = {}
    first_containing_two_obstruction = None
    for half_conductor in range(1, 13):
        frobenius = 2 * half_conductor - 1
        diagonal_count = 0
        for mask in range(1 << (half_conductor - 1)):
            elements = {0}
            for low in range(1, half_conductor):
                elements.add(low if mask & (1 << (low - 1)) else frobenius - low)
            assert symmetric(elements, frobenius)
            ordered = sorted(elements)
            prefix = all(value >= 2 * index for index, value in enumerate(ordered))
            _, forbidden = cells(elements, frobenius)
            assert prefix == (not forbidden)
            if not prefix:
                continue
            diagonal_count += 1
            if half_conductor <= 4:
                assert closed(elements, frobenius)
                small_targets.setdefault(str(frobenius), []).append(ordered)
            if 2 in elements and ordered != list(range(0, frobenius, 2)):
                if first_containing_two_obstruction is None:
                    first_containing_two_obstruction = {'frobenius': frobenius, 'elements': ordered}
        target_counts[str(frobenius)] = diagonal_count
    for half_conductor in range(5, 101):
        frobenius = 2 * half_conductor - 1
        elements = {0, 2} | (set(range(half_conductor, 2 * half_conductor - 1)) - {2 * half_conductor - 3})
        assert len(elements) == half_conductor
        assert symmetric(elements, frobenius)
        assert 2 in elements and 4 not in elements
        assert all(value >= 2 * index for index, value in enumerate(sorted(elements)))
        assert not cells(elements, frobenius)[1]
    source_masks = 0
    semigroups = 0
    almost_symmetric = 0
    source_counts = {}
    for frobenius in range(1, maximum_source + 1):
        group_count = 0
        for mask in range(1 << (frobenius - 1)):
            source_masks += 1
            elements = {0} | {value for value in range(1, frobenius)
                              if mask & (1 << (value - 1))}
            if not closed(elements, frobenius):
                continue
            semigroups += 1
            group_count += 1
            gaps = set(range(frobenius + 1)) - elements
            pseudo = {gap for gap in gaps
                      if all(gap + value > frobenius or gap + value in elements
                             for value in elements - {0})}
            if 2 * len(gaps) != frobenius + len(pseudo):
                continue
            almost_symmetric += 1
            retained = sorted(set(range(frobenius + 1)) - (pseudo - {frobenius}))
            assert set(retained) == elements | {frobenius - value for value in elements}
            output = {rank for rank, value in enumerate(retained) if value in elements}
            output_frobenius = len(retained) - 1
            assert symmetric(output, output_frobenius)
            assert not cells(output, output_frobenius)[1]
            assert all(value >= 2 * index for index, value in enumerate(sorted(output)))
            if 2 in output:
                assert sorted(output) == list(range(0, output_frobenius, 2))
        source_counts[str(frobenius)] = group_count
    witness = {0, 2, 5, 6, 8}
    occupied, forbidden = cells(witness, 9)
    return {
        'target_scope': 'All symmetric numerical sets with Frobenius 1,3,...,23',
        'diagonal_target_counts': target_counts,
        'attained_targets_through_frobenius_7': small_targets,
        'first_containing_two_obstruction': first_containing_two_obstruction,
        'family_parameters_checked': {'h_min': 5, 'h_max': 100},
        'source_maximum_frobenius': maximum_source,
        'source_membership_masks': source_masks,
        'numerical_semigroups': semigroups,
        'almost_symmetric_sources': almost_symmetric,
        'semigroups_by_source_frobenius': source_counts,
        'witness': {'elements_below_conductor': sorted(witness), 'gaps': [1, 3, 4, 7, 9],
                    'boundary_word': 'ENENNEENEN', 'column_bottom_heights': [0, 1, 3, 3, 4],
                    'row_lengths_bottom_to_top': [sum(row == height for _, row in occupied) for height in range(5)],
                    'full_cells_strictly_below_diagonal': forbidden},
        'scope': 'Finite checks supplement the written proofs for all source semigroups and every family parameter h>=5.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--maximum-source', type=int, default=18)
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    if not 1 <= arguments.maximum_source <= 20:
        parser.error('Choose a source Frobenius bound between 1 and 20')
    result = calculate(arguments.maximum_source)
    arguments.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

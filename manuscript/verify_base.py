import json


def is_semigroup(gaps):
    frobenius = max(gaps)
    members = [value for value in range(1, frobenius + 1) if value not in gaps]
    return all(first + second not in gaps for first in members for second in members)


def pseudo_frobenius(gaps):
    frobenius = max(gaps)
    members = [value for value in range(1, frobenius + 1) if value not in gaps]
    return frozenset(gap for gap in gaps if all(gap + member not in gaps for member in members))


def is_symmetric(gaps):
    frobenius = max(gaps)
    return all((value in gaps) != (frobenius - value in gaps)
               for value in range(frobenius + 1))


def deletion_formula(gaps):
    removed = pseudo_frobenius(gaps) - {max(gaps)}
    return frozenset(gap - sum(deleted < gap for deleted in removed)
                     for gap in gaps - removed)


def deletion_boundary(gaps):
    removed = pseudo_frobenius(gaps) - {max(gaps)}
    output_gaps = set()
    new_label = 0
    for old_label in range(max(gaps) + 1):
        if old_label in removed:
            continue
        if old_label in gaps:
            output_gaps.add(new_label)
        new_label += 1
    return frozenset(output_gaps)


def gap_sets(frobenius):
    if frobenius == 1:
        yield frozenset({1})
        return
    for mask in range(1 << (frobenius - 2)):
        yield frozenset({1, frobenius} | {
            value for value in range(2, frobenius)
            if mask & (1 << (value - 2))
        })


def check_sources():
    expected_almost = [1, 1, 2, 2, 4, 3, 7, 6, 11, 9, 20, 15, 32, 24, 47, 42, 83, 58]
    expected_images = [1, 1, 2, 2, 4, 3, 6, 5, 8, 7, 13, 8, 18, 13, 21, 18, 34, 21]
    expected_semigroup_images = [1, 1, 2, 2, 4, 3, 6, 5, 8, 6, 12, 8, 17, 13, 20, 15, 30, 19]
    rows = []
    for frobenius in range(1, 19):
        semigroups = 0
        almost_symmetric = 0
        images = set()
        ordinary_sources = 0
        fixed_points = 0
        for gaps in gap_sets(frobenius):
            if not is_semigroup(gaps):
                continue
            semigroups += 1
            pseudo = pseudo_frobenius(gaps)
            output = deletion_formula(gaps)
            assert output == deletion_boundary(gaps)
            assert 0 not in output and 1 in output
            assert len(output) == len(gaps) - len(pseudo) + 1
            assert max(output) == frobenius - len(pseudo) + 1
            ordinary = gaps == frozenset(range(1, frobenius + 1))
            assert (output == {1}) == ordinary
            assert (output == gaps) == is_symmetric(gaps)
            ordinary_sources += ordinary
            fixed_points += output == gaps
            if is_symmetric(gaps):
                assert pseudo == {frobenius}
                assert output == gaps
            if 1 in pseudo:
                assert gaps == frozenset(range(1, frobenius + 1))
                assert output == {1}
            if 2 * len(gaps) == frobenius + len(pseudo):
                almost_symmetric += 1
                assert is_symmetric(output)
                assert len(output) == frobenius - len(gaps) + 1
                assert max(output) == 2 * (frobenius - len(gaps) + 1) - 1
                assert max(output) <= frobenius
                images.add(output)
        semigroup_images = sum(is_semigroup(image) for image in images)
        assert almost_symmetric == expected_almost[frobenius - 1]
        assert len(images) == expected_images[frobenius - 1]
        assert semigroup_images == expected_semigroup_images[frobenius - 1]
        image_upper_bound = 2 ** ((frobenius + 1) // 2 - 1)
        assert 1 <= semigroup_images <= len(images) <= image_upper_bound
        assert ordinary_sources == 1 and frozenset({1}) in images
        rows.append({'source_frobenius': frobenius, 'numerical_semigroups': semigroups,
                     'almost_symmetric': almost_symmetric, 'distinct_images': len(images),
                     'semigroup_images': semigroup_images, 'image_upper_bound': image_upper_bound,
                     'ordinary_sources': ordinary_sources, 'symmetric_fixed_points': fixed_points})
    return rows


def check_targets():
    rows = []
    for half_conductor in range(1, 10):
        frobenius = 2 * half_conductor - 1
        targets = set()
        for mask in range(1 << (half_conductor - 1)):
            gaps = {frobenius}
            for lower in range(1, half_conductor):
                gaps.add(lower if mask & (1 << (lower - 1)) else frobenius - lower)
            gaps = frozenset(gaps)
            assert is_symmetric(gaps)
            targets.add(gaps)
        containing_one = sum(1 not in gaps for gaps in targets)
        assert len(targets) == 2 ** (half_conductor - 1)
        if half_conductor >= 2:
            assert containing_one == 2 ** (half_conductor - 2)
        rows.append({'target_frobenius': frobenius, 'symmetric_numerical_sets': len(targets),
                     'targets_containing_one': containing_one})
    return rows


def main():
    witness_gaps = frozenset({2, 3})
    assert is_symmetric(witness_gaps)
    assert 1 not in witness_gaps and 2 in witness_gaps
    assert not is_semigroup(witness_gaps)
    first_collision = frozenset({1, 2, 3, 5, 7})
    second_collision = frozenset({1, 2, 3, 4, 7})
    assert is_semigroup(first_collision) and is_semigroup(second_collision)
    assert 2 * len(first_collision) == 7 + len(pseudo_frobenius(first_collision))
    assert 2 * len(second_collision) == 7 + len(pseudo_frobenius(second_collision))
    assert deletion_formula(first_collision) == deletion_formula(second_collision) == {1, 2, 5}
    sources = check_sources()
    targets = check_targets()
    result = {
        'arithmetic': 'exact integers and finite sets; no floating-point operations',
        'scope': {'source_frobenius_min': 1, 'source_frobenius_max': 18,
                  'target_frobenius_values': list(range(1, 18, 2))},
        'source_completeness': 'Every proper numerical semigroup has gap 1; all remaining gap subsets below the fixed Frobenius number are enumerated.',
        'finite_reduction': 'A sum or pseudo-Frobenius test exceeding the largest gap automatically belongs to the numerical set.',
        'unbounded_statements': 'The universal obstruction, target count, fixed-point characterization, ordinary fiber and fixed-source bound have written proofs in note.pdf.',
        'numerical_semigroups_checked': sum(row['numerical_semigroups'] for row in sources),
        'almost_symmetric_checked': sum(row['almost_symmetric'] for row in sources),
        'source_table_comparison': 'All three columns of Table 1, rows F=1 through F=18, agree.',
        'sources': sources,
        'targets': targets,
        'counterexample': {'gaps': [2, 3], 'frobenius': 3, 'symmetric': True,
                           'contains_one': True, 'semigroup': False},
        'existing_collision': {'source_gap_sets': [sorted(first_collision), sorted(second_collision)],
                               'image_gaps': [1, 2, 5]},
        'checks': 'pass'
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

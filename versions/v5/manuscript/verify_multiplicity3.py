import argparse
import hashlib
import json
from pathlib import Path


def source_semigroups(maximum):
    pending = [(2, 1, 1)]
    while pending:
        gap_bits, source_frobenius, genus = pending.pop()
        yield gap_bits, source_frobenius, genus
        positive_bits = ((1 << (source_frobenius + 1)) - 1) & ~gap_bits & ~1
        multiplicity = ((positive_bits & -positive_bits).bit_length() - 1
                        if positive_bits else source_frobenius + 1)
        for new_gap in range(source_frobenius + 1, min(maximum, source_frobenius + multiplicity) + 1):
            decomposable = any(not (gap_bits >> summand) & 1 and
                              not (gap_bits >> (new_gap - summand)) & 1
                              for summand in range(1, new_gap // 2 + 1))
            if not decomposable:
                pending.append((gap_bits | (1 << new_gap), new_gap, genus + 1))


def bit_pseudo(gap_bits, source_frobenius):
    positive_bits = ((1 << (source_frobenius + 1)) - 1) & ~gap_bits & ~1
    return [gap for gap in range(1, source_frobenius + 1)
            if gap_bits & (1 << gap) and not ((gap_bits >> gap) & positive_bits)]


def compressed_elements(gap_bits, source_frobenius, pseudo):
    deleted = set(pseudo) - {source_frobenius}
    rank = 0
    elements = []
    for original in range(source_frobenius + 1):
        if original in deleted:
            continue
        if not (gap_bits >> original) & 1:
            elements.append(rank)
        rank += 1
    return tuple(elements)


def even_tail(half):
    return tuple([0] + list(range(3, 2 * half - 2, 2)) + [2 * half - 2])


def triple_family(half):
    if half % 3 != 2:
        generator = half + 1
        return tuple(value for value in range(2 * half)
                     if any((value - copies * generator) % 3 == 0
                            for copies in range(value // generator + 1)))
    quotient = (half - 2) // 3
    return tuple(sorted(set(range(0, 3 * quotient + 1, 3)) |
                        set(range(3 * quotient + 2, 6 * quotient + 3, 3)) |
                        set(range(3 * quotient + 4, 6 * quotient + 2, 3))))


def direct_data(elements, source_frobenius):
    elements = set(elements)
    assert 0 in elements and source_frobenius not in elements
    assert all(left + right > source_frobenius or left + right in elements
               for left in elements for right in elements)
    gaps = set(range(source_frobenius + 1)) - elements
    positive = elements - {0}
    pseudo = {gap for gap in gaps if all(gap + value > source_frobenius or gap + value in elements
                                       for value in positive)}
    return gaps, pseudo


def direct_phi(elements, source_frobenius):
    gaps, pseudo = direct_data(elements, source_frobenius)
    assert 2 * len(gaps) == source_frobenius + len(pseudo)
    deleted = pseudo - {source_frobenius}
    return tuple(sorted(value - sum(gap < value for gap in deleted) for value in elements))


def independent_fixed_frobenius(maximum, known):
    checked = 0
    for source_frobenius in range(1, maximum + 1):
        for element_mask in range(1 << max(0, source_frobenius - 1)):
            elements = {0} | {value for value in range(1, source_frobenius)
                              if element_mask & (1 << (value - 1))}
            if not all(left + right > source_frobenius or left + right in elements
                       for left in elements for right in elements):
                continue
            checked += 1
            gap_bits = sum(1 << value for value in range(1, source_frobenius + 1) if value not in elements)
            assert (gap_bits, source_frobenius) in known
            gaps, pseudo = direct_data(elements, source_frobenius)
            if 2 * len(gaps) != source_frobenius + len(pseudo):
                continue
            result = direct_phi(elements, source_frobenius)
            assert result == compressed_elements(gap_bits, source_frobenius, bit_pseudo(gap_bits, source_frobenius))
            if len(result) >= 2 and result[1] == 3:
                assert result in {even_tail(len(result)), triple_family(len(result))}
    assert checked == len(known)
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-source-frobenius", type=int, default=35)
    parser.add_argument("--independent-maximum", type=int, default=18)
    parser.add_argument("--construction-maximum", type=int, default=100)
    parser.add_argument("--output", type=Path, default=Path("multiplicity3_checks.json"))
    args = parser.parse_args()
    if not 1 <= args.independent_maximum <= args.maximum_source_frobenius:
        parser.error("Require 1 <= independent-maximum <= maximum-source-frobenius")
    if args.construction_maximum < 3:
        parser.error("Require construction-maximum >= 3")
    source_count = 0
    almost_count = 0
    multiplicity_three_sources = 0
    general_bound_count = 0
    images = {}
    independent_known = set()
    for gap_bits, source_frobenius, genus in source_semigroups(args.maximum_source_frobenius):
        source_count += 1
        if source_frobenius <= args.independent_maximum:
            independent_known.add((gap_bits, source_frobenius))
        pseudo = bit_pseudo(gap_bits, source_frobenius)
        if 2 * genus != source_frobenius + len(pseudo):
            continue
        almost_count += 1
        output = compressed_elements(gap_bits, source_frobenius, pseudo)
        half = len(output)
        assert output[0] == 0
        assert source_frobenius - len(pseudo) + 1 == 2 * half - 1
        if half < 2:
            continue
        output_multiplicity = output[1]
        positive = [value for value in range(1, source_frobenius + 1) if not (gap_bits >> value) & 1]
        source_multiplicity = positive[0]
        assert output_multiplicity <= half
        chain_count = sum(value - source_multiplicity not in positive and value != source_multiplicity
                          for value in positive) + 1
        assert chain_count == output_multiplicity - 1
        if half > output_multiplicity:
            assert source_multiplicity <= 2 * output_multiplicity - 2
            assert source_frobenius <= 2 * half + 2 * output_multiplicity - 5
            general_bound_count += 1
        if output_multiplicity == 3:
            multiplicity_three_sources += 1
            assert output in {even_tail(half), triple_family(half)}
            images.setdefault(half, set()).add(output)
    construction_checks = 0
    for half in range(3, args.construction_maximum + 1):
        even_source = {0} | set(range(4, 2 * half + 1, 2))
        assert direct_phi(even_source, 2 * half + 1) == even_tail(half)
        if half % 3 != 2:
            source = set(triple_family(half))
            assert direct_phi(source, 2 * half - 1) == triple_family(half)
        else:
            source = set(range(0, 2 * half + 1, 3)) | set(range(half + 3, 2 * half + 1, 3))
            assert direct_phi(source, 2 * half) == triple_family(half)
        construction_checks += 2
    independent_count = independent_fixed_frobenius(args.independent_maximum, independent_known)
    target_counts = []
    largest_complete_half = (args.maximum_source_frobenius - 1) // 2
    for half in range(3, largest_complete_half + 1):
        expected = {even_tail(half), triple_family(half)}
        assert images[half] == expected
        assert len(expected) == (1 if half <= 5 else 2)
        target_counts.append(dict(frobenius=2 * half - 1, image_count=len(expected),
                                 left_elements=[list(elements) for elements in sorted(expected)]))
    if args.maximum_source_frobenius == 35:
        assert source_count == 840170
        assert almost_count == 17842
    result = dict(maximum_source_frobenius=args.maximum_source_frobenius,
                  proper_semigroups=source_count, almost_symmetric_sources=almost_count,
                  multiplicity_three_sources=multiplicity_three_sources,
                  general_source_bound_checks=general_bound_count,
                  independent_maximum=args.independent_maximum, independent_semigroups=independent_count,
                  construction_half_range=[3, args.construction_maximum], construction_checks=construction_checks,
                  complete_target_frobenius_maximum=2 * largest_complete_half - 1,
                  classification=target_counts,
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "classification"}, sort_keys=True))


if __name__ == "__main__":
    main()

from typing import Callable


def repeats(n: int) -> bool:
    """Two adjacent digits are the same."""
    s = str(n)
    return any(x == y for x, y in zip(s, s[1:]))


def repeats_careful(n: int) -> bool:
    """Has two adjacent matching digits which aren't part of a larger group."""
    s = str(n)
    saved, count = s[0], 1
    for c in s[1:]:
        if c == saved:
            count += 1
        else:
            if count == 2:
                return True
            saved, count = c, 1
    return count == 2


def increases(n: int) -> bool:
    """Going from left to right, the digits never decrease."""
    return int(''.join(sorted(str(n)))) == n


def match_all(n: int, *predicates: Callable[[int], bool]) -> bool:
    return all(p(n) for p in predicates)


def part_1(lo: int, hi: int) -> int:
    r = range(lo, hi + 1)
    return sum(match_all(n, repeats, increases) for n in r)


def part_2(lo: int, hi: int) -> int:
    r = range(lo, hi + 1)
    return sum(match_all(n, repeats_careful, increases) for n in r)


def test_cases_part_1():
    cases = [
        (111111, True),
        (223450, False),
        (123789, False),
    ]
    for x, y in cases:
        assert match_all(x, repeats, increases) == y


def test_cases_part_2():
    cases = [
        (112233, True),
        (123444, False),
        (111122, True),
    ]
    for x, y in cases:
        assert match_all(x, repeats_careful, increases) == y


def test_solution_part_1():
    lo, hi = 246540, 787419
    assert part_1(lo, hi) == 1063


def test_solution_part_2():
    lo, hi = 246540, 787419
    assert part_2(lo, hi) == 686
from typing import Callable

import numpy as np


def repeats(n: int) -> bool:
    """Two adjacent digits are the same."""
    s = str(n)
    return any(x == y for x, y in zip(s, s[1:]))


def repeats_careful(n: int) -> bool:
    """Has two adjacent matching digits which aren't part of a larger group."""
    digits = list(map(int, list(str(n))))
    return any(np.bincount(digits) == 2)


def increases(n: int) -> bool:
    """Going from left to right, the digits never decrease."""
    s = str(n)
    return list(s) == sorted(s)


def match_all(n: int, *predicates: Callable[[int], bool]) -> bool:
    # For speed, put faster or more restrictive filters first!
    return all(p(n) for p in predicates)


def part_1(lo: int, hi: int) -> int:
    r = range(lo, hi + 1)
    return sum(match_all(n, increases, repeats) for n in r)


def part_2(lo: int, hi: int) -> int:
    r = range(lo, hi + 1)
    # All Part 2 passwords are also Part 1 passwords, so we can use all three
    # filters. This is actually faster, since the most expensive filter
    # (repeats_careful) isn't run as often.
    return sum(match_all(n, increases, repeats, repeats_careful) for n in r)


def test_cases_part_1():
    cases = [
        (111111, True),
        (223450, False),
        (123789, False),
    ]
    for x, y in cases:
        assert match_all(x, increases, repeats) == y


def test_cases_part_2():
    cases = [
        (112233, True),
        (123444, False),
        (111122, True),
    ]
    for x, y in cases:
        assert match_all(x, increases, repeats, repeats_careful) == y


def test_solution_part_1():
    lo, hi = 246540, 787419
    assert part_1(lo, hi) == 1063


def test_solution_part_2():
    lo, hi = 246540, 787419
    assert part_2(lo, hi) == 686

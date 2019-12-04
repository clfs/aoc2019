from typing import Callable, Iterable

import numpy as np  # type: ignore


def increases(n: int) -> bool:
    """Going from left to right, the digits never decrease."""
    s = str(n)
    return list(s) == sorted(s)


def repeats(n: int) -> bool:
    """Two adjacent digits are the same."""
    s = str(n)
    return any(x == y for x, y in zip(s, s[1:]))


def repeats_careful(n: int) -> bool:
    """Has two adjacent matching digits which aren't part of a larger group."""
    digits = list(map(int, list(str(n))))
    return any(np.bincount(digits) == 2)


def sweep(it: Iterable[int], *filters: Callable[[int], bool]) -> Iterable[int]:
    # For speed, put faster or less frequently passing filters first!
    for f in filters:
        it = filter(f, it)
    return it


def part_1(lo: int, hi: int) -> int:
    r = range(lo, hi + 1)
    return len(list(sweep(r, increases, repeats)))


def part_2(lo: int, hi: int) -> int:
    r = range(lo, hi + 1)
    # All Part 2 passwords are also Part 1 passwords, so using three filters is
    # a little faster than just two.
    return len(list(sweep(r, increases, repeats, repeats_careful)))


def test_cases_part_1() -> None:
    cases = [
        (111111, True),
        (223450, False),
        (123789, False),
    ]
    for x, y in cases:
        assert (increases(x) and repeats(x)) == y


def test_cases_part_2() -> None:
    cases = [
        (112233, True),
        (123444, False),
        (111122, True),
    ]
    for x, y in cases:
        assert (increases(x) and repeats_careful(x)) == y


def test_solutions() -> None:
    lo, hi = 246540, 787419
    assert part_1(lo, hi) == 1063
    assert part_2(lo, hi) == 686

def is_sorted(s: str) -> bool:
    """Is s a sorted string?"""
    return list(s) == sorted(s)


def is_group_in_sorted(s: str) -> bool:
    """Assuming s is sorted, is there a repeated character?"""
    return any(x >= 2 for x in map(s.count, s))


def is_pair_in_sorted(s: str) -> bool:
    """Assuming s is sorted, is a there a character repeated only twice?"""
    return any(x == 2 for x in map(s.count, s))


def check_1(password: str) -> bool:
    return is_sorted(password) and is_group_in_sorted(password)


def check_2(password: str) -> bool:
    return is_sorted(password) and is_pair_in_sorted(password)


def part_1(lo: int, hi: int) -> int:
    passwords = map(str, range(lo, hi + 1))
    return sum(check_1(p) for p in passwords)


def part_2(lo: int, hi: int) -> int:
    passwords = map(str, range(lo, hi + 1))
    return sum(check_2(p) for p in passwords)


def test_cases_part_1() -> None:
    cases = [
        ("111111", True),
        ("223450", False),
        ("123789", False),
    ]
    for x, y in cases:
        assert check_1(x) == y


def test_cases_part_2() -> None:
    cases = [
        ("112233", True),
        ("123444", False),
        ("111122", True),
    ]
    for x, y in cases:
        assert check_2(x) == y


def test_solutions() -> None:
    lo, hi = 246540, 787419
    assert part_1(lo, hi) == 1063
    assert part_2(lo, hi) == 686

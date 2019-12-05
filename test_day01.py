def fuel_required(module: int) -> int:
    return module // 3 - 2


def fuel_required_accurate(module: int) -> int:
    fuel, n = 0, module
    while n > 0:
        n = max(0, n // 3 - 2)
        fuel += n
    return fuel


def test_fuel_required() -> None:
    cases = [
        (12, 2),
        (14, 2),
        (1969, 654),
        (100756, 33583),
    ]
    for x, y in cases:
        assert fuel_required(x) == y


def test_fuel_required_accurate() -> None:
    cases = [
        (14, 2),
        (1969, 966),
        (100756, 50346),
    ]
    for x, y in cases:
        assert fuel_required_accurate(x) == y


def test_solutions() -> None:
    with open("input/01.txt") as f:
        modules = [int(line) for line in f]

    part_1 = sum(map(fuel_required, modules))
    part_2 = sum(map(fuel_required_accurate, modules))
    assert part_1 == 3375962
    assert part_2 == 5061072

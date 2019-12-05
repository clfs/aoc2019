def fuel_required(weight: int) -> int:
    return weight // 3 - 2


def fuel_required_accurate(weight: int) -> int:
    fuel = 0
    while weight > 0:
        weight = max(0, weight // 3 - 2)
        fuel += weight
    return fuel


def test_fuel_required() -> None:
    cases = [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
    for x, y in cases:
        assert fuel_required(x) == y


def test_fuel_required_accurate() -> None:
    cases = [(14, 2), (1969, 966), (100756, 50346)]
    for x, y in cases:
        assert fuel_required_accurate(x) == y


def test_solutions() -> None:
    with open("input/01.txt") as f:
        modules = [int(line) for line in f]

    part_1 = sum(map(fuel_required, modules))
    part_2 = sum(map(fuel_required_accurate, modules))
    assert part_1 == 3375962
    assert part_2 == 5061072

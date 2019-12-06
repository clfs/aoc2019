from typing import List

import networkx as nx  # type: ignore


def part_1(data: List[List[str]]) -> int:
    g = nx.Graph()
    g.add_edges_from(data)
    # The shortest path is the number of direct orbits (1, or 0 for COM), plus
    # the number of indirect orbits (0 or more).
    return sum(nx.shortest_path_length(g, n, "COM") for n in g.nodes)


def part_2(data: List[List[str]]) -> int:
    g = nx.Graph()
    g.add_edges_from(data)
    # Subtract 2, since Santa and I both "start" at the objects we're
    # respectively orbiting. The unnecessary int() is for the return type
    # annotation.
    return int(nx.shortest_path_length(g, "YOU", "SAN")) - 2


def parse(s: str) -> List[List[str]]:
    return [line.split(")") for line in s.split()]


def test_cases_part_1() -> None:
    x = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L"
    y = 42
    assert part_1(parse(x)) == y


def test_case_part_2() -> None:
    x = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN"
    y = 4
    assert part_2(parse(x)) == y


def test_solutions() -> None:
    with open("input/06.txt") as f:
        data = parse(f.read())

    assert part_1(data) == 162439
    assert part_2(data) == 367

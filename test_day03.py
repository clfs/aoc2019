from typing import Iterator, List, Set

DIRECTIONS = {
    "R": 1,
    "U": 1j,
    "L": -1,
    "D": -1j,
}


def to_moves(wire: str) -> List[complex]:
    """Encode a wire as moves.

    For example, "D2,R1" becomes [-2j, 1].
    """
    moves = []
    for token in wire.split(","):
        direction, distance = token[0], int(token[1:])  # str, int
        m = distance * DIRECTIONS[direction]
        moves.append(m)
    return moves


def walk(wire: str) -> Iterator[complex]:
    """Walk a wire and yield each point visited, excluding the starting point.

    For example, "D2,R1" yields -1j, -2j, and -2j+1.
    """
    head = 0 + 0j  # Isn't yielded.
    for move in to_moves(wire):
        for step in steps(move):
            head += step
            yield head


def steps(move: complex) -> Iterator[complex]:
    """Stroll along and yield a series of steps.

    For example, steps(3j) yields 1j, 1j, and 1j.
    """
    magnitude = int(abs(move))
    step = move / magnitude
    for _ in range(magnitude):
        yield step


def intersections(w1: str, w2: str) -> Set[complex]:
    """Return the set of points at which two wires intersect."""
    return set(walk(w1)).intersection(walk(w2))


def manhattan_dist(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def part_1(w1: str, w2: str) -> int:
    """Return the Manhattan distance to the most central intersection."""
    points = intersections(w1, w2)
    heuristic = lambda p: manhattan_dist(0 + 0j, p)
    return min(map(heuristic, points))


def part_2(w1: str, w2: str) -> int:
    # Brute-force, with much more big-O space than needed :(
    p1 = list(walk(w1))
    p2 = list(walk(w2))
    # Add 2, since .index() starts at 0.
    heuristic = lambda p: p1.index(p) + p2.index(p) + 2
    return min(map(heuristic, intersections(w1, w2)))


def test_cases_part_1():
    cases = [
        (
            "R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "U62,R66,U55,R34,D71,R55,D58,R83",
            159,
        ),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            135,
        ),
    ]
    for x, y, z in cases:
        assert part_1(x, y) == z


def test_cases_part_2():
    cases = [
        (
            "R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "U62,R66,U55,R34,D71,R55,D58,R83",
            610,
        ),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            410,
        ),
    ]
    for x, y, z in cases:
        assert part_2(x, y) == z


def test_solution_part_1():
    with open("input/03.txt") as f:
        w1, w2 = [line.strip() for line in f]

    assert part_1(w1, w2) == 1264


def test_solution_part_2():
    with open("input/03.txt") as f:
        w1, w2 = [line.strip() for line in f]

    assert part_2(w1, w2) == 37390

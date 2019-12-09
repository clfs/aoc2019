import enum
from typing import Any, List


class Color(enum.IntEnum):
    BLACK = 0
    WHITE = 1
    CLEAR = 2


def is_colored(pixel: int) -> bool:
    return pixel != Color.CLEAR


def blocks(x: Any, n: int) -> List[Any]:
    return [x[i:i + n] for i in range(0, len(x), n)]


def shrink(mound: Any) -> int:
    # Type-checking this one is pretty difficult :(
    return int(next(filter(is_colored, mound), Color.CLEAR))


def collapse(layers: List[List[int]]) -> List[int]:
    return [shrink(mound) for mound in zip(*layers)]


def show(view: List[int], w: int) -> str:
    s = "".join(map(str, view))
    return "\n".join(blocks(s, w))


def part_1(digits: List[int], w: int, h: int) -> int:
    layers = blocks(digits, w * h)

    def heuristic(layer: List[int]) -> int:
        return layer.count(0)

    layer = min(layers, key=heuristic)
    # Unnecessary int() to please the type checker.
    return int(layer.count(1) * layer.count(2))


def part_2(digits: List[int], w: int, h: int) -> str:
    layers = blocks(digits, w * h)
    return show(collapse(layers), w)


def test_cases_part_2() -> None:
    digits, w, h = [0, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 2, 0, 0, 0, 0], 2, 2
    answer = "01\n10"

    assert part_2(digits, w, h) == answer


def test_solutions() -> None:
    with open("input/08.txt") as f:
        digits = [int(c) for c in f.read().strip()]
    w, h = 25, 6

    assert part_1(digits, w, h) == 2016
    assert part_2(digits, w, h) == ("1001011110011001111010010\n"
                                    "1001000010100100001010010\n"
                                    "1111000100100000010010010\n"
                                    "1001001000100000100010010\n"
                                    "1001010000100101000010010\n"
                                    "1001011110011001111001100")  # HZCZU

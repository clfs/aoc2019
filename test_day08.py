import enum
from typing import List

class Color(enum.IntEnum):
    BLACK = 0
    WHITE = 1
    TRANS = 2

def add(top: int, bot: int) -> int:
    if top == bot:
        return top
    if top == 2:
        return bot
    if top == 1:
        return 1
    if top == 0:
        return 0
"""
def add(top: Color, bot: Color) -> Color:
    if top == bot:
        return top
    if top == Color.BLACK and bot == Color.WHITE:
        return Color.BLACK
    if top == Color.BLACK and bot == Color.TRANS:
        return Color.BLACK
    if top == Color.WHITE and bot == Color.BLACK:
        return Color.WHITE
    if top == Color.WHITE and bot == Color.TRANS:
        return Color.WHITE
    if top == Color.TRANS and bot == Color.BLACK:
        return Color.BLACK
    if top == Color.TRANS and bot == Color.WHITE:
        return Color.White
    raise RuntimeError("bad addition")
"""
def zero_count(s) -> int:
    return s.count(0)

def blocks(s, w) -> List[str]:
    b = [s[i:i+w] for i in range(0, len(s), w)]
    return b

def print_picture(s, w, h):
    b = blocks(s, w*h)
    ov = overlay(b)
    a = blocks(ov, w)
    print("")
    for j in a:
        print(j)

def part_1(data, w, h) -> int:
    window_size = w * h
    b = blocks(data, window_size)
    magic = min(b, key=zero_count)
    return magic.count(1) * magic.count(2)

def overlay(x: List[List[str]]) -> str:
    ret = x[0]
    for layer in x[1:]:
        ret = add_layer(ret, layer)
    return ret

def add_layer(a: str, b: str) -> str:
    c = []
    for x, y in zip(a, b):
        c.append(add(int(x), int(y)))
    return ''.join(map(str, c))

def part_2(data, w, h) -> int:
    window_size = w * h
    b = blocks(data, window_size)
    pic = overlay(b)
    print_picture(pic, w, h)


def test_cases_part_1() -> None:
    data = "123456789012"
    window_size = 2*3
    blocks = [data[i : i + window_size] for i in range(0, len(data), window_size)]

def test_cases_part_2() -> None:
    data = "0222112222120000"
    w, h = 2, 2
    part_2(data, w, h)

def test_solutions():
    with open("input/08.txt") as f:
        data = [int(c) for c in f.read() if c.isdigit()]
    w, h = 25, 6

    assert part_1(data, w, h) == 2016
    assert part_2(data, w, h) == None

import enum
from typing import List, Tuple


class Op(enum.IntEnum):
    ADD = 1
    MUL = 2
    HLT = 99


class VirtualMachine:
    # NOTE: The memory size is mutable, and set as large as the loaded program.
    def __init__(self) -> None:
        self.mem: List[int] = []

    def load(self, program: List[int]) -> None:
        self.mem = program[:]  # Deep copy to avoid bugs.

    def execute(self) -> None:
        pc = 0
        while True:
            op = self.mem[pc]
            pc += 1
            if op == Op.ADD:
                src1, src2, dst = self.mem[pc:pc + 3]
                pc += 3
                self.mem[dst] = self.mem[src1] + self.mem[src2]
            elif op == Op.MUL:
                src1, src2, dst = self.mem[pc:pc + 3]
                pc += 3
                self.mem[dst] = self.mem[src1] * self.mem[src2]
            elif op == Op.HLT:
                break
            else:
                raise RuntimeError("encountered invalid opcode")

    def read(self, location: int) -> int:
        return self.mem[location]

    def write(self, location: int, value: int) -> None:
        self.mem[location] = value

    def dump(self) -> List[int]:
        return self.mem


def find_desired_output(program: List[int],
                        desired_output: int,
                        max_noun: int = 100,
                        max_verb: int = 100) -> Tuple[int, int]:
    vm = VirtualMachine()
    for noun in range(max_noun + 1):
        for verb in range(max_verb + 1):
            vm.load(program)
            vm.write(1, noun)
            vm.write(2, verb)
            vm.execute()
            if desired_output == vm.read(0):
                return noun, verb
    raise RuntimeError("desired output could not be found")


def test_cases() -> None:
    cases = [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ]
    vm = VirtualMachine()
    for x, y in cases:
        vm.load(x)
        vm.execute()
        assert vm.dump() == y


def test_solution_part_1() -> None:
    with open("input/02.txt") as f:
        program = [int(n) for n in f.read().split(",")]

    vm = VirtualMachine()
    vm.load(program)
    vm.write(1, 12)
    vm.write(2, 2)
    vm.execute()
    assert vm.read(0) == 5866714


def test_solution_part_2() -> None:
    with open("input/02.txt") as f:
        program = [int(n) for n in f.read().split(",")]

    noun, verb = find_desired_output(program, 19690720)
    assert 100 * noun + verb == 5208

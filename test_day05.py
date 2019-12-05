import enum
from typing import Iterator, List, Tuple


class Op(enum.IntEnum):
    ADD = 1  # add
    MUL = 2  # multiply
    SAV = 3  # save
    OUT = 4  # output
    JIT = 5  # jump if true
    JIF = 6  # jump if false
    LTH = 7  # less than
    EQL = 8  # equals
    HLT = 99  # halt


ARITY = {
    Op.ADD: 3,
    Op.MUL: 3,
    Op.SAV: 1,
    Op.OUT: 1,
    Op.JIT: 2,
    Op.JIF: 2,
    Op.LTH: 3,
    Op.EQL: 3,
    Op.HLT: 0,
}


class Mode(enum.IntEnum):
    POS = 0
    IMM = 1


class VirtualMachine:
    # NOTE: The memory size is mutable, and set as large as the loaded program.
    def __init__(self) -> None:
        self.mem: List[int] = []
        self.pc: int = 0
        self.input: int = 0

    def load(self, program: List[int], program_input: int) -> None:
        self.mem = program[:]  # Deep copy, avoid bugs.
        self.pc = 0
        self.input = program_input

    def execute(self) -> Iterator[int]:
        while True:
            op, vals, locs = self.read()
            if op == Op.ADD:
                self.mem[locs[2]] = vals[0] + vals[1]
            elif op == Op.MUL:
                self.mem[locs[2]] = vals[0] * vals[1]
            elif op == Op.SAV:
                self.mem[locs[0]] = self.input
            elif op == Op.OUT:
                yield vals[0]
            elif op == Op.JIT:
                self.pc = vals[1] if vals[0] else self.pc
            elif op == Op.JIF:
                self.pc = vals[1] if not vals[0] else self.pc
            elif op == Op.LTH:
                self.mem[locs[2]] = int(vals[0] < vals[1])
            elif op == Op.EQL:
                self.mem[locs[2]] = int(vals[0] == vals[1])
            elif op == Op.HLT:
                break
            else:
                raise RuntimeError("encountered invalid opcode")

    def read(self) -> Tuple[int, List[int], List[int]]:
        """Return the opcode, a list of values, and a list of locations."""
        # Read the current instruction.
        ins = self.mem[self.pc]
        self.pc += 1
        # Determine the opcode.
        op = ins % 100
        # Start two lists, for values and locations.
        vals: List[int] = []
        locs: List[int] = []
        # Read each used mode, then save a value and optional location.
        for i in range(ARITY[Op(op)]):
            mode = ins // pow(10, 2 + i) % 10
            if mode == Mode.POS:
                vals.append(self.mem[self.mem[self.pc]])
                locs.append(self.mem[self.pc])
            elif mode == Mode.IMM:
                vals.append(self.mem[self.pc])
                locs.append(-1)
            else:
                raise RuntimeError("encountered invalid mode")
            self.pc += 1
        return op, vals, locs

    def memory_dump(self) -> List[int]:
        return self.mem[:]  # Deep copy, avoid bugs.


def test_input_is_output() -> None:
    """Does this program output its own input?"""
    program = [3, 0, 4, 0, 99]
    program_input = 1337  # Arbitrary.

    vm = VirtualMachine()
    vm.load(program, program_input)
    assert next(vm.execute()) == program_input


def test_params_parsing() -> None:
    """Are the first arg's parameter modes parsed correctly?"""
    program = [1002, 4, 3, 4, 33]
    program_input = 420  # Unused.

    vm = VirtualMachine()
    vm.load(program, program_input)
    for _ in vm.execute():
        pass  # discard output
    want = [1002, 4, 3, 4, 99]
    got = vm.memory_dump()
    assert want == got


def test_input_comparisons() -> None:
    """Do these programs correctly compare inputs against values?"""
    cases = [
        (
            # Using position mode, is the input equal to 8?
            [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8],
            [(-1, 0), (0, 0), (8, 1), (9, 0)],
        ),
        (
            # Using position mode, is the input less than 8?
            [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8],
            [(-1, 1), (0, 1), (8, 0), (9, 0)],
        ),
        (
            # Using immediate mode, is the input equal to 8?
            [3, 3, 1108, -1, 8, 3, 4, 3, 99],
            [(-1, 0), (0, 0), (8, 1), (9, 0)],
        ),
        (
            # Using immediate mode, is the input less than 8?
            [3, 3, 1107, -1, 8, 3, 4, 3, 99],
            [(-1, 1), (0, 1), (8, 0), (9, 0)],
        ),
        (
            # If less than 8, 999; if 8, 1000; if greater than 8, 1001.
            [
                3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20,
                31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1,
                46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1,
                46, 98, 99
            ],
            [(-1, 999), (0, 999), (8, 1000), (9, 1001)],
        ),
    ]

    vm = VirtualMachine()
    for program, pairs in cases:
        for x, y in pairs:
            vm.load(program, x)
            assert next(vm.execute()) == y


def test_solution_part_1() -> None:
    with open("input/05.txt") as f:
        program = [int(n) for n in f.read().split(",")]
    program_input = 1

    vm = VirtualMachine()
    vm.load(program, program_input)
    *test_codes, answer = (output for output in vm.execute())
    assert all(t == 0 for t in test_codes)
    assert answer == 2845163


def test_solution_part_2() -> None:
    with open("input/05.txt") as f:
        program = [int(n) for n in f.read().split(",")]
    program_input = 5

    vm = VirtualMachine()
    vm.load(program, program_input)
    assert next(vm.execute()) == 9436229

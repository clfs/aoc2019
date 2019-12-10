from __future__ import annotations
import enum
from typing import Iterator, List, Tuple
from queue import Queue


class Op(enum.IntEnum):
    ADD = 1  # add
    MUL = 2  # multiply
    SAV = 3  # save
    OUT = 4  # output
    JIT = 5  # jump if true
    JIF = 6  # jump if false
    LTH = 7  # less than
    EQL = 8  # equals
    IRB = 9  # increment relative base
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
    Op.IRB: 1,
    Op.HLT: 0,
}


class Mode(enum.IntEnum):
    POS = 0
    IMM = 1
    REL = 2


class State(enum.IntEnum):
    BLOCKED = 0
    HALTED = 1


VM_MEMSIZE = 10000


class VirtualMachine:
    # NOTE: The memory size is mutable, and set as large as the loaded program.
    def __init__(self) -> None:
        self.mem: List[int] = [0] * VM_MEMSIZE
        self.pc: int = 0
        self.rb: int = 0
        self.input: Queue[int] = Queue()
        self.output: Queue[int] = Queue()

    def load(self, program: List[int]) -> None:
        self.mem = [0] * VM_MEMSIZE  # Wipe the memory.
        self.mem[:len(program)] = program[:]  # Deep copy, avoid bugs.

    def rx_from(self, vm: VirtualMachine) -> None:
        # Must be run *before* manually pushing inputs. Bonus fact: this
        # function type signature is only possible with __future__.
        self.input = vm.output

    def push_input(self, inp: int) -> None:
        self.input.put(inp)

    def pop_output(self) -> int:
        return self.output.get()

    def execute(self) -> Iterator[State]:
        """Yield State.BLOCKED or State.HALTED."""
        while True:
            op, vals, locs = self.read()
            if op == Op.ADD:
                self.mem[locs[2]] = vals[0] + vals[1]
            elif op == Op.MUL:
                self.mem[locs[2]] = vals[0] * vals[1]
            elif op == Op.SAV:
                while self.input.empty():
                    yield State.BLOCKED
                self.mem[locs[0]] = self.input.get()  # Blocking.
            elif op == Op.OUT:
                self.output.put(vals[0])
            elif op == Op.JIT:
                self.pc = vals[1] if vals[0] else self.pc
            elif op == Op.JIF:
                self.pc = vals[1] if not vals[0] else self.pc
            elif op == Op.LTH:
                self.mem[locs[2]] = int(vals[0] < vals[1])
            elif op == Op.EQL:
                self.mem[locs[2]] = int(vals[0] == vals[1])
            elif op == Op.IRB:
                self.rb += vals[0]
            elif op == Op.HLT:
                while True:
                    yield State.HALTED
            else:
                raise RuntimeError(f"encountered invalid opcode {op}")

    def exhaust(self) -> None:
        e = self.execute()
        while next(e) != State.HALTED:
            pass

    def drain(self) -> Iterator[int]:
        while not self.output.empty():
            yield self.output.get()

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
            elif mode == Mode.REL:
                vals.append(self.mem[self.rb + self.mem[self.pc]])
                locs.append(self.rb + self.mem[self.pc])
            else:
                raise RuntimeError(f"encountered invalid mode {mode}")
            self.pc += 1
        return op, vals, locs

    def memory_dump(self) -> List[int]:
        return self.mem[:]  # Deep copy, avoid bugs.


def parse(s: str) -> List[int]:
    return [int(n) for n in s.split(",")]


def test_cases_part_1() -> None:
    cases = [
        (
            # Quine.
            "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99",
            [
                109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006,
                101, 0, 99
            ],
        ),
        (
            # 16-digit number.
            "1102,34915192,34915192,7,4,7,99,0",
            [1219070632396864],
        ),
        (
            # Large number in the middle.
            "104,1125899906842624,99",
            [1125899906842624],
        ),
    ]
    for x, y in cases:
        vm = VirtualMachine()
        program = parse(x)
        vm.load(program)
        vm.exhaust()
        assert list(vm.drain()) == y


def part_1(program: List[int]) -> int:
    vm = VirtualMachine()
    vm.load(program)
    vm.push_input(1)
    vm.exhaust()
    *test_codes, boost_keycode = list(vm.drain())
    assert all(t == 0 for t in test_codes)
    return boost_keycode


def part_2(program: List[int]) -> int:
    vm = VirtualMachine()
    vm.load(program)
    vm.push_input(2)
    vm.exhaust()
    coordinates = next(vm.drain())
    return coordinates


def test_solutions() -> None:
    with open("input/09.txt") as f:
        program = parse(f.read())

    assert part_1(program) == 3429606717
    assert part_2(program) == 33679

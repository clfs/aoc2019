from __future__ import annotations
import enum
import itertools
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


class State(enum.IntEnum):
    BLOCKED = 0
    HALTED = 1


class VirtualMachine:
    # NOTE: The memory size is mutable, and set as large as the loaded program.
    def __init__(self) -> None:
        self.mem: List[int] = []
        self.pc: int = 0
        self.input: Queue[int] = Queue()
        self.output: Queue[int] = Queue()

    def load(self, program: List[int]) -> None:
        self.mem = program[:]  # Deep copy, avoid bugs.

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
            elif op == Op.HLT:
                while True:
                    yield State.HALTED
            else:
                raise RuntimeError(f"encountered invalid opcode {op}")

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
                raise RuntimeError(f"encountered invalid mode {mode}")
            self.pc += 1
        return op, vals, locs

    def memory_dump(self) -> List[int]:
        return self.mem[:]  # Deep copy, avoid bugs.


def simulate(vms: List[VirtualMachine]) -> List[VirtualMachine]:
    running_vms = [vm.execute() for vm in vms]
    while True:
        for i, r in enumerate(running_vms):
            state = next(r)
            if (i == len(vms) - 1) and (state == State.HALTED):
                return vms


def part_1(program: List[int]) -> int:
    best_signal = 0
    for permutation in itertools.permutations(range(5)):
        signal = 0
        for phase in permutation:
            vm = VirtualMachine()
            vm.load(program)
            vm.push_input(phase)
            vm.push_input(signal)
            _ = next(vm.execute())
            signal = vm.pop_output()
        best_signal = max(best_signal, signal)
    return best_signal


def part_2(program: List[int]) -> int:
    best_signal = 0
    for permutation in itertools.permutations(range(5, 10)):
        print(f"=== PERMUTATION {permutation} ===")
        # Create enough VMs.
        vms = [VirtualMachine() for _ in range(len(permutation))]
        # Have each VM load the program.
        for vm in vms:
            vm.load(program)
        # Set each VM to recieve input from the VM immediately before it.
        for i, vm in enumerate(vms):
            vm.rx_from(vms[(i - 1) % len(vms)])  # -1 % 5 == 4
        # Push each phase input to its respective VM input queue.
        for i, phase in enumerate(permutation):
            vms[i].push_input(phase)
        # Push the initial 0 signal to the first VM.
        vms[0].push_input(0)
        # Execute all VMs.
        vms = simulate(vms)
        # Get the output from the last VM, and see if it's any better.
        print(*vms, sep='\n')
        signal = vms[-1].pop_output()
        best_signal = max(best_signal, signal)
    return best_signal


def parse(s: str) -> List[int]:
    return [int(n) for n in s.split(",")]


def test_cases_part_1() -> None:
    cases = [
        (
            "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",
            43210,
        ),
        (
            "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
            54321,
        ),
        (
            "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
            65210,
        ),
    ]
    for x, y in cases:
        assert part_1(parse(x)) == y


def test_cases_part_2() -> None:
    cases = [
        (
            "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
            139629729,
        ),
        (
            "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10",
            18216,
        ),
    ]
    for x, y in cases:
        assert part_2(parse(x)) == y


def test_solutions() -> None:
    with open("input/07.txt") as f:
        program = parse(f.read())

    assert part_1(program) == 117312
    assert part_2(program) == 1336480

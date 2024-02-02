import enum
import operator


class Opcode(enum.IntEnum):
    ADD = 1
    MULTIPLY = 2
    HALT = 99


class Computer:
    memory: list[int]
    pointer: int
    opcode_map: dict[Opcode, operator] = {
        Opcode.ADD: operator.add,
        Opcode.MULTIPLY: operator.mul,
    }

    def __init__(self) -> None:
        self.restart()

    def restart(self) -> None:
        self.memory = []
        self.pointer = 0

    def run(self, program: list[int]) -> None:
        self.memory = program.copy()

        while self.memory[self.pointer] != Opcode.HALT:
            self._run_instruction()

    def _run_instruction(self) -> None:
        opcode = Opcode(self.memory[self.pointer])
        val1, val2 = self.memory[self.pointer + 1], self.memory[self.pointer + 2]
        output = self.memory[self.pointer + 3]

        self.memory[output] = self.opcode_map[opcode](
            self.memory[val1], self.memory[val2]
        )
        self.pointer += 4

import dataclasses
import enum
import functools
import operator


class Opcode(enum.IntEnum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


class Mode(enum.IntEnum):
    POSITION = 0
    IMMEDIATE = 1


@dataclasses.dataclass
class Instruction:
    opcode: Opcode
    modes: list[Mode]


class Computer:
    memory: list[int]
    pointer: int
    input: int
    output: int
    opcode_map: dict[Opcode, operator]

    def __init__(self) -> None:
        self.opcode_map = {
            Opcode.ADD: self._add,
            Opcode.MULTIPLY: self._multiply,
            Opcode.INPUT: self._input,
            Opcode.OUTPUT: self._output,
            Opcode.JUMP_IF_TRUE: self._jump_if_true,
            Opcode.JUMP_IF_FALSE: self._jump_if_false,
            Opcode.LESS_THAN: self._less_than,
            Opcode.EQUALS: self._equals,
        }
        self.restart()

    @functools.cached_property
    def current_instruction(self) -> Instruction:
        instruction = str(self.memory[self.pointer]).rjust(5, "0")
        return Instruction(
            opcode=Opcode(int(instruction[3:5])),
            modes=[
                Mode(int(instruction[2])),
                Mode(int(instruction[1])),
                Mode(int(instruction[0])),
            ],
        )

    def _invalidate_instruction_cache(self) -> None:
        if "current_instruction" in self.__dict__:
            del self.current_instruction  # noqa

    def restart(self) -> None:
        self.memory = []
        self.input = 0
        self.output = 0
        self.pointer = 0
        self._invalidate_instruction_cache()

    def run(self, program: list[int], input_data: int = 0) -> int:
        self.memory = program.copy()
        self.input = input_data

        while self.current_instruction.opcode != Opcode.HALT:
            self._run_instruction()

        return self.output

    def _run_instruction(self) -> None:
        self.opcode_map[self.current_instruction.opcode]()
        self._invalidate_instruction_cache()

    def _get_memory_addresses(self, nr_of_params: int) -> list[int]:
        data = []
        for i in range(nr_of_params):
            address = self.pointer + i + 1
            if self.current_instruction.modes[i] == Mode.POSITION:
                data.append(self.memory[address])
            elif self.current_instruction.modes[i] == Mode.IMMEDIATE:
                data.append(address)
            else:
                raise ValueError("Invalid mode")

        return data

    def _add(self) -> None:
        address1, address2, address3 = self._get_memory_addresses(nr_of_params=3)
        value1, value2 = self.memory[address1], self.memory[address2]
        self.memory[address3] = value1 + value2
        self.pointer += 4

    def _multiply(self) -> None:
        address1, address2, address3 = self._get_memory_addresses(nr_of_params=3)
        value1, value2 = self.memory[address1], self.memory[address2]
        self.memory[address3] = value1 * value2
        self.pointer += 4

    def _input(self) -> None:
        address1 = self._get_memory_addresses(nr_of_params=1)[0]
        self.memory[address1] = self.input
        self.pointer += 2

    def _output(self) -> None:
        address1 = self._get_memory_addresses(nr_of_params=1)[0]
        self.output = self.memory[address1]
        self.pointer += 2

    def _jump_if_true(self) -> None:
        address1, address2 = self._get_memory_addresses(nr_of_params=2)
        value1, value2 = self.memory[address1], self.memory[address2]
        self.pointer = value2 if value1 else self.pointer + 3

    def _jump_if_false(self) -> None:
        address1, address2 = self._get_memory_addresses(nr_of_params=2)
        value1, value2 = self.memory[address1], self.memory[address2]
        self.pointer = value2 if not value1 else self.pointer + 3

    def _less_than(self) -> None:
        address1, address2, address3 = self._get_memory_addresses(nr_of_params=3)
        value1, value2 = self.memory[address1], self.memory[address2]
        self.memory[address3] = 1 if value1 < value2 else 0
        self.pointer += 4

    def _equals(self) -> None:
        address1, address2, address3 = self._get_memory_addresses(nr_of_params=3)
        value1, value2 = self.memory[address1], self.memory[address2]
        self.memory[address3] = 1 if value1 == value2 else 0
        self.pointer += 4

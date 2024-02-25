import copy
import itertools
from array import array

import ivan.aoc


class Computer:
    def __init__(self) -> None:
        self._memory = None

    @property
    def memory(self):
        return self._memory

    def get_input(self, year: int, day: int):
        return ivan.aoc.get_input(year, day)

    def parse_str_into_memory(self, inp: str, as_array_of_int: bool):
        if not as_array_of_int:
            self._memory = inp.split(",")
        else:
            self._memory = array("i", (int(i) for i in inp.split(",")))

    def _compute(self, program):
        """Compute an Intcode program"""

        def exec_instruction(opcode, param1_mode, param2_mode):
            a = next(program_iter)
            if param1_mode == 0:
                a = program[a]

            b = next(program_iter)
            if param2_mode == 0:
                b = program[b]

            pos = next(program_iter)

            if opcode == 1:
                program[pos] = a + b
            elif opcode == 2:
                program[pos] = a * b

        program_iter = iter(program)

        while True:
            try:
                value = next(program_iter)

                opcode_str = str(value)
                opcode_length = len(opcode_str)
                if opcode_length <= 2:
                    param1_mode, param2_mode, opcode = 0, 0, value
                elif opcode_length == 4:
                    param2_mode, param1_mode, _, opcode = (int(i) for i in opcode_str)
                else:
                    opcode = None

                if opcode == 1:  # opcode: sum
                    exec_instruction(opcode, param1_mode, param2_mode)
                    continue
                elif opcode == 2:  # opcode: mul
                    exec_instruction(opcode, param1_mode, param2_mode)
                    continue
                elif opcode == 3:  # opcode: input
                    inp = int(input("Provide input: "))
                    pos = next(program_iter)
                    program[pos] = inp
                    continue
                elif opcode == 4:  # opcode: output
                    pos = next(program_iter)
                    print(program[pos])
                    continue
                elif opcode == 99:  # opcode: halt
                    break
            except StopIteration:
                break
        return program

    def exec_day2p1(self, noun=12, verb=2):
        """Solution for Day 2, part 1."""

        memory_copy = copy.deepcopy(self.memory)
        memory_copy[1], memory_copy[2] = noun, verb
        result = self._compute(memory_copy)[0]
        return result

    def exec_day2p2(self):
        """Solution for Day 2, part 2."""
        for n, v in itertools.product(range(100), range(100)):
            memory_copy = copy.deepcopy(self.memory)
            memory_copy[1], memory_copy[2] = n, v
            result = self._compute(memory_copy)[0]

            if result == 19690720:
                return n, v, 100 * n + v

    def exec_day5p1(self):
        return self._compute(self.memory)


if __name__ == "__main__":
    c = Computer()

    c.parse_str_into_memory(c.get_input(2019, 2), as_array_of_int=True)

    d2p1 = c.exec_day2p1()
    print(f"Solution Day 2, part 1: {d2p1}")
    assert d2p1 == 4690667

    d2p2 = c.exec_day2p2()
    n, v, res = d2p2
    print(f"Solution Day 2, part 2: {n=}, {v=}, Result: {100 * n + v}")
    assert d2p2 == (62, 55, 6255)

    # c.parse_aoc_input(2019, 5)
    # c.exec_day5p1()

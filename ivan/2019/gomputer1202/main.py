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

    def parse_str_into_memory(self, inp: str):
        self._memory = array("i", (int(i) for i in inp.split(",")))

    def _compute(self, program: array):
        """Compute an Intcode program and return it back."""
        pointer = 0
        valid_opcodes = (1, 2, 3, 4, 99)
        valid_param_modes = (0, 1)

        def exec_instruction(opcode: int, param_modes: tuple):
            if len(param_modes) == 0:
                param_modes = (0, 0)
            elif len(param_modes) == 1:
                param_modes = (param_modes[0], 0)
            elif len(param_modes) == 2:
                param_modes = (param_modes[0], param_modes[1])
            else:
                raise ValueError("Invalid param_modes")

            a = program[pointer + 1]
            if param_modes[0] == 0:
                a = program[a]

            b = program[pointer + 2]
            if param_modes[1] == 0:
                b = program[b]

            pos = program[pointer + 3]

            if opcode == 1:
                program[pos] = a + b
            elif opcode == 2:
                program[pos] = a * b

            # for debugging
            # print(f"{opcode=}, {param_modes=}, {a=}, {b=}, {pos=}, {program[pos]=}")

        while True:
            try:
                opcode = program[pointer]
                # Handling parameter modes
                opcode_str = str(opcode)
                if len(opcode_str) == 1:
                    param_modes, opcode = (0, 0), opcode
                else:
                    opcode = int(opcode_str[-2:])
                    param_modes = tuple(int(p) for p in opcode_str[:-2][::-1])

                assert opcode in valid_opcodes
                assert set(param_modes).issubset(valid_param_modes)

                if opcode == 1:  # opcode: sum
                    exec_instruction(opcode, param_modes)
                    pointer += 4
                    continue
                elif opcode == 2:  # opcode: mul
                    exec_instruction(opcode, param_modes)
                    pointer += 4
                    continue
                elif opcode == 3:  # opcode: input
                    inp = int(input("Provide input: "))
                    idx = program[pointer + 1]
                    program[idx] = inp
                    pointer += 2
                    continue
                elif opcode == 4:  # opcode: output
                    idx = program[pointer + 1]
                    if param_modes == (1,):
                        result = idx
                    else:
                        result = program[idx]
                    print(f"{pointer=}, {result}")

                    pointer += 2
                    continue
                elif opcode == 99:  # opcode: halt
                    break
                else:
                    pointer += 1
            except IndexError:
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

    c.parse_str_into_memory(c.get_input(2019, 2))
    d2p1 = c.exec_day2p1()
    print(f"Solution Day 2, part 1: {d2p1}")
    assert d2p1 == 4690667

    d2p2 = c.exec_day2p2()
    n, v, res = d2p2
    print(f"Solution Day 2, part 2: {n=}, {v=}, Result: {100 * n + v}")
    assert d2p2 == (62, 55, 6255)

    c.parse_str_into_memory(c.get_input(2019, 5))
    c.exec_day5p1()

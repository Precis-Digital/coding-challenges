# %%
import copy
from array import array

import ivan.aoc


# %%
class Computer:
    def __init__(self) -> None:
        self._memory = None

    def parse_aoc_input(self, year: int, day: int):
        """Parse AOC input string (Intcode program) into memory.

        Parameters:
            year: int
                Year of the AOC puzzle.
            day: int
                Day of the AOC puzzle.
        """
        self._memory = array(
            "I", (int(n) for n in ivan.aoc.get_input(year, day).split(","))
        )

    @property
    def memory(self):
        return self._memory

    def _compute(self, noun: int = 0, verb: int = 0):
        """Compute the result of the Intcode program with the given noun and verb."""
        _memory = copy.deepcopy(self.memory)
        _memory[1], _memory[2] = noun, verb
        memory_iter = iter(_memory)
        while True:
            try:
                val = next(memory_iter)
                if val == 1:  # opcode: sum
                    a = _memory[next(memory_iter)]
                    b = _memory[next(memory_iter)]
                    pos = next(memory_iter)
                    _memory[pos] = a + b
                    continue
                elif val == 2:  # opcode: mul
                    a = _memory[next(memory_iter)]
                    b = _memory[next(memory_iter)]
                    pos = next(memory_iter)
                    _memory[pos] = a * b
                    continue
                elif val == 99:  # opcode: halt
                    raise StopIteration
            except StopIteration:
                break
        return _memory[0]

    def exec_day2p1(self):
        """Solution for Day 2, part 1."""
        return f"Solution Day 2, part 1: {self._compute(12, 2)}"

    def exec_day2p2(self):
        """Solution for Day 2, part 2."""
        for n in range(100):
            for v in range(100):
                if self._compute(n, v) == 19690720:
                    return f"Solution Day 2, part 2: {n=}, {v=}, Result: {100 * n + v}"


# %%
c = Computer()
c.parse_aoc_input(2019, 2)

print(c.exec_day2p1())
print(c.exec_day2p2())

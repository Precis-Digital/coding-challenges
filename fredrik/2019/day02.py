import itertools

from fredrik.shared import intcode, utils


def part1(program: list[int]) -> int:
    computer = intcode.Computer()
    program[1], program[2] = 12, 2
    computer.run(program=program)
    return computer.memory[0]


def part2(program: list[int]) -> int:
    program = program.copy()
    computer = intcode.Computer()
    for verb, noun in itertools.product(range(100), repeat=2):
        program[1], program[2] = noun, verb
        computer.run(program=program)
        if computer.memory[0] == 19690720:
            return 100 * noun + verb

        computer.restart()


def main() -> None:
    data = utils.read_input_to_string()
    program = list(map(int, data.split(",")))

    print(f"Part 1: {part1(program=program)}")
    print(f"Part 2: {part2(program=program)}")


if __name__ == "__main__":
    main()

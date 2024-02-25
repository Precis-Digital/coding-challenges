from fredrik.shared import intcode, utils


def run_with_output(program: list[int], input_data: int) -> int:
    computer = intcode.Computer()
    return computer.run(program=program, input_data=input_data)


def main() -> None:
    data = utils.read_input_to_string()
    program = list(map(int, data.split(",")))
    print(f"Part 1: {run_with_output(program=program, input_data=1)}")
    print(f"Part 2: {run_with_output(program=program, input_data=5)}")


if __name__ == "__main__":
    main()

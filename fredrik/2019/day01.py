from fredrik.shared import utils


def calculate_fuel_required(mass: int) -> int:
    return mass // 3 - 2


def part1(lines: list[str]) -> int:
    return sum(calculate_fuel_required(int(line)) for line in lines)


def part2(lines: list[str]) -> int:
    total_fuel = 0
    for line in lines:
        fuel = calculate_fuel_required(int(line))
        while fuel > 0:
            total_fuel += fuel
            fuel = calculate_fuel_required(fuel)
    return total_fuel


def main() -> None:
    data = utils.read_input_to_string().splitlines()

    print(f"Part 1: {part1(lines=data)}")
    print(f"Part 2: {part2(lines=data)}")


if __name__ == "__main__":
    main()

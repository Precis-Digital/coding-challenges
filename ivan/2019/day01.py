from math import floor

import ivan.aoc as aoc

inp = [int(mass) for mass in aoc.get_input(2019, 1).splitlines()]


def part_1():
    return sum(floor(mass / 3) - 2 for mass in inp)


print(f"Part 1: {part_1()}")


def part_2():
    def calc_fuel_rec(mass: int):
        fuel = floor(mass / 3) - 2
        if fuel <= 0:
            return 0
        else:
            return fuel + calc_fuel_rec(fuel)

    return sum(calc_fuel_rec(mass) for mass in inp)


print(f"Part 2: {part_2()}")

from __future__ import annotations

import dataclasses
import itertools
import math
import re

from fredrik.shared import utils


@dataclasses.dataclass
class Moon:
    x: int
    y: int
    z: int
    dx: int = 0
    dy: int = 0
    dz: int = 0

    @property
    def potential_energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def kinetic_energy(self) -> int:
        return abs(self.dx) + abs(self.dy) + abs(self.dz)

    @property
    def total_energy(self) -> int:
        return self.potential_energy * self.kinetic_energy

    @property
    def x_state(self) -> tuple[int, int]:
        return self.x, self.dx

    @property
    def y_state(self) -> tuple[int, int]:
        return self.y, self.dy

    @property
    def z_state(self) -> tuple[int, int]:
        return self.z, self.dz

    def apply_gravity(self, other: Moon) -> None:
        if self.x > other.x:
            self.dx -= 1
            other.dx += 1

        elif self.x < other.x:
            self.dx += 1
            other.dx -= 1

        if self.y > other.y:
            self.dy -= 1
            other.dy += 1

        elif self.y < other.y:
            self.dy += 1
            other.dy -= 1

        if self.z > other.z:
            self.dz -= 1
            other.dz += 1

        elif self.z < other.z:
            self.dz += 1
            other.dz -= 1

    def apply_velociy(self) -> None:
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz


@dataclasses.dataclass
class Universe:
    moons: list[Moon]
    initial_x_state: tuple[tuple[int, int], ...] | None = None
    initial_y_state: tuple[tuple[int, int], ...] | None = None
    initial_z_state: tuple[tuple[int, int], ...] | None = None
    x_cycle: int | None = None
    y_cycle: int | None = None
    z_cycle: int | None = None

    def __post_init__(self) -> None:
        self.initial_x_state = self.x_state
        self.initial_y_state = self.y_state
        self.initial_z_state = self.z_state

    @property
    def x_state(self) -> tuple[tuple[int, int], ...]:
        return tuple(moon.x_state for moon in self.moons)

    @property
    def y_state(self) -> tuple[tuple[int, int], ...]:
        return tuple(moon.y_state for moon in self.moons)

    @property
    def z_state(self) -> tuple[tuple[int, int], ...]:
        return tuple(moon.z_state for moon in self.moons)

    @property
    def all_cycles_found(self) -> bool:
        return all((self.x_cycle, self.y_cycle, self.z_cycle))

    def apply_gravity(self):
        for moon1, moon2 in itertools.combinations(self.moons, r=2):
            moon1.apply_gravity(other=moon2)

    def apply_velocity(self):
        for moon in self.moons:
            moon.apply_velociy()

    def total_energy(self) -> int:
        return sum(moon.total_energy for moon in self.moons)


def parse_moons(moons_raw: str) -> list[Moon]:
    moon_pattern = r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>"

    moons = []
    for line in moons_raw.splitlines():
        match = re.match(moon_pattern, line)
        x, y, z = (int(match.group(i)) for i in range(1, 4))
        moons.append(Moon(x=x, y=y, z=z))

    return moons


def part1(moons_raw) -> int:
    universe = Universe(moons=parse_moons(moons_raw=moons_raw))
    for _ in range(1000):
        universe.apply_gravity()
        universe.apply_velocity()

    return universe.total_energy()


def part2(moons_raw) -> int:
    universe = Universe(moons=parse_moons(moons_raw=moons_raw))

    steps = 0
    while not universe.all_cycles_found:
        universe.apply_gravity()
        universe.apply_velocity()

        steps += 1

        if not universe.x_cycle and universe.x_state == universe.initial_x_state:
            universe.x_cycle = steps

        if not universe.y_cycle and universe.y_state == universe.initial_y_state:
            universe.y_cycle = steps

        if not universe.z_cycle and universe.z_state == universe.initial_z_state:
            universe.z_cycle = steps

    return math.lcm(universe.x_cycle, universe.y_cycle, universe.z_cycle)


def main() -> None:
    moons_raw = utils.read_input_to_string()

    print(f"Part 1: {part1(moons_raw=moons_raw)}")
    print(f"Part 2: {part2(moons_raw=moons_raw)}")


if __name__ == "__main__":
    main()

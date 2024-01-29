import pprint
import re

import ivan.aoc as aoc

inp = [
    [int(pos) for pos in re.findall("\=(-\d+|\d+)", moon)]
    for moon in aoc.get_input(2019, 12).splitlines()
]

# aoc_inp = """<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>"""

# aoc_inp = """<x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>"""

# inp = [
#     tuple(int(pos) for pos in re.findall("\=(-\d+|\d+)", moon))
#     for moon in aoc_inp.splitlines()
# ]

# print(inp)


class JupiterMoon:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.state = {
            0: {
                "pos": {"x": self.x, "y": self.y, "z": self.z},
                "vel": {"x": 0, "y": 0, "z": 0},
            }
        }

    def __repr__(self):
        return f"{__class__.__name__}(x={self.x}, y={self.y}, z={self.z}"

    def potential_energy(self, ts):
        return sum(
            (
                abs(self.state[ts]["pos"]["x"]),
                abs(self.state[ts]["pos"]["y"]),
                abs(self.state[ts]["pos"]["z"]),
            )
        )

    def kinetic_energy(self, ts):
        return sum(
            (
                abs(self.state[ts]["vel"]["x"]),
                abs(self.state[ts]["vel"]["y"]),
                abs(self.state[ts]["vel"]["z"]),
            )
        )

    def total_energy(self, ts):
        return self.potential_energy(ts) * self.kinetic_energy(ts)


def part_1():
    def simulate(time_steps, moons):
        # print(f"After 0 step")
        # for m in moons:
        # pprint.pprint(m.state[0])

        for ts in range(time_steps):
            for m in moons:
                m.state[ts + 1] = m.state[ts].copy()

            for m in moons:
                for other in moons:
                    for c in ("x", "y", "z"):
                        if m.state[ts]["pos"][c] == other.state[ts]["pos"][c]:
                            continue
                        elif m.state[ts]["pos"][c] > other.state[ts]["pos"][c]:
                            m.state[ts + 1]["vel"][c] -= 1
                            other.state[ts + 1]["vel"][c] += 1

            # print(f"After {ts+1} step")
            for m in moons:
                for c in ("x", "y", "z"):
                    m.state[ts + 1]["pos"][c] = (
                        m.state[ts + 1]["vel"][c] + m.state[ts]["pos"][c]
                    )
                # pprint.pprint(m.state[ts + 1])

        return sum(m.total_energy(time_steps) for m in moons)

    moons = [JupiterMoon(*moon) for moon in inp]

    return simulate(1000, moons)


print(f"Part 1: {part_1()}")

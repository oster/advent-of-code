from dataclasses import dataclass
from icecream import ic
import functools
import re


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

    max_width: int = 0
    max_height: int = 0

    def move(self) -> None:
        self.x = (self.x + self.vx + self.max_width) % self.max_width
        self.y = (self.y + self.vy + self.max_height) % self.max_height

    def jump_at_time(self, times: int) -> None:
        self.x = (self.x + times * self.vx + self.max_width) % self.max_width
        self.y = (self.y + times * self.vy + self.max_height) % self.max_height


def read_data(filename: str) -> list[Robot]:
    robots = []
    with open(filename, "r") as data_file:
        for line in data_file:
            values = tuple(map(int, re.findall(r"-?\d+", line)))
            r = Robot(*values)
            # for line in data_file:
            #     p, v = line.strip().split(" ")
            #     p = p.split("=")[1].split(",")
            #     v = v.split("=")[1].split(",")
            # r = Robot(int(p[0]), int(p[1]), int(v[0]), int(v[1]))
            robots.append(r)
    return robots


def build_grid(robots: list[Robot], width: int, height: int) -> list[list[int]]:
    g = [[0 for _ in range(width)] for _ in range(height)]
    for r in robots:
        g[r.y][r.x] += 1
    return g


def print_grid(g: list[list[int]]) -> None:
    for col in g:
        for cell in col:
            if cell == 0:
                print(".", end="")
            else:
                print(cell, end="")
        print()


def count_by_quadran(robots: list[Robot], width: int, height: int) -> list[int]:
    quadran_width = width // 2
    quadran_height = height // 2

    quadrans = [0] * 4

    for r in robots:
        if r.x == quadran_width or r.y == quadran_height:
            continue

        if r.x < quadran_width:
            if r.y < quadran_height:
                quadrans[0] += 1
            else:
                quadrans[1] += 1
        else:
            if r.y < quadran_height:
                quadrans[2] += 1
            else:
                quadrans[3] += 1

    return quadrans


def security_factor(robots_by_quadran: list[int]) -> int:
    return functools.reduce(lambda x, y: x * y, robots_by_quadran, 1)


def part1(filename: str, width: int, height: int) -> int:
    robots = read_data(filename)

    for r in robots:
        r.max_width = width
        r.max_height = height

    # for _ in range(100):
    #     for r in robots:
    #         r.move(width=width, height=height)

    for r in robots:
        r.jump_at_time(100)

    # print_grid(build_grid(robots, width, height))

    return security_factor(count_by_quadran(robots, width, height))


def part2(filename: str, width: int, height: int) -> int:
    initial_robots = read_data(filename)

    for r in initial_robots:
        r.max_width = width
        r.max_height = height

    time = 0
    occupied = set()

    max_time = 100000

    robots = initial_robots
    while time < max_time:
        occupied.clear()
        # robots = [
        #     Robot(r.x, r.y, r.vx, r.vy, r.max_width, r.max_height)
        #     for r in initial_robots
        # ]

        time += 1
        all_at_unique_place = True
        for r in robots:
            # r.jump_at_time(time)
            r.move()

            if (r.x, r.y) in occupied:
                # occupied.clear()
                all_at_unique_place = False
                # break
            else:
                occupied.add((r.x, r.y))

        if all_at_unique_place:
            return time

    return -1


def part2_minfactor(filename: str, width: int, height: int) -> int:
    robots = read_data(filename)
    for r in robots:
        r.max_width = width
        r.max_height = height

    min_factor = float("inf")
    min_time = 0

    time = 0
    max_time = 10000
    while time < max_time:
        time += 1
        for r in robots:
            r.move()
        factor = security_factor(count_by_quadran(robots, width, height))
        if factor < min_factor:
            min_factor = factor
            min_time = time
    return min_time


assert ic(part1("./sample.txt", 11, 7)) == 12
assert ic(part1("./input.txt", 101, 103)) == 221616000

assert ic(part2("./input.txt", 101, 103)) == 7572
assert ic(part2_minfactor("./input.txt", 101, 103)) == 7572

# z = part2('./input.txt', 101, 103)
# robots = read_data('./input.txt')
# for r in robots:
#     r.max_width = 101
#     r.max_height = 103
#     r.jump_at_time(z)
# print_grid(build_grid(robots, 101, 103))

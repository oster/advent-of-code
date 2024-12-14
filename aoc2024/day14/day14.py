from dataclasses import dataclass
from icecream import ic
import functools


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
            p, v = line.strip().split(" ")
            p = p.split("=")[1].split(",")
            v = v.split("=")[1].split(",")

            r = Robot(int(p[0]), int(p[1]), int(v[0]), int(v[1]))
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

    quadrans = {}
    quadran_width = width // 2
    quadran_height = height // 2

    for qy in range(0, 2):
        for qx in range(0, 2):

            start_x = qx * (quadran_width + 1)
            end_x = start_x + quadran_width

            start_y = qy * (quadran_height + 1)
            end_y = start_y + quadran_height

            q = 0
            for r in robots:
                if r.x >= start_x and r.x < end_x and r.y >= start_y and r.y < end_y:
                    q += 1
            quadrans[qx, qy] = q

    return functools.reduce(lambda x, y: x * y, quadrans.values(), 1)


# def robot_at(robots: list[Robot], x: int, y: int) -> bool:
#     for r in robots:
#         if r.x == x and r.y == y:
#             return True
#     return False


def part2(filename: str, width: int, height: int) -> int:
    initial_robots = read_data(filename)

    for r in initial_robots:
        r.max_width = width
        r.max_height = height

    time = 0
    occupied = set()

    max_time = 100000
    while time < max_time:
        robots = [
            Robot(r.x, r.y, r.vx, r.vy, r.max_width, r.max_height)
            for r in initial_robots
        ]

        time += 1
        all_at_unique_place = True
        for r in robots:
            r.jump_at_time(time)

            if (r.x, r.y) in occupied:
                occupied.clear()
                all_at_unique_place = False
                break
            else:
                occupied.add((r.x, r.y))

        if all_at_unique_place:
            return time

    return -1


assert ic(part1("./sample.txt", 11, 7)) == 12
assert ic(part1("./input.txt", 101, 103)) == 221616000

assert ic(part2("./input.txt", 101, 103)) == 7572

# z = part2('./input.txt', 101, 103)
# robots = read_data('./input.txt')
# for r in robots:
#     r.max_width = 101
#     r.max_height = 103
#     r.jump_at_time(z)
# print_grid(build_grid(robots, 101, 103))

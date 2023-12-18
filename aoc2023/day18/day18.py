import sys
from typing import Any

def die(msg: str):
    raise Exception(msg)


def print_grid(grid: list[list[Any]]):
    for line in grid:
        for val in line:
            print(f"{val:2}", end="")
        print()
    print()


def sign(x) -> int:
    if x >= 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def flood(grid: list[list[str]], x: int, y: int, size: int) -> int:
    filled = 0

    if y <= -size or y >= size or x <= -size or x >= size:
        die("Out of bounds.")

    if grid[y][x] == "x" or grid[y][x] == "#":
        return 0

    filled += 1
    grid[y][x] = "x"

    filled += flood(grid, x, y + 1, size)
    filled += flood(grid, x, y - 1, size)
    filled += flood(grid, x + 1, y, size)
    filled += flood(grid, x - 1, y, size)

    return filled


def read_input_part1(filename: str) -> list[tuple[str, int]]:
    data = []
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            elts = line.rstrip().split()

            direction = elts[0]
            length = int(elts[1])

            data.append((direction, length))
    return data


def part1_flood(filename: str, size) -> int:
    data = read_input_part1(filename)
    grid = [["." for _ in range(size)] for _ in range(size)]

    start_x, start_y = (size // 2, size // 2)
    for direction, length in data:
        old_x, old_y = (start_x, start_y)
        match direction:
            case "R":
                start_x += length
            case "L":
                start_x -= length
            case "U":
                start_y -= length
            case "D":
                start_y += length
            case _:
                die("Invalid direction.")

        sign_y = sign(start_y - old_y)
        for y in range(old_y, start_y + sign_y, sign_y):
            sign_x = sign(start_x - old_x)
            for x in range(old_x, start_x + sign_x, sign_x):
                grid[y][x] = "#"

    filled = 0
    filled = flood(grid, start_x + 1, start_y + 1, size)

    outline = sum(row.count("#") for row in grid)

    return filled + outline


sys.setrecursionlimit(100000)
assert part1_flood("./sample.txt", 22) == 62
assert part1_flood("./input.txt", 800) == 106459


def manhattan(a: tuple[int, int], b: tuple[int, int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)


def grouped(iterable, size):
    a = iter(iterable)
    return zip(*(a for _ in range(size)))


def window(iterable):
    return zip(iterable, iterable[1:])


def count_points_inside_polygon(outline_points: list[tuple[int, int]]) -> int:
    # shoelace algorithm to compute the area of a polygon
    n_points = len(outline_points)
    sum1 = 0
    sum2 = 0

    for i in range(n_points):
        x1, y1 = outline_points[i]
        x2, y2 = outline_points[(i + 1) % n_points]

        sum1 += x1 * y2
        sum2 += x2 * y1

    area = abs(sum1 - sum2) // 2

    # Pick's theorem to count the number of points inside a polygon
    # A = i + b/2 - 1
    # where:
    # - A is the area of the polygon,
    # - i is the number of interior points with integer coordinates,
    # - b is the number of boundary points with integer coordinates.
    #     (i.e. points on the outline)
    # So, i = A - b/2 + 1

    # we need a closed polygon, so we add the first point at the end
    b = 0
    for p1, p2 in window(outline_points + [outline_points[0]]):
        b += manhattan(p1, p2)

    i = area - b // 2 + 1 + b

    return i


def plot_points(points: list[tuple[int, int]], size: int):
    grid = [[0 for _ in range(size)] for _ in range(size)]

    start_x, start_y = (size // 2, size // 2)

    n = 0
    for x, y in points:
        n += 1
        grid[start_y + y][start_x + x] = n

    for line in grid:
        for val in line:
            if val > 0:
                print(f"{val:2}", end="")
            else:
                print(f" .", end="")
        print()
    print()


def solve(data: list[tuple[str, int]]) -> int:
    start = (0, 0)
    current_x, current_y = start

    outline_points = []
    outline_points.append(start)

    for direction, length in data:
        match direction:
            case "R":
                current_x += length
            case "L":
                current_x -= length
            case "U":
                current_y -= length
            case "D":
                current_y += length
            case _:
                die("Invalid direction.")
        if (current_x, current_y) != start:
            outline_points.append((current_x, current_y))

    return count_points_inside_polygon(outline_points)


def part1(filename: str) -> int:
    data = read_input_part1(filename)
    return solve(data)


assert part1("./sample.txt") == 62
assert part1("./input.txt") == 106459


def read_input_part2(filename: str) -> list[tuple[str, int]]:
    data = []
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            elts = line.rstrip().split()
            hex_value = elts[2][2:-2]
            length = int(hex_value, 16)
            direction_idx = int(elts[2][-2:-1])
            direction = ["R", "D", "L", "U"][direction_idx]
            data.append((direction, length))
    return data


def part2(filename: str) -> int:
    data = read_input_part2(filename)
    res = solve(data)
    return res


assert part2("./sample.txt") == 952408144115
assert part2("./input.txt") == 63806916814808

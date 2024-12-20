from typing import Generator
from icecream import ic
from collections import defaultdict

from typing import NewType

type Grid = dict[Pos, int]
type Pos = tuple[int, int]

# Pos = NewType("Pos", tuple[int, int])
# Grid = NewType("Grid", dict[Pos, str])


def read_data(filename: str) -> tuple[Grid, int, Pos, Pos]:
    grid = {}
    with open(filename, "r") as input_file:
        for y, line in enumerate(input_file.readlines()):
            for x, c in enumerate(line.strip()):
                if c == "#":
                    grid[x, y] = c
                elif c == "S":
                    start = (x, y)
                    pass
                elif c == "E":
                    end = (x, y)
                elif c == ".":
                    pass
                else:
                    raise ValueError(f"invalid character {c}")

    grid_size = max([x for x, _ in grid.keys()])

    return grid, grid_size, start, end


def print_grid(grid: Grid, start: Pos, end: Pos) -> None:
    min_x = min([x for x, _ in grid.keys()])
    max_x = max([x for x, _ in grid.keys()])
    min_y = min([y for _, y in grid.keys()])
    max_y = max([y for _, y in grid.keys()])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if start == (x, y):
                print("S", end="")
            elif end == (x, y):
                print("E", end="")
            else:
                print(grid.get((x, y), "."), end="")
        print()

def print_path(grid: Grid, path: list[Pos]) -> None:
    min_x = min([x for x, _ in grid.keys()])
    max_x = max([x for x, _ in grid.keys()])
    min_y = min([y for _, y in grid.keys()])
    max_y = max([y for _, y in grid.keys()])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in path:
                print("o", end="")
            else:
                print(grid.get((x, y), "."), end="")
        print()


def next_neighbor(pos: Pos, grid: Grid, grid_size: int) -> Generator[Pos, None, None]:
    x, y = pos
    return (pos for pos in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)] if pos[0] >= 0 and pos[0] < grid_size and pos[1] >= 0 and pos[1] < grid_size and grid.get(pos, None) != "#")


def compute_distances(start: Pos, end: Pos, grid: Grid, grid_size: int) -> tuple[set[Pos], dict[Pos, int]]:
    distances = {} # Pos -> distance from start
    current = start
    dist = 0
    visited = set()
    visited.add(start)
    distances[start] = 0
    while current != end:
        for next_pos in next_neighbor(current, grid, grid_size):
            if next_pos in visited:
                continue
            visited.add(next_pos)
            dist += 1
            distances[next_pos] = dist
            current = next_pos

    return visited, distances


def part1(filename: str, min_gain: int = 0) -> int:
    grid, grid_size, start, end = read_data(filename)
    visited, distances = compute_distances(start, end, grid, grid_size)
    path = sorted(visited, key=lambda pos: distances[pos]) 
    count = 0
    # gains = defaultdict(set)

    for src_idx, src in enumerate(path):
        src_x, src_y = src
        for dst in path[src_idx+1:]:
            dst_x, dst_y = dst
            
            dx = abs((dst_x - src_x))
            dy = abs(dst_y - src_y)

            if (dx == 2 and dy == 0) or (dx == 0 and dy == 2):
                gain = distances[dst] - distances[src] - 2
                if gain >= min_gain:
                    # gains[gain].add((src, dst))
                    count += 1
    return count


def manhattan(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def part2(filename: str, min_gain: int = 0) -> int:
    grid, grid_size, start, end = read_data(filename)
    visited, distances = compute_distances(start, end, grid, grid_size)


    path = sorted(visited, key=lambda pos: distances[pos]) 
    count = 0
    # gains = defaultdict(set)

    for src_idx, src in enumerate(path):
        src_x, src_y = src
        for dst in path[src_idx+1:]:
            dst_x, dst_y = dst
            
            if manhattan(src, dst) <= 20:
                gain = distances[dst] - distances[src] - manhattan(src, dst)
                if gain >= min_gain:
                    # gains[gain].add((src, dst))
                    count += 1

    return count



# grid, grid_size, start, end = read_data('sample.txt')
# path, distances = compute_distances(start, end, grid, grid_size)
# ic(max(distances.values()))
# assert max(distances.values()) == 84


# grid, grid_size, start, end = read_data('input.txt')
# path, distances = compute_distances(start, end, grid, grid_size)
# ic(max(distances.values()))
# assert max(distances.values()) == 9452


assert ic(part1('sample.txt', 1)) == 44
assert ic(part1('input.txt', 100)) == 1438

assert ic(part2('./sample.txt', 50)) == 285
assert ic(part2('./input.txt', 100)) == 1026446

from typing import Generator
from icecream import ic


type Grid = dict[Pos, int]
type Pos = tuple[int, int]

# from typing import NewType

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
    return (
        pos
        for pos in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        if pos[0] >= 0
        and pos[0] < grid_size
        and pos[1] >= 0
        and pos[1] < grid_size
        and grid.get(pos, None) != "#"
    )


def compute_distances(
    start: Pos, end: Pos, grid: Grid, grid_size: int
) -> tuple[set[Pos], dict[Pos, int]]:
    distances = {}  # Pos -> distance from start
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


def manhattan(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def manhattan_valid_neighbors(
    pos: Pos, path: list[Pos], distances: dict[Pos, int], distance: int
) -> set[Pos]:
    px, py = pos
    neighbors = set()
    for deltaX in range(distance + 1):
        for deltaY in range(distance - deltaX + 1):
            if deltaX == 0 and deltaY == 0:
                continue

            if 2 <= abs(deltaX) + abs(deltaY) <= distance:
                for nn in [
                    (px + deltaX, py + deltaY),
                    (px - deltaX, py + deltaY),
                    (px + deltaX, py - deltaY),
                    (px - deltaX, py - deltaY),
                ]:
                    if nn in path and distances[nn] > distances[pos]:
                        neighbors.add(nn)

    return neighbors


def solve(
    start: Pos,
    end: Pos,
    cheat_distance: int,
    min_gain_to_cheat: int,
    grid: Grid,
    grid_size: int,
) -> int:
    visited, distances = compute_distances(start, end, grid, grid_size)
    path = sorted(visited, key=lambda pos: distances[pos])
    count = 0

    for src_idx, src in enumerate(path):
        # for dst in manhattan_valid_neighbors(src, path, distances, cheat_distance):
        for dst in path[src_idx + 1 :]:
            if manhattan(src, dst) <= cheat_distance:
                gain = distances[dst] - distances[src] - manhattan(src, dst)
                if gain >= min_gain_to_cheat:
                    count += 1

    return count


def part1(filename: str, min_gain: int = 0) -> int:
    grid, grid_size, start, end = read_data(filename)
    return solve(start, end, 2, min_gain, grid, grid_size)


def part2(filename: str, min_gain: int = 0) -> int:
    grid, grid_size, start, end = read_data(filename)
    return solve(start, end, 20, min_gain, grid, grid_size)


# grid, grid_size, start, end = read_data('sample.txt')
# path, distances = compute_distances(start, end, grid, grid_size)
# ic(max(distances.values()))
# assert max(distances.values()) == 84


# grid, grid_size, start, end = read_data('input.txt')
# path, distances = compute_distances(start, end, grid, grid_size)
# ic(max(distances.values()))
# assert max(distances.values()) == 9452


assert ic(part1("sample.txt", 1)) == 44
assert ic(part1("input.txt", 100)) == 1438

assert ic(part2("./sample.txt", 50)) == 285
assert ic(part2("./input.txt", 100)) == 1026446

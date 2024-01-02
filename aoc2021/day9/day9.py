from typing import Iterable


type Pos = tuple[int, int]
type Grid = list[list[int]]


def dump_grid(card: Grid) -> None:
    for row in card:
        for col in row:
            print(f"{col:2d}", end=" ")
        print()
    print()


def read_data(filename: str) -> Grid:
    lines = []
    with open(filename, "r") as data_file:
        for line in data_file:
            lines.append(list(map(int, list(line.rstrip()))))

    return lines


def neighbors(pos: Pos, height: int, width: int) -> Iterable[Pos]:
    x, y = pos
    return filter(
        lambda pos: pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height,
        ((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)),
    )


def find_lowest_positions(grid: Grid) -> list[Pos]:
    height = len(grid)
    width = len(grid[0])
    lowest = []

    for y in range(height):
        for x in range(width):
            elevation = grid[y][x]
            elevations = [grid[y][x] for x, y in neighbors((x, y), height, width)]
            if all(elevation < e for e in elevations):
                lowest.append((x, y))

    return lowest


def part1(filename: str) -> int:
    grid = read_data(filename)
    risk = sum([grid[y][x] + 1 for x, y in find_lowest_positions(grid)])
    return risk


assert part1("sample.txt") == 15
assert part1("input.txt") == 562


def find_basin_dfs(grid: Grid, lowest_position: Pos) -> int:
    height = len(grid)
    width = len(grid[0])

    basin = []

    visited = set()
    queue = [lowest_position]
    while queue:
        pos = queue.pop(0)
        if pos in visited:
            continue
        visited.add(pos)

        basin.append(pos)

        for neighbor in neighbors(pos, height, width):
            n_x, n_y = neighbor
            if grid[n_y][n_x] < 9:
                queue.append(neighbor)

    return len(basin)


def part2(filename: str) -> int:
    grid = read_data(filename)
    lowest_positions = find_lowest_positions(grid)

    all_basin_sizes = [
        find_basin_dfs(grid, lowest_position) for lowest_position in lowest_positions
    ]
    all_basin_sizes = sorted(all_basin_sizes, reverse=True)

    return all_basin_sizes[0] * all_basin_sizes[1] * all_basin_sizes[2]


assert part2("sample.txt") == 1134
assert part2("input.txt") == 1076922

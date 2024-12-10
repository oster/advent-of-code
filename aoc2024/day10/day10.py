from typing import Generator
from icecream import ic


type Grid = dict[Pos, str]
type Pos = tuple[int, int]

# from typing import NewType
# Pos = NewType('Pos', tuple[int, int])
# Grid = NewType('Grid', dict[Pos, str])


def read_input(filename: str) -> tuple[Grid, int, list[Pos]]:
    grid = {}
    grid_size: int = 0

    starts = []

    with open(filename, "r") as input_file:
        for y, line in enumerate(input_file.readlines()):
            grid_size += 1
            for x, c in enumerate(line.strip()):
                height = int(c) if c.isdigit() else -1
                grid[x, y] = height
                if height == 0:
                    starts.append((x, y))


    return grid, grid_size, starts


def in_grid(pos: Pos, size: int) -> bool:
    x, y = pos
    return x >= 0 and x < size and y >= 0 and y < size


def four_neighbours(pos: Pos) -> Generator[Pos, None, None]:
    x, y = pos
    yield (x + 1, y)
    yield (x, y + 1)
    yield (x - 1, y)
    yield (x, y - 1)


def next_steps(pos: Pos, current_height, grid: Grid, grid_size: int) -> Generator[Pos, None, None]:
    return ( (x, y) for (x,y) in four_neighbours(pos) if in_grid((x,y), grid_size) and  grid[x, y] == current_height + 1)


def get_walk_path(current: Pos, grid: Grid, size: int, visited: set[Pos], visited_trailhead) -> dict[Pos, int]:
    if grid[current] == 9:
        visited_trailhead[current] = visited_trailhead.get(current, 0) + 1
        return visited_trailhead

    current_height = grid[current]
    for next_position in next_steps(current, current_height, grid, size):
        if next_position not in visited:
            visited_trailhead |= get_walk_path(next_position, grid, size, visited | { next_position }, visited_trailhead)

    return visited_trailhead


def part1(filename: str) -> int:
    grid, grid_size, starts = read_input(filename)
    return sum(len(get_walk_path(start, grid, grid_size, set(), dict())) for start in starts)


def part2(filename: str) -> int:
    grid, grid_size, starts = read_input(filename)
    
    s = 0
    for start in starts:
        v = get_walk_path(start, grid, grid_size, set(), dict())
        s += sum(v.values())
    return s


# ic.disable()

# assert ic(part1('./sample1.txt')) == 1
# assert ic(part1('./sample2.txt')) == 2
# assert ic(part1('./sample3.txt')) == 4
# assert ic(part1('./sample4.txt')) == 3
# assert ic(part1('./sample25.txt')) == 1

assert ic(part1('./sample.txt')) == 36
assert ic(part1('./input.txt')) == 638

# assert ic(part2('./sample2-1.txt')) == 3
assert ic(part2('./sample.txt')) == 81
assert ic(part2('./input.txt')) == 1289


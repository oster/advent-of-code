from enum import IntEnum
from icecream import ic


def die(msg: str):
    raise Exception(msg)


class Direction(IntEnum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3
    EXIT = 666


type Grid = dict[Pos, str]
type Pos = tuple[int, int]


def one_step(pos: Pos, dir: Direction) -> Pos:
    x, y = pos
    match dir:
        case Direction.EAST:
            return (x + 1, y)
        case Direction.SOUTH:
            return (x, y + 1)
        case Direction.WEST:
            return (x - 1, y)
        case Direction.NORTH:
            return (x, y - 1)
    return (x, y)


SYMBOL_TO_DIRECTION = {
    '>': Direction.EAST,
    'v': Direction.SOUTH,
    '<': Direction.WEST,
    '^': Direction.NORTH
}

def read_input(filename: str) -> tuple[Grid, int, Pos, Direction]:
    grid = {}
    grid_size: int = 0
    with open(filename, "r") as input_file:
        for y, line in enumerate(input_file.readlines()):
            grid_size += 1
            for x, c in enumerate(line.strip()):
                if c == '#':
                    grid[x, y] = c
                elif c in SYMBOL_TO_DIRECTION:
                    guard_pos = x, y
                    guard_dir = SYMBOL_TO_DIRECTION[c]

    return grid, grid_size, guard_pos, guard_dir


def print_grid(grid: Grid, grid_size: int):
    for y in range(grid_size):
        for x in range(grid_size):
            print(f"{grid.get((x, y), ' '):2}", end="")
        print()
    print()


def next_pos(pos: Pos, dir: Direction, grid: Grid, size: int) -> tuple[Pos, Direction]:
    new_pos = one_step(pos, dir)
    match grid.get(new_pos):
        case '#':
            match dir:
                case Direction.EAST:
                    return pos, Direction.SOUTH
                case Direction.SOUTH:
                    return pos, Direction.WEST
                case Direction.WEST:
                    return pos, Direction.NORTH
                case Direction.NORTH:
                    return pos, Direction.EAST

    return new_pos, dir


def in_grid(pos: Pos, size: int) -> bool:
    x, y = pos
    return x >= 0 and x < size and y >= 0 and y < size


def get_walk_path(guard_pos: Pos, guard_dir: Direction, grid: Grid, size: int) -> set[Pos]:
    walk_positions = set()
    while in_grid(guard_pos, size):
        guard_pos, guard_dir = next_pos(guard_pos, guard_dir, grid, size)
        walk_positions.add(guard_pos)

    # remove latest position since it is out of the grid
    walk_positions.remove(guard_pos)

    return walk_positions


def part1(filename: str) -> int:
    grid, size, guard_pos, guard_dir = read_input(filename)

    walk_positions = get_walk_path(guard_pos, guard_dir, grid, size)
    return len(walk_positions)


def got_cycle(guard_pos, guard_dir, grid, size) -> bool:
    dicting_pos = set()
    while in_grid(guard_pos, size):
        guard_pos, guard_dir = next_pos(guard_pos, guard_dir, grid, size)
        if (guard_pos, guard_dir) in dicting_pos:
            return True
        dicting_pos.add((guard_pos, guard_dir))
    return False


def part2_brute(filename: str) -> int:
    grid, size, guard_pos, guard_dir = read_input(filename)

    cycle_count = 0
    for ox in range(size):
        for oy in range(size):
            if (ox, oy) != guard_pos and grid.get((ox, oy)) is None:
                grid[ox, oy] = '#'
                if got_cycle(guard_pos, guard_dir, grid, size):
                    cycle_count += 1
                del grid[ox, oy]
    return cycle_count


def it_may_create_a_cycle(ox, oy, guard_pos, guard_dir, grid, size, obstacles_by_x, obstacles_by_y) -> bool:
    return obstacles_by_x.get(ox - 1) or obstacles_by_x.get(ox + 1) or obstacles_by_y.get(oy - 1) or obstacles_by_y.get(oy + 1)


def part2(filename: str) -> int:
    grid, size, guard_pos, guard_dir = read_input(filename)

    # obstacles_by_x = { x : True for  x,_ in grid.keys() }
    # obstacles_by_y = { y : True for  y,_ in grid.keys() }

    cycle_count = 0
    for pos in get_walk_path(guard_pos, guard_dir, grid, size):
        if pos != guard_pos and grid.get(pos) is None:
            # if it_may_create_a_cycle(*pos, guard_pos, guard_dir, grid, size, obstacles_by_x, obstacles_by_y):
            grid[pos] = '#'
            if got_cycle(guard_pos, guard_dir, grid, size):
                cycle_count += 1
            del grid[pos]
    return cycle_count



assert ic(part1('./sample.txt')) == 41
assert ic(part1('./input.txt')) == 4883

assert ic(part2('./sample.txt')) == 6
assert ic(part2('./input.txt')) == 1655

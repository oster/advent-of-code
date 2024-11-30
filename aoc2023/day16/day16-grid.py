from collections import deque
from enum import IntEnum
import sys
from typing import Generator

sys.setrecursionlimit(5000)

class Direction(IntEnum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


type Pos = tuple[int, int]
type Grid = dict[Pos, str]


def read_input(filename: str) -> tuple[Grid, int]:
    grid = {}
    grid_size = 0
    with open(filename, "r") as input_file:
        for y, line in enumerate(input_file.readlines()):
            grid_size += 1
            for x, c in enumerate(line.strip()):
                grid[x, y] = c
    return grid, grid_size


def die(msg: str):
    raise Exception(msg)


def print_grid(grid: Grid, grid_size: int):
    for y in range(grid_size):
        for x in range(grid_size):
            print(f"{grid.get((x, y), ' '):2}", end="")
        print()
    print()


def debug_decorator(f):
    def wrapper(*args, **kwargs):
        print(f"f{args}, {kwargs}")
        res = f(*args, **kwargs)
        print(f"  return {res}")
        return res

    return wrapper


# @debug_decorator
def move(current: Pos, heading: Direction) -> tuple[Pos, Direction]:
    x, y = current

    match heading:
        case Direction.EAST:
            return (x + 1, y), heading
        case Direction.SOUTH:
            return (x, y + 1), heading
        case Direction.WEST:
            return (x - 1, y), heading
        case Direction.NORTH:
            return (x, y - 1), heading
        case _:
            die("Invalid heading.")


# def move(current : Pos, heading : Direction) -> tuple[Pos, Direction] :
#     x, y = current
#     dx, dy = {
#         Direction.EAST: (1, 0),
#         Direction.SOUTH: (0, 1),
#         Direction.WEST: (-1, 0),
#         Direction.NORTH: (0, -1),
#     }[heading]
#     return (x + dx, y + dy), heading


MIRROR_MAP = {
    ("/", Direction.EAST): Direction.NORTH,
    ("/", Direction.SOUTH): Direction.WEST,
    ("/", Direction.WEST): Direction.SOUTH,
    ("/", Direction.NORTH): Direction.EAST,
    ("\\", Direction.EAST): Direction.SOUTH,
    ("\\", Direction.SOUTH): Direction.EAST,
    ("\\", Direction.WEST): Direction.NORTH,
    ("\\", Direction.NORTH): Direction.WEST,
}


def horizontal(heading: Direction) -> bool:
    return heading == Direction.EAST or heading == Direction.WEST

def vertical(heading: Direction) -> bool:
    return heading == Direction.NORTH or heading == Direction.SOUTH


def yield_next_positions(
    current: Pos, heading: Direction, grid: Grid
) -> Generator[tuple[Pos, Direction], None, None]:
    at_current_pos = grid[current]

    match at_current_pos:
        case ".":
            yield move(current, heading)
        case "|":
            if horizontal(heading):
                for next_heading in [Direction.NORTH, Direction.SOUTH]:
                    yield move(current, next_heading)
            else:
                yield move(current, heading)
        case "-":
            if vertical(heading):
                for next_heading in [Direction.EAST, Direction.WEST]:
                    yield move(current, next_heading)
            else:
                yield move(current, heading)
        case "\\" | "/":
            yield move(current, MIRROR_MAP[(at_current_pos, heading)])
        case _:
            die(f"Invalid character in grid: '{current}'.")


def compute_energized_cells(rays: dict[Pos, bool]) -> int:
    visited_positions = {pos for pos, _ in rays.keys()}
    return len(visited_positions)


def compute_part1_bfs(grid: Grid, start: Pos, heading: Direction) -> int:
    rays = {}
    states = deque()
    states.append((start, heading))
    while states:
        current, heading = states.popleft()
        rays[(current, heading)] = True
        for next_pos, next_heading in yield_next_positions(current, heading, grid):
            if next_pos in grid and (next_pos, next_heading) not in rays:
                states.append((next_pos, next_heading))
    return compute_energized_cells(rays)


def dfs_walk(
    grid: Grid,
    current: Pos,
    heading: Direction,
    rays: dict[tuple[Pos, Direction], bool],
) -> None:
    rays[(current, heading)] = True
    for next_pos, next_heading in yield_next_positions(current, heading, grid):
        if next_pos in grid and (next_pos, next_heading) not in rays:
            dfs_walk(grid, next_pos, next_heading, rays)


def compute_part1_rec(grid: Grid, start: Pos, heading: Direction) -> int:
    rays = {}
    dfs_walk(grid, start, heading, rays)
    return compute_energized_cells(rays)


def compute_part1(grid: Grid, start: Pos, heading: Direction) -> int:
    return compute_part1_bfs(grid, start, heading)


def part1(filename: str) -> int:
    grid, _ = read_input(filename)
    return compute_part1(grid, (0, 0), Direction.EAST)


def part2(filename: str) -> int:
    grid, grid_size = read_input(filename)
    max_energies = 0

    for k in range(0, grid_size):
        energies = compute_part1(grid, (k, 0), Direction.SOUTH)
        if energies > max_energies:
            max_energies = energies

        energies = compute_part1(grid, (k, grid_size - 1), Direction.NORTH)
        if energies > max_energies:
            max_energies = energies

        energies = compute_part1(grid, (0, k), Direction.EAST)
        if energies > max_energies:
            max_energies = energies

        energies = compute_part1(grid, (grid_size - 1, k), Direction.WEST)
        if energies > max_energies:
            max_energies = energies

    return max_energies


def check(expected, actual):
    assert expected == actual, f"Expected {expected}, but got {actual}."
    print(f"Passed: {expected}")


if __name__ == "__main__":
    check(46, part1("./sample.txt"))
    check(7632, part1("./input.txt"))
    check(51, part2("./sample.txt"))
    check(8023, part2("./input.txt"))

    # from cProfile import Profile
    # from pstats import SortKey, Stats

    # with Profile() as profile:
    #     check(8023, part2("./input.txt"))
    #     Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats()
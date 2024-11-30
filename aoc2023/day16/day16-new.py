from collections import deque
from typing import Any
from enum import IntEnum
import sys
from typing import Generator
sys.setrecursionlimit(5000)


class Direction(IntEnum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


def read_input(filename: str) -> list[list[str]]:
    data = []
    with open(filename, "r") as input_file:
        data = map(list, map(str.rstrip, input_file.readlines()))
    return list(data)


def die(msg: str):
    raise Exception(msg)


def print_grid(grid: list[list[Any]]):
    for line in grid:
        for val in line:
            print(f"{val:2}", end="")
        print()
    print()


def debug_decorator(f):
    def wrapper(*args, **kwargs):
        print(f'f{args}, {kwargs}')
        res = f(*args, **kwargs)
        print(f'  return {res}')
        return res
    return wrapper


type Pos = tuple[int, int, Direction]


# @debug_decorator
def move(current : Pos, heading : Direction) -> Pos :
    x, y, _ = current

    match heading:
        case Direction.EAST:
            return (x+1, y, heading)
        case Direction.SOUTH:
            return (x, y+1, heading)
        case Direction.WEST:
            return (x-1, y, heading)
        case Direction.NORTH:
            return (x, y-1, heading)
        case _:
            die("Invalid heading.")     


# def move(current : Pos, heading : Direction) -> Pos :
#     x, y, _ = current
#
#     dx, dy = {
#         Direction.EAST: (1, 0),
#         Direction.SOUTH: (0, 1),
#         Direction.WEST: (-1, 0),
#         Direction.NORTH: (0, -1),
#     }[heading]
#
#     return (x + dx, y + dy, heading)


MIRROR_MAP = {
    ('/', Direction.EAST): Direction.NORTH,
    ('/', Direction.SOUTH): Direction.WEST,
    ('/', Direction.WEST): Direction.SOUTH,
    ('/', Direction.NORTH): Direction.EAST,
    ('\\', Direction.EAST): Direction.SOUTH,
    ('\\', Direction.SOUTH): Direction.EAST,
    ('\\', Direction.WEST): Direction.NORTH,
    ('\\', Direction.NORTH): Direction.WEST,
}


def next_positions(current : Pos, grid : list[list[str]]) -> list[Pos]:
    x, y, heading = current
    at_current_pos = grid[y][x]

    match at_current_pos:
        case '.':
            return [ move(current, heading) ]
        case '|':
            if heading in [ Direction.EAST, Direction.WEST ]:
                return [ (x , y-1, Direction.NORTH), (x, y+1, Direction.SOUTH) ]
            else:
                return [ move(current, heading) ]
        case '-':
            if heading in [ Direction.NORTH, Direction.SOUTH ]:
                return [ (x-1 , y, Direction.WEST), (x+1, y, Direction.EAST) ]
            else:
                return [ move(current, heading) ]
        case '\\' | '/':
            return [ move(current, MIRROR_MAP[(at_current_pos, heading)]) ]

        case _:
            return []
            # die(f"Invalid character in grid: '{current}'.")


def yield_next_positions(current : Pos, grid : list[list[str]]) -> Generator[Pos]:
    x, y, heading = current
    at_current_pos = grid[y][x]

    match at_current_pos:
        case '.':
            yield move(current, heading)
        case '|':
            if heading in [ Direction.EAST, Direction.WEST ]:
                for next_heading in [ Direction.NORTH, Direction.SOUTH ]:
                    yield move(current, next_heading)
            else:
                yield move(current, heading)
        case '-':
            if heading in [ Direction.NORTH, Direction.SOUTH ]:
                for next_heading in [ Direction.EAST, Direction.WEST ]:
                    yield move(current, next_heading)
            else:
                yield move(current, heading)
        case '\\' | '/':
            yield move(current, MIRROR_MAP[(at_current_pos, heading)])
        case _:
            die(f"Invalid character in grid: '{current}'.")


def compute_energized_cells(rays : dict[Pos, bool]) -> int:
    visited_positions = { (x,y) for (x,y,_) in rays.keys() }
    return len(visited_positions)


def is_position_valid(pos : Pos, grid_size : int) -> bool:
    return  0 <= pos[0] < grid_size and 0 <= pos[1] < grid_size


def compute_part1(grid : list[list[str]], start : Pos) -> int:
    grid_size = len(grid)

    rays = {}
    states = deque()
    states.append(start)
    while states:
        current = states.popleft()
        rays[current] = True
        for next_pos in yield_next_positions(current, grid):
            if is_position_valid(next_pos, grid_size) and next_pos not in rays:
                states.append(next_pos)
    return compute_energized_cells(rays)


def dfs_walk(grid : list[list[str]], current : Pos, rays : dict[Pos,bool]) -> None:
    grid_size = len(grid)

    rays[current] = True
    for next_pos in yield_next_positions(current, grid):
        if is_position_valid(next_pos, grid_size) and next_pos not in rays:
            dfs_walk(grid, next_pos, rays)    


def compute_part1_rec(grid : list[list[str]], start : Pos) -> int:
    rays = {}
    dfs_walk(grid, start, rays)
    return compute_energized_cells(rays)


def part1(filename: str) -> int:
    grid = read_input(filename)
    return compute_part1(grid, (0, 0, Direction.EAST))


def part2(filename: str) -> int:
    grid = read_input(filename)
    grid_size = len(grid)

    max_energies = 0

    for k in range(0, grid_size):
        energies = compute_part1(grid, (k, 0, Direction.SOUTH))
        if energies > max_energies:
            max_energies = energies

        energies = compute_part1(grid, (k, grid_size-1, Direction.NORTH))
        if energies > max_energies:
            max_energies = energies

        energies = compute_part1(grid, (0, k, Direction.EAST))
        if energies > max_energies:
            max_energies = energies

        energies = compute_part1(grid, (grid_size-1, k, Direction.WEST))
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


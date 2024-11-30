from collections import deque
from typing import Any
from enum import Enum
import sys
sys.setrecursionlimit(5000)


class Direction(Enum):
    EAST=0
    SOUTH=1
    WEST=2
    NORTH=3


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
        print(f'return {res}')
        return res
    return wrapper


# @debug_decorator
def move(current : tuple[int, int, Direction] ) -> tuple[int, int, Direction] :
    x, y, heading = current

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


def next_positions(current : tuple[int, int, Direction], grid : list[list[str]]) -> list[tuple[int, int, Direction]]:
    x, y, heading = current

    at_current_pos = grid[y][x]

    match at_current_pos:
        case '.':
            return [ move(current) ]
        case '|':
            if heading in [ Direction.EAST, Direction.WEST ]:
                return [ (x , y-1, Direction.NORTH), (x, y+1, Direction.SOUTH) ]
            else:
                return [ move(current) ]
        case '-':
            if heading in [ Direction.NORTH, Direction.SOUTH ]:
                return [ (x-1 , y, Direction.WEST), (x+1, y, Direction.EAST) ]
            else:
                return [ move(current) ]
        case '\\':
            if heading == Direction.EAST:
                return [ (x, y+1, Direction.SOUTH) ]
            elif heading == Direction.SOUTH:
                return [ (x+1, y, Direction.EAST) ]
            elif heading == Direction.WEST:
                return [ (x, y-1, Direction.NORTH) ]
            elif heading == Direction.NORTH:
                return [ (x-1, y, Direction.WEST) ]
            else:
                die("Invalid heading.")
        case '/':
            if heading == Direction.EAST:
                return [ (x, y-1, Direction.NORTH) ]
            elif heading == Direction.SOUTH:
                return [ (x-1, y, Direction.WEST) ]
            elif heading == Direction.WEST:
                return [ (x, y+1, Direction.SOUTH) ]
            elif heading == Direction.NORTH:
                return [ (x+1, y, Direction.EAST) ]
            else:
                die("Invalid heading.")
        case _:
            die(f"Invalid character in grid: '{current}'.")


def compute_energy(rays) -> int:
    visited_positions = { (x,y) for (x,y,_) in rays.keys() }
    return len(visited_positions)


def compute_part1(grid : list[list[str]], start = (0,0,Direction.EAST)) -> int:
    size = len(grid)

    rays = {}
    states = deque()
    states.append(start)

    while states:
        current = states.popleft()
        rays[current] = True
        for next_pos in next_positions(current, grid):
            if next_pos[0] >= 0 and next_pos[0] < size and next_pos[1] >= 0 and next_pos[1] < size:
                if next_pos not in rays:
                    states.append(next_pos)
    return compute_energy(rays)


def walk(grid : list[list[str]], current, rays) -> None:
    size = len(grid)

    rays[current] = True
    for next_pos in next_positions(current, grid):
        if next_pos[0] >= 0 and next_pos[0] < size and next_pos[1] >= 0 and next_pos[1] < size:
            if next_pos not in rays:
                walk(grid, next_pos, rays)    


def compute_part1_rec(grid : list[list[str]], start = (0,0,Direction.EAST)) -> int:
    rays = {}
    walk(grid, start, rays)
    return compute_energy(rays)


def part1(filename: str) -> int:
    grid = read_input(filename)
    return compute_part1_rec(grid, (0, 0, Direction.EAST))


def part2(filename: str) -> int:
    grid = read_input(filename)
    size = len(grid)

    max_energies = 0

    for k in range(0, size):
        energies = compute_part1_rec(grid, (k, 0, Direction.SOUTH))
        if energies > max_energies:
            max_energies = energies

        energies = compute_part1_rec(grid, (k, size-1, Direction.NORTH))
        if energies > max_energies:
            max_energies = energies

        energies = compute_part1_rec(grid, (0, k, Direction.EAST))
        if energies > max_energies:
            max_energies = energies

        energies = compute_part1_rec(grid, (size-1, k, Direction.WEST))
        if energies > max_energies:
            max_energies = energies

    return max_energies

assert part1("./sample.txt") == 46
assert part1("./input.txt") == 7632

assert part2("./sample.txt") == 51
assert part2("./input.txt") == 8023




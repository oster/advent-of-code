from collections import deque
from typing import Any
from enum import Enum

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


heading_char = [ '>', 'v', '<','^' ]


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


def rotate_right(heading : Direction) -> Direction:
    rotated = Direction((heading.value + 1) % 4)
    return rotated 

assert rotate_right(Direction.EAST) == Direction.SOUTH
assert rotate_right(Direction.SOUTH) == Direction.WEST
assert rotate_right(Direction.WEST) == Direction.NORTH
assert rotate_right(Direction.NORTH) == Direction.EAST

def rotate_left(heading : Direction) -> Direction:
    rotated = Direction((heading.value - 1) % 4)
    return rotated 

assert rotate_left(Direction.EAST) == Direction.NORTH
assert rotate_left(Direction.SOUTH) == Direction.EAST
assert rotate_left(Direction.WEST) == Direction.SOUTH
assert rotate_left(Direction.NORTH) == Direction.WEST


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

                # if heading == Direction.NORTH:
                #     return [ (x, y-1, heading) ]
                # else: # heading == SOUTH:
                #     return [ (x, y+1, heading) ]
        case '-':
            if heading in [ Direction.NORTH, Direction.SOUTH ]:
                return [ (x-1 , y, Direction.WEST), (x+1, y, Direction.EAST) ]
            else:
                return [ move(current) ]
                # if heading == Direction.EAST:
                #     return [ (x+1, y, heading) ]
                # else: # heading == WEST:
                #     return [ (x-1, y, heading) ]
        case '\\':
            # heading = rotate_left(heading)
            # return [ move(current) ]

            # if heading in [ Direction.NORTH, Direction.SOUTH]:
            #     heading = rotate_left(heading)
            # else:
            #     heading = rotate_right(heading)
            # return [ move(current) ]

            # x, y, heading = move(current)
            # if heading in [ Direction.NORTH, Direction.SOUTH]:
            #     heading = rotate_left(heading)
            # else:
            #     heading = rotate_right(heading)
            # return [ (x, y, heading) ]

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

def mark_pos(pos : tuple[int, int, Direction], energized_grid : list[list[str]]):
    x, y, heading = pos

    current_mark = energized_grid[y][x]
    if current_mark != '.':
        energized_grid[y][x] = '2'
    else:
        energized_grid[y][x] = heading_char[heading.value]


def count_energy(energized_grid : list[list[str]]) -> int:
    sum = 0
    for line in energized_grid:
        for val in line:
            if val != '.':
                sum += 1
    return sum

def compute_part1(grid : list[list[str]], start = (0,0,Direction.EAST)) -> int:
    size = len(grid)

    energized_grid = [ list('.' * size ) for _ in range(size) ]

    states = deque()
    rays = {}
    count = 0
    states.append(start)

    while states:
        current = states.popleft()
        # print(current)

        if current in rays:
            continue
        else:
            count +=1
            rays[current] = count

            mark_pos(current, energized_grid)
            # print_grid(energized_grid)
            # input()

            for next_pos in next_positions(current, grid):
                # print(f'next_pos:', next_pos)

                if next_pos[0] >= 0 and next_pos[0] < size and next_pos[1] >= 0 and next_pos[1] < size:
                    # stay in grid
                    states.append(next_pos)

    energies = count_energy(energized_grid)
    return energies

def part1(filename: str) -> int:
    grid = read_input(filename)
    return compute_part1(grid, (0,0,Direction.EAST))

def part2(filename: str) -> int:
    grid = read_input(filename)
    size = len(grid)

    max_energies = 0


    for x in range(0, size):
        energies = compute_part1(grid, (x, 0, Direction.SOUTH))
        if energies > max_energies:
            max_energies = energies

    for x in range(0, size):
        energies = compute_part1(grid, (x, size-1, Direction.NORTH))
        if energies > max_energies:
            max_energies = energies

    for y in range(0, size):
        energies = compute_part1(grid, (0, y, Direction.EAST))
        if energies > max_energies:
            max_energies = energies

    for y in range(0, size):
        energies = compute_part1(grid, (size-1, y, Direction.WEST))
        if energies > max_energies:
            max_energies = energies

    return max_energies

assert part1("./sample.txt") == 46
assert part1("./input.txt") == 7632

assert part2("./sample.txt") == 51
assert part2("./input.txt") == 8023




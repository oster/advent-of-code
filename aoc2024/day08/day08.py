from itertools import combinations
from icecream import ic
import string

type Pos = tuple[int, int]
type Grid = dict[Pos, str]

# from typing import NewType
# Pos = NewType('Pos', tuple[int, int])
# Grid = NewType('Grid', dict[Pos, str])

def read_input(filename: str) -> tuple[Grid, int, dict[str, list[Pos]]]:
    grid = {}
    grid_size: int = 0

    antennas = {}

    with open(filename, "r") as input_file:
        for y, line in enumerate(input_file.readlines()):
            grid_size += 1
            for x, c in enumerate(line.strip()):
                if c in string.ascii_letters + string.digits:
                    grid[x, y] = c
                    if c not in antennas:
                        antennas[c] = []
                    antennas[c].append((x, y))

    return grid, grid_size, antennas


def in_bounds(grid: Grid, pos: Pos, size: int) -> bool:
    return 0 <= pos[0] < size and 0 <= pos[1] < size


def print_antinodes(grid: Grid, grid_size: int, antinodes: set[Pos], display_antennas: bool = False):
    for y in range(grid_size):
        for x in range(grid_size):
            if (x, y) in grid and display_antennas:
                print(grid[x,y], end="")
            elif (x, y) in antinodes:
                print("#", end="")
            else:
                print('.', end="")  
        print()
    print()


def part1(filename: str) -> int:
    grid, grid_size, antennas = read_input(filename)
    antinodes = set()

    for _, ants in antennas.items():
        for ant1, ant2 in combinations(ants, 2):
            vec = (ant2[0] - ant1[0], ant2[1] - ant1[1])            
            antinodes.update([ p for p in [ (ant1[0] - vec[0], ant1[1] - vec[1]), (ant2[0] + vec[0], ant2[1] + vec[1])] if in_bounds(grid, p, grid_size)])
            
    return len(antinodes)


def part2(filename: str) -> int:
    grid, grid_size, antennas = read_input(filename)
    antinodes = set()

    for _, ants in antennas.items():
        for ant1, ant2 in combinations(ants, 2):
            vec = (ant2[0] - ant1[0], ant2[1] - ant1[1])

            p = ant1
            while in_bounds(grid, p, grid_size):
                antinodes.add(p)
                p = (p[0] + vec[0], p[1] + vec[1])

            p = ant1
            while in_bounds(grid, p, grid_size):
                antinodes.add(p)
                p = (p[0] - vec[0], p[1] - vec[1])

    return len(antinodes)

# ic.disable()

# assert ic(part1('./sample1.txt')) == 2
# assert ic(part1('./sample2.txt')) == 4
assert ic(part1('./sample.txt')) == 14
assert ic(part1('./input.txt')) == 222

# assert ic(part2('./sample3.txt')) == 9
assert ic(part2('./sample.txt')) == 34
assert ic(part2('./input.txt')) == 884

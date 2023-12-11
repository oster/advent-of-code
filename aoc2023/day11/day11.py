from typing import Generator

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()


def parse_input(filename : str) -> list[tuple[int, int,int]]:
    input = read_input(filename)

    galaxy_id = 0
    galaxies = []
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            if c == '#':
                galaxy_id = galaxy_id + 1
                galaxies.append((galaxy_id, x, y))

    return galaxies


def manhattan_distance(g1, g2):
    return abs(g1[1] - g2[1]) + abs(g1[2] - g2[2])


def sum_of_manhattan_distances(galaxies):
    sum = 0
    for i in range(0, len(galaxies)):
        g1 = galaxies[i]
        for j in range(i+1, len(galaxies)):
            g2 = galaxies[j]
            d = manhattan_distance(g1, g2)
            sum += d

    return sum


def part1(filename : str, times=2) -> int:
    galaxies = parse_input(filename)

    # expand on y-axis
    # galaxies are aleady sorted by y according to parsing
    frontiers = []
    for y in range(galaxies[0][2], galaxies[-1][2]):
        if len(list(filter(lambda g: g[2] == y, galaxies))) == 0:
            frontiers.append(y)

    expanded_galaxies = []
    idx = 0
    for g in galaxies:
        while idx < len(frontiers) and frontiers[idx] < g[2]:
            idx += 1
        expanded_galaxies.append((g[0], g[1], g[2]+(idx*(times-1))))
    galaxies = expanded_galaxies


    # expand on x-axis
    galaxies = sorted(galaxies, key=lambda g: g[1]) # sort by x
    frontiers = []
    for x in range(galaxies[0][1], galaxies[-1][1]):
        if len(list(filter(lambda g: g[1] == x, galaxies))) == 0:
            frontiers.append(x)

    expanded_galaxies = []
    idx = 0
    for g in galaxies:
        while idx < len(frontiers) and frontiers[idx] < g[1]:
            idx += 1
        expanded_galaxies.append((g[0], g[1]+(idx*(times-1)), g[2]))
    galaxies = expanded_galaxies
    

    galaxies = sorted(galaxies, key=lambda g: g[0])
    return sum_of_manhattan_distances(galaxies)


def part2(filename : str, times) -> int:
    return part1(filename, times)


assert part1('./sample.txt') == 374
assert part1('./input.txt') == 9623138

assert part2('./sample.txt', 10) == 1030
assert part2('./sample.txt', 100) == 8410
assert part2('./input.txt', 1000000) == 726820169514

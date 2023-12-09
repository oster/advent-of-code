from typing import Generator
from itertools import tee
from functools import reduce

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()


def parse_input(filename : str) -> list[list[int]]:
    input = read_input(filename)

    histories = []
    for lines in input:
        history = map(int, lines.split())
        histories.append(list(history))

    return histories


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def part1(filename : str) -> int:
    histories = parse_input(filename)

    challenge = 0
    for h in histories:
        lasts = []
        while any(map(lambda x: x != 0, h)):
            lasts.append(h[-1])
            h = [ (b-a) for a,b in pairwise(h) ]
            
        s = sum(lasts)
        challenge += s
    
    return challenge


def part2(filename : str) -> int:
    histories = parse_input(filename)

    challenge = 0
    for h in histories:
        firsts = []
        while any(map(lambda x: x != 0, h)):
            firsts.append(h[0])
            h = [ (b-a) for a,b in pairwise(h) ]

        s = reduce(lambda x,y: y-x, reversed(firsts), 0)
        challenge += s

    return challenge


assert part1('./sample.txt') == 114
assert part1('./input.txt') == 1731106378

assert part2('./sample.txt') == 2
assert part2('./input.txt') == 1087

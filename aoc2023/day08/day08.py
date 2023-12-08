from typing import Generator
import math

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()


def parse_input(filename : str) -> tuple[list[int], dict[str, str]]:
    input = read_input(filename)

    instructions = list(map(lambda ins: 0 if ins == 'L' else 1, input.__next__().rstrip()))

    input.__next__() # skip blank

    path = {}
    for line in input:
        # ZZZ = (ZZZ, ZZZ)
        src, left, right = line[0:3], line[7:10], line[12:15]
        path[src] = (left, right)

    return (instructions, path)


def part1(filename : str) -> int:
    instructions, next_step = parse_input(filename)

    current = 'AAA'
    i = 0
    n = len(instructions)
    step = 0
    while current != 'ZZZ':
        step += 1
        current = next_step[current][instructions[i]]
        i = (i + 1) % n

    return step


# # Greatest Common Divisor
# def gcd_brute(a, b):
#     while b > 0:
#         a, b = b, a % b
#     return a

# def gcd_rec(a, b):
#     if a == 0:
#         return b
#     return gcd_rec(b % a, a)


def lcm(a : int, b : int) -> int:
    # Lowest Common Multiple
    return a * b // math.gcd(a, b)


def lcms(values : list[int]):
    llcm = 1
    for v in values:
        llcm = lcm(llcm, v)
    return llcm


def part2(filename : str) -> int:
    instructions, next_step = parse_input(filename)

    starts = []
    for k, _ in next_step.items():
        if k[2] =='A':
            starts.append(k)

    n = len(instructions)
    cycles = []
    for start in starts:         
        current = start
        i = 0
        step = 0
        while current[2] != 'Z':
            step += 1
            current = next_step[current][instructions[i]]
            i = (i + 1) % n

        cycles.append(step)

    return lcms(cycles)


assert part1('./sample.txt') == 2
assert part1('./sample2.txt') == 6
assert part1('./input.txt') == 14257

assert part2('./sample3.txt') == 6
assert part2('./input.txt') == 16187743689077

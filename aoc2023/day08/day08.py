from typing import Generator
import math

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()


def parse_input(filename : str) -> tuple[str, dict]:
    input = read_input(filename)

    instructions = input.__next__().rstrip()
    input.__next__()

    step = {}

    for line in input:
        src, other = line.split('=')
        src = src.strip()

        left, right = other.split(',')
        left, right = left.strip()[1:], right.strip()[:-1]

        step[src] = (left, right)

    return (instructions, step)


def part1(filename : str) -> int:
    instructions, next_step = parse_input(filename)

    current = 'AAA'
    i = 0
    n = len(instructions)
    step = 0
    while current != 'ZZZ':
        step = step + 1
        if instructions[i] == 'L':
            current = next_step[current][0]
        else:
            current = next_step[current][1]
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


def lcm(a, b):
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
            step = step + 1
            if instructions[i] == 'L':
                current = next_step[current][0]
            else:
                current = next_step[current][1]
            i = (i + 1) % n
        cycles.append(step)

    return lcms(cycles)


assert part1('./sample.txt') == 2
assert part1('./sample2.txt') == 6
assert part1('./input.txt') == 14257

assert part2('./sample3.txt') == 6
assert part2('./input.txt') == 16187743689077

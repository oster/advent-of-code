from typing import Generator
import math

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()

def parse_input_part_1(filename : str) -> tuple[list[int], list[int]]:
    inputs = read_input(filename)

    times = list(map(int, inputs.__next__()[len('Time:'):].split()))
    distances = list(map(int, inputs.__next__()[len('Distance:'):].split()))

    return times, distances


def parse_input_part1(filename : str) -> tuple[list[int], list[int]]:
    inputs = read_input(filename)

    times = list(map(int, inputs.__next__()[len('Time:'):].split()))
    distances = list(map(int, inputs.__next__()[len('Distance:'):].split()))

    return times, distances


def parse_input_part2(filename : str) -> tuple[int, int]:
    inputs = read_input(filename)

    time = int(inputs.__next__()[len('Time:'):].replace(' ',''))
    distance = int(inputs.__next__()[len('Distance:'):].replace(' ',''))

    return time, distance


def part1(filename : str) -> int:
    times, distances = parse_input_part1(filename)

    res = 1
    for idx, time in enumerate(times):
        count = 0
        distance = distances[idx]
        for start in range(0, time+1):
            if (time-start)*start > distance:
                count += 1
        res *= count

    return res


def part2_brute(filename : str) -> int:
    time, distance = parse_input_part2(filename)

    count = 0
    for start in range(0, time+1):
        if (time-start)*start > distance:
            count += 1

    return count


def part2(filename : str) -> int:
    time, distance = parse_input_part2(filename)

    a = -1
    b = time
    c = -distance

    # Δ = b² - 4ac
    delta = (b * b) - 4 * (a * c)

    # x1 = -b - √Δ / 2a 
    x1 = (-b - math.sqrt(delta)) / (2 * a)

    # x2 = -b + √Δ / 2a
    x2 = (-b + math.sqrt(delta)) / (2 * a)

    return int(x1) - int(x2)


assert part1('./sample.txt') == 288
assert part1('./input.txt') == 1624896

assert part2('./sample.txt') == 71503
# assert part2_brute('./input.txt') == 32583852
assert part2('./input.txt') == 32583852

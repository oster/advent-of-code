import sys
from statistics import median


def read_data(filename: str) -> list[int]:
    with open(filename, "r") as data_file:
        values = list(map(int, data_file.readline().rstrip().split(",")))
    return values


def part1(filename: str) -> int:
    values = read_data(filename)

    # min_value = min(values)
    # max_value = max(values)
    # min_sum = sys.maxsize

    # for k in range(min_value, max_value + 1):
    #     sum_d = 0
    #     for v in values:
    #         sum_d += abs(k - v)

    #     if sum_d < min_sum:
    #         min_sum = sum_d

    # return min_sum

    # or since, the median minimizes the sum of absolute deviations
    best_x = median(values)
    return sum((int(abs(best_x - v)) for v in values))


def part2(filename: str) -> int:
    values = read_data(filename)

    min_value = min(values)
    max_value = max(values)

    min_sum = sys.maxsize

    for k in range(min_value, max_value + 1):
        sum_d = 0
        for v in values:
            d = abs(k - v)
            sum_d += d * (d + 1) // 2

        if sum_d < min_sum:
            min_sum = sum_d

    return min_sum


assert part1("sample.txt") == 37
assert part1("input.txt") == 349812

assert part2("sample.txt") == 168
assert part2("input.txt") == 99763899

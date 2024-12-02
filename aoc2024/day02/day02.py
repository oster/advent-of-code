from icecream import ic
from itertools import pairwise


def read_data(filename: str) -> list[list[int]]:
    values = []
    with open(filename, "r") as data_file:
        for line in data_file:
            values.append(list(map(int, line.split())))
    return values


def validate_levels(levels: list[int]) -> bool:
    return (
        levels[0] < levels[1]
        and all(
            lvl1 < lvl2 and 1 <= abs(lvl1 - lvl2) <= 3
            for lvl1, lvl2 in pairwise(levels)
        )
        or levels[0] > levels[1]
        and all(
            lvl1 > lvl2 and 1 <= abs(lvl1 - lvl2) <= 3
            for lvl1, lvl2 in pairwise(levels)
        )
    )


# def part1(filename: str) -> int:
#     all_levels = read_data(filename)
#     count = 0
#     for levels in all_levels:
#         if validate_levels(levels):
#             count += 1
#     return count


def part1(filename: str) -> int:
    all_levels = read_data(filename)
    return sum(validate_levels(levels) for levels in all_levels)


# def part2(filename: str) -> int:
#     all_levels = read_data(filename)
#     count = 0
#     for levels in all_levels:
#         if validate_levels(levels):
#             count += 1
#         else:
#             is_now_valid = False
#             for idx in range(len(levels)):
#                 l = levels[:idx] + levels[idx + 1 :]
#                 if validate_levels(l):
#                     is_now_valid = True
#                     break
#             if is_now_valid:
#                 count += 1
#     return count


def part2(filename: str) -> int:
    all_levels = read_data(filename)
    return sum(
        (
            validate_levels(levels)
            or any(
                validate_levels(fixed_levels)
                for idx in range(len(levels))
                if (fixed_levels := levels[:idx] + levels[idx + 1 :])
            )
        )
        for levels in all_levels
    )


# ic.disable()

assert ic(part1("./sample.txt")) == 2
assert ic(part1("./input.txt")) == 572

assert ic(part2("./sample.txt")) == 4
assert ic(part2("./input.txt")) == 612

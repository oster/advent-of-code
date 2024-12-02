from icecream import ic
from itertools import tee


def window2(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def read_data(filename: str) -> list[list[int]]:
    values = []
    with open(filename, "r") as data_file:
        for line in data_file:
            values.append([(b-a) for a, b in window2(map(int, line.split()))])
    return values


def validate_level_differences(diffs: list[int]) -> bool:
    return (
        all(diff < 0 and 1 <= abs(diff) <=3 for diff in diffs)
        or all(diff > 0 and 1 <= abs(diff) <=3 for diff in diffs)
    )


def part1(filename: str) -> int:
    all_level_differences = read_data(filename)
    return sum(validate_level_differences(diff) for diff in all_level_differences)


def validate_levels_with_error(diff: list[int]) -> bool:
        diff_size = len(diff)

        if diff_size <= 2:
            raise ValueError("unsupported input")
        
        sign = 1
        if (diff[0] < 0 and diff[1] < 0) or (diff[0] < 0 and diff[2] < 0) or (diff[1] < 0 and diff[2] < 0):
            sign = -1

        joker_used = False
        idx = 0
        while idx < diff_size:
            if 1 <= sign*diff[idx] <= 3:
                pass
            else:
                if joker_used:
                    return False
                joker_used = True
                if idx >= 0:
                    if idx+1 == diff_size:
                        pass
                    elif 1 <= sign*(diff[idx]+diff[idx+1]) <= 3:
                        idx += 1
                    elif idx == 0:
                        pass
                    elif 1 <= sign*(diff[idx-1]+diff[idx]) <= 3:
                        pass
                    else:
                        return False
            idx += 1
        return True


def part2(filename: str) -> int:
    all_level_differences = read_data(filename)
    return sum(validate_levels_with_error(diff) for diff in all_level_differences)


assert ic(part1("./sample.txt")) == 2
assert ic(part1("./input.txt")) == 572


assert ic(part2("./sample.txt")) == 4
assert ic(part2("./input.txt")) == 612



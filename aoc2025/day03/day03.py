from typing import Any
from icecream import ic


def read_data(filename: str) -> list[list[int]]:
    with open(filename, "r") as data_file:
        banks = [[int(v) for v in line.strip()] for line in data_file]

    return banks


def max_with_index(l: list[Any]) -> tuple[Any, int]:
    m_idx = -1
    m = -1

    for idx, v in enumerate(l):
        if v > m:
            m, m_idx = v, idx

    return (m, m_idx)


def part1(filename: str) -> int:
    banks = read_data(filename)

    jolts = 0
    for bank in banks:
        max1, max1_idx = max_with_index(bank[:-1])
        max2 = max(bank[max1_idx + 1 :])
        jolt = max1 * 10 + max2
        jolts += jolt
    return jolts


def biggest_number(bank, size):
    if size == 1:
        return max(bank)

    remaining_len = size - 1
    m, idx = max_with_index(bank[:-remaining_len])
    return (m * 10**remaining_len) + biggest_number(bank[idx + 1 :], remaining_len)


def part2(filename: str) -> int:
    banks = read_data(filename)
    return sum(biggest_number(from_bank, 12) for from_bank in banks)


# ic.disable()

assert ic(part1("./sample.txt")) == 357
assert ic(part1("./input.txt")) == 17346

assert ic(part2("./sample.txt")) == 3121910778619
assert ic(part2("./input.txt")) == 172981362045136

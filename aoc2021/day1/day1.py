from typing import Iterator


def read_data(filename: str) -> list[int]:
    data = []
    with open(filename, "r") as data_file:
        data = [int(l) for l in data_file.readlines()]

    return data


def window2(data: list[int]) -> Iterator[tuple[int, int]]:
    for i in range(1, len(data)):
        yield (data[i - 1], data[i])


# Problem 1: the number of times a depth measurement increases
def part1(filename: str) -> int:
    data = read_data(filename)
    count = 0
    for a, b in window2(data):
        if a < b:
            count += 1
    return count


assert part1("sample.txt") == 7
assert part1("input.txt") == 1791


def window3(data: list[int]) -> Iterator[tuple[int, int, int]]:
    for i in range(2, len(data)):
        yield (data[i - 2], data[i - 1], data[i])


# Problem 2: three-measurement sliding window
def part2(filename: str) -> int:
    data = read_data(filename)

    count = 0
    for t1, t2 in zip(window3(data), window3(data[1:])):
        if sum(t1) < sum(t2):
            count += 1
    return count


assert part2("sample.txt") == 5
assert part2("input.txt") == 1822

from icecream import ic
from typing import Generator


def read_data(filename: str) -> str:
    with open(filename, "r") as data_file:
        return data_file.read().strip()


def parse_int(values: str, idx: int) -> tuple[int|None, int]:
    n = None
    while values[idx].isdigit():
        if n is None:
            n = 0
        n = n*10 + int(values[idx])
        idx += 1
    return n, idx


def yield_mul(values: str) -> Generator[tuple[int, int], None, None]:
    idx = 0
    while idx < len(values):
        match values[idx]:
            case 'm':
                if values[idx:idx+4] == 'mul(':
                    idx += 4
                    a, idx = parse_int(values, idx)
                    if a is None:
                        idx += 1
                        continue
                    if values[idx] != ',':
                        continue
                    idx += 1
                    b, idx = parse_int(values, idx)
                    if b is None:
                        idx += 1
                        continue
                    if values[idx] != ')':
                        continue
                    yield (a,b)
            case _:
                pass
        idx += 1


def part1(filename: str) -> int:
    values = read_data(filename)
    return sum(a*b for a,b in yield_mul(values))


def yield_mul_part2(values: str) -> Generator[tuple[int, int], None, None]:
    do = True

    idx = 0
    while idx < len(values):
        match values[idx]:
            case 'd':
                if values[idx:idx+4] == "do()":
                    do = True
                    idx += 4
                    continue
                if values[idx:idx+7] == "don't()":
                    do = False
                    idx += 8
                    continue
            case 'm':
                if values[idx:idx+4] == 'mul(':
                    idx += 4
                    a, idx = parse_int(values, idx)
                    if a is None:
                        idx += 1
                        continue
                    if values[idx] != ',':
                        continue
                    idx += 1
                    b, idx = parse_int(values, idx)
                    if b is None:
                        idx += 1
                        continue
                    if values[idx] != ')':
                        continue
                    if do:
                        yield (a,b)
            case _:
                pass
        idx += 1


def part2(filename: str) -> int:
    values = read_data(filename)
    return sum(a*b for a,b in yield_mul_part2(values))


assert ic(part1('./sample.txt')) == 161
assert ic(part1('./input.txt')) == 189600467


assert ic(part2('./sample2.txt')) == 48
assert ic(part2('./input.txt')) == 107069718

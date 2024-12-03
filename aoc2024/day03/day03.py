from icecream import ic
import re

def read_data(filename: str) -> str:
    with open(filename, "r") as data_file:
        return data_file.read().strip()


def part1(filename: str) -> int:
    values = read_data(filename)

    p = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    return sum(int(a)*int(b) for a, b in p.findall(values))
    # return sum(int(m.group(1))*int(m.group(2)) for m in p.finditer(values))


def part2(filename: str) -> int:
    values = read_data(filename)

    p = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")

    s = 0
    enable = True
    for m in p.finditer(values):
        match m.group():
            case 'do()':
                enable = True
            case "don't()":
                enable = False
            case _:
                if enable:
                    a, b = int(m.group(1)), int(m.group(2))
                    s += a*b

    return s


assert ic(part1('./sample.txt')) == 161
assert ic(part1('./input.txt')) == 189600467


assert ic(part2('./sample2.txt')) == 48
assert ic(part2('./input.txt')) == 107069718

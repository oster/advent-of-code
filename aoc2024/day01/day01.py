from icecream import ic

def read_data(filename: str) -> tuple[list[int], list[int]]:
    values1 = []
    values2 =[]
    with open(filename, "r") as data_file:
        for v1, v2 in map(str.split, data_file.readlines()):
            values1.append(int(v1))
            values2.append(int(v2))
    return (values1, values2)


def part1(filename: str) -> int:
    l1, l2 = read_data(filename)
    return sum(abs(v1-v2) for (v1, v2) in zip(sorted(l1), sorted(l2)))


def part2(filename: str) -> int:
    l1, l2 = read_data(filename)

    counters = {}
    for v in l2:
        counters[v] = counters.get(v, 0) + 1

    return sum((v*counters.get(v, 0) for v in l1))

# ic.disable()

assert ic(part1('./sample.txt')) == 11
assert ic(part1('./input.txt')) == 1722302

assert ic(part2('./sample.txt')) == 31
assert ic(part2('./input.txt')) == 20373490


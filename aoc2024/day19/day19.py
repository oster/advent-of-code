from icecream import ic


def read_data(filename: str) -> tuple[list[str], list[str]]:
    with open(filename, "r") as data_file:
        t, ds = data_file.read().split("\n\n")
        towels = list(map(str.strip, t.split(",")))
        designs = [d.strip() for d in ds.split("\n")][:-1]
    return towels, designs


def can_build(depth: int, design: str, towels: list[str]) -> bool:
    if len(design) == 0:
        return True

    for towel in towels:
        l = len(towel)
        if design[:l] == towel:
            ok = can_build(depth + l, design[l:], towels)
            if ok:
                return True

    return False


def part1(filename: str) -> int:
    towels, designs = read_data(filename)
    towels = sorted(towels, key=lambda x: len(x), reverse=True)

    count = 0
    for d in designs:
        if can_build(0, d, towels):
            count += 1
    return count


mem = {}

def can_build_all(design: str, towels: list[str]) -> int:
    if design in mem:
        return mem[design]

    if len(design) == 0:
        return 1

    res = 0
    for towel in towels:
        l = len(towel)
        if design[:l] == towel:
            ok = can_build_all(design[l:], towels)
            res += ok

    mem[design] = res
    return res


def part2(filename: str) -> int:
    global mem
    mem = {}
    towels, designs = read_data(filename)
    towels = sorted(towels, key=lambda x: len(x), reverse=True)
    count = 0
    for d in designs:
        r = can_build_all(d, towels)
        count += r
    return count


# ic.disable()

assert ic(part1("./sample.txt")) == 6
assert ic(part1("./input.txt")) == 358

assert ic(part2("./sample.txt")) == 16
assert ic(part2("./input.txt")) == 600639829400603

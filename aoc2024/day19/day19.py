from icecream import ic


def read_data(filename: str) -> tuple[list[str], list[str]]:
    with open(filename, "r") as data_file:
        t, ds = data_file.read().split("\n\n")
        towels = t.split(", ")
        designs = [d.strip() for d in ds.rstrip().split("\n")]
    return towels, designs


def can_build(design: str, towels: list[str]) -> bool:
    if len(design) == 0:
        return True

    if design in mem:
        return mem[design]

    for towel in towels:
        l = len(towel)
        if design[:l] == towel:
            ok = can_build(design[l:], towels)
            if ok:
                mem[design] = True
                return True

    mem[design] = False
    return False


def part1(filename: str) -> int:
    global mem
    mem.clear()

    towels, designs = read_data(filename)
    towels = sorted(towels, key=lambda x: len(x), reverse=True)

    count = sum(can_build(d, towels) for d in designs)
    return count


mem = {}


def can_build_all(design: str, towels: list[str]) -> int:
    if len(design) == 0:
        return 1

    if design in mem:
        return mem[design]

    res = 0
    for towel in towels:
        l = len(towel)
        if design[:l] == towel:
            res += can_build_all(design[l:], towels)

    mem[design] = res
    return res


def part2(filename: str) -> int:
    global mem
    mem.clear()

    towels, designs = read_data(filename)
    towels = sorted(towels, key=lambda x: len(x), reverse=True)

    count = sum(can_build_all(d, towels) for d in designs)
    return count


# ic.disable()

assert ic(part1("./sample.txt")) == 6
assert ic(part1("./input.txt")) == 358

assert ic(part2("./sample.txt")) == 16
assert ic(part2("./input.txt")) == 600639829400603

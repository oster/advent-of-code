from icecream import ic


def rotate_counter_90(matrix: list[str]) -> list[str]:
    return [
        "".join([matrix[y][x] for y in range(0, len(matrix), 1)])
        for x in range(len(matrix[0]))
    ]


def read_data(filename: str) -> tuple[list[tuple[int]], list[tuple[int]]]:
    locks = []
    keys = []

    with open(filename, "r") as data_file:
        data = data_file.read().strip()
        schematics = data.split("\n\n")

        for schematic in schematics:
            if schematic == "":
                continue

            schematic = list(map(str.strip, schematic.split("\n")))
            schematic = rotate_counter_90(schematic)

            is_lock = all([schematic[y][0] == "#" for y in range(0, len(schematic))])
            if is_lock:
                locks.append(tuple(s.count("#") - 1 for s in schematic))
            else:
                keys.append(tuple(s.count("#") - 1 for s in schematic))

    return locks, keys


def fit(key: tuple[int], lock: tuple[int]) -> bool:
    for k, l in zip(key, lock):
        if k + l > 5:
            return False
    return True


def part1(filename: str) -> int:
    locks, keys = read_data(filename)
    return sum([fit(key, lock) for lock in locks for key in keys])


def part2(filename: str) -> int:
    return 0


# ic.disable()

assert ic(part1("./sample.txt")) == 3
assert ic(part1("./input.txt")) == 3395

# assert ic(part2('./sample.txt')) == 0
# assert ic(part2('./input.txt')) == 0

from icecream import ic


def read_data(filename: str) -> list[tuple[int, int]]:
    values = []
    with open(filename, "r") as data_file:
        line = data_file.readlines()[0].strip()

        for interval in line.split(","):
            start, end = interval.split("-")
            values.append((int(start), int(end)))
    return values


def is_invalid_p1(id: int) -> bool:
    str_id = str(id)

    if len(str_id) % 2 != 0:
        return False

    half = len(str_id) // 2
    return str_id[:half] == str_id[half:]


def part1(filename: str) -> int:
    values = read_data(filename)

    invalids = []
    for start, end in values:
        invalids.extend((id for id in range(start, end + 1) if is_invalid_p1(id)))

    return sum(invalids)


def is_invalid_p2(id: int) -> bool:
    str_id = str(id)

    for split_count in range(2, len(str_id) + 1):
        if len(str_id) % split_count == 0:
            size = len(str_id) // split_count
            first = str_id[:size]
            chunks = (str_id[size * i : size * (i + 1)] for i in range(1, split_count))

            if all((first == chunk for chunk in chunks)):
                return True

    return False


def part2(filename: str) -> int:
    values = read_data(filename)

    invalids = []
    for start, end in values:
        invalids.extend((id for id in range(start, end + 1) if is_invalid_p2(id)))

    return sum(invalids)


# ic.disable()

assert ic(part1("./sample.txt")) == 1227775554
assert ic(part1("./input.txt")) == 18952700150


# assert ic(is_invalid_p2(99)) == True
# assert ic(is_invalid_p2(111)) == True
# assert ic(is_invalid_p2(110)) == False
# assert ic(is_invalid_p2(565656)) == True
# assert ic(is_invalid_p2(2121212121)) == True

assert ic(part2("./sample.txt")) == 4174379265
assert ic(part2("./input.txt")) == 28858486244

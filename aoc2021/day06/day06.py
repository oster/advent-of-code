def read_data(filename: str) -> list[int]:
    with open(filename, "r") as data_file:
        values = list(map(int, data_file.readline().rstrip().split(",")))
    return values


def part1(filename: str, days: int) -> int:
    values = read_data(filename)

    lanternfishes = [0] * 9  # at index k = the number of lanternfishes of age k

    for value in values:
        lanternfishes[value] += 1

    for _ in range(days):
        creators = lanternfishes[0]
        for k in range(1, 9):
            lanternfishes[k - 1] = lanternfishes[k]
        lanternfishes[8] = creators
        lanternfishes[6] += creators

    return sum(lanternfishes)


def part2(filename: str, days: int) -> int:
    return part1(filename, days)


assert part1("sample.txt", 18) == 26
assert part1("sample.txt", 80) == 5934
assert part1("input.txt", 80) == 396210

assert part2("sample.txt", 256) == 26984457539
assert part2("input.txt", 256) == 1770823541496

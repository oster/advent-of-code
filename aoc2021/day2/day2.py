def read_data(filename: str) -> list[tuple[str, int]]:
    data = []
    with open(filename, "r") as data_file:
        for line in data_file:
            direction, length = line.rstrip().split()
            data.append((direction, int(length)))
        
    return data


def part1(filename: str) -> int:
    data = read_data(filename)

    x = 0
    depth = 0
    for direction, length in data:
        match direction:
            case "forward":
                x += length
            case "up":
                depth -= length
            case "down":
                depth += length
    return x * depth

assert part1("sample.txt") == 150
assert part1("input.txt") == 2019945


def part2(filename: str) -> int:
    data = read_data(filename)

    x = 0
    depth = 0
    aim = 0
    for direction, length in data:
        match direction:
            case "forward":
                x += length
                depth += aim * length
            case "up":
                aim -= length
            case "down":
                aim += length
    return x * depth

assert part2("sample.txt") == 900
assert part2("input.txt") == 1599311480

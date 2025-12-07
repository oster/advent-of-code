from icecream import ic

type Pos = tuple[int, int]


def read_data(filename: str) -> tuple[Pos, dict[Pos, str], tuple[int, int]]:
    start = (0, 0)
    splits = {}
    height = 0
    width = 0

    with open(filename, "r") as input_file:
        content = input_file.readlines()

        width = len(content[0]) - 1
        height = len(content) - 1

        for y, line in enumerate(content):
            for x, c in enumerate(line.strip()):
                match c:
                    case ".":
                        continue
                    case "S":
                        start = (x, y)
                    case "^":
                        splits[(x, y)] = "^"

    return start, splits, (width, height)


def mark(x, y, splits, beams, width, height, activated, path_counts):
    if x < 0 or x >= width or y < 0:
        return 0

    if y > height:
        return 1

    current = (x, y)

    if current in beams:
        return path_counts[current]

    if current in splits:
        if not current in path_counts:
            activated.add(current)
            a = mark(x - 1, y + 1, splits, beams, width, height, activated, path_counts)
            b = mark(x + 1, y + 1, splits, beams, width, height, activated, path_counts)
            r = a + b
            path_counts[current] = r
            return r
    else:
        beams[current] = "|"
        c = mark(x, y + 1, splits, beams, width, height, activated, path_counts)
        path_counts[current] = c
        return c


def part1(filename: str) -> int:
    data = read_data(filename)
    start, splits, (width, height) = data
    (start_x, start_y) = start

    mark(start_x, start_y + 1, splits, {}, width, height, activated_splits := set(), {})
    return len(activated_splits)


def part2(filename: str) -> int:
    data = read_data(filename)
    start, splits, (width, height) = data
    (start_x, start_y) = start

    path_count = mark(start_x, start_y + 1, splits, {}, width, height, set(), {})
    return path_count


# ic.disable()

assert ic(part1("./sample.txt")) == 21
assert ic(part1("./input.txt")) == 1667

assert ic(part2("./sample.txt")) == 40
assert ic(part2("./input.txt")) == 62943905501815

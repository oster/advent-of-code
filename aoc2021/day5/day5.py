type Line = tuple[tuple[int, int], tuple[int, int]]
type Grid = list[list[int]]


def dump_grid(card: Grid) -> None:
    for row in card:
        for col in row:
            print(f"{col:2d}", end=" ")
        print()
    print()


def read_data(filename: str) -> list[Line]:
    lines = []
    with open(filename, "r") as data_file:
        for line in data_file:
            p1_str, p2_str = line.rstrip().split(" -> ")
            p1 = tuple(map(int, p1_str.split(",")))
            p2 = tuple(map(int, p2_str.split(",")))
            lines.append((p1, p2))

    return lines


def sign(x: int) -> int:
    return 1 if x > 0 else -1


def part1(filename: str) -> int:
    lines = read_data(filename)

    # keep only horizontal and vertical lines
    lines = list(
        filter(lambda line: line[0][0] == line[1][0] or line[0][1] == line[1][1], lines)
    )

    max_x = 0
    max_y = 0

    for (x1, y1), (x2, y2) in lines:
        max_x = max(max(max_x, x1), x2)
        max_y = max(max(max_y, y1), y2)

    grid = [[0] * (max_x + 1) for _ in range(max_y + 1)]

    for (x1, y1), (x2, y2) in lines:
        sign_y = sign(y2 - y1)
        sign_x = sign(x2 - x1)
        for y in range(y1, y2 + sign_y, sign_y):
            for x in range(x1, x2 + sign_x, sign_x):
                grid[y][x] += 1

    count = 0
    for row in grid:
        for col in row:
            if col > 1:
                count += 1

    return count


def part2(filename: str) -> int:
    lines = read_data(filename)

    max_x = 0
    max_y = 0

    for (x1, y1), (x2, y2) in lines:
        max_x = max(max(max_x, x1), x2)
        max_y = max(max(max_y, y1), y2)

    grid = [[0] * (max_x + 1) for _ in range(max_y + 1)]

    for (x1, y1), (x2, y2) in lines:
        sign_y = sign(y2 - y1)
        sign_x = sign(x2 - x1)
        if x1 == x2 or y1 == y2:
            # horitontal or vertical line
            for y in range(y1, y2 + sign_y, sign_y):
                for x in range(x1, x2 + sign_x, sign_x):
                    grid[y][x] += 1
        else:
            # diagonal line
            length = abs(x2 - x1) + 1
            for k in range(length):
                grid[y1 + k * sign_y][x1 + k * sign_x] += 1

    count = 0
    for row in grid:
        for col in row:
            if col > 1:
                count += 1

    return count


assert part1("sample.txt") == 5
assert part1("input.txt") == 6267

assert part2("sample.txt") == 12
assert part2("input.txt") == 13158

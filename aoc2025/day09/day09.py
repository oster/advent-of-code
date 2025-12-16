from itertools import pairwise, islice
from typing import Generator, Iterable
from icecream import ic


type Pos = tuple[int, int]
type Grid = dict[Pos, str]


def read_data(filename: str) -> list[Pos]:
    data = []
    with open(filename, "r") as input_file:
        for line in map(str.strip, input_file.readlines()):
            a, b = line.split(",")
            data.append(
                (
                    int(a),
                    int(b),
                )
            )
    return data


def rectangles(points: Iterable[Pos]) -> Generator[tuple[int, Pos, Pos]]:
    for i, (x1, y1) in enumerate(points):
        for x2, y2 in islice(points, i+1, None):
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            yield (
                area,
                (x1, y1),
                (x2, y2),
            )


def part1(filename: str) -> int:
    data = read_data(filename)
    max_area = -1
    for area, _, _ in rectangles(data):
        if area > max_area:
            max_area = area
    return max_area


def crossed_by_segment(p1: Pos, p2: Pos, segments: Iterable[tuple[Pos, Pos]]) -> bool:
    left = min(p1, p2, key=lambda p: p[0])
    right = p1 if left == p2 else p2

    left_x, _ = left
    right_x, _ = right

    top = min(p1, p2, key=lambda p: p[1])
    bottom = p1 if top == p2 else p2

    _, top_y = top
    _, bottom_y = bottom

    for pa, pb in segments:
        if pa == p1 or pa == p2 or pb == p1 or pb == p2:
            continue

        xa, ya = pa
        xb, yb = pb

        a_inside_r = left_x < xa < right_x and top_y < ya < bottom_y
        if a_inside_r:
            return True

        #       top_s
        #        |
        #   x--------x top_y
        #   |    |   |
        #   |    |   |
        #   |    |   |
        #   x--------x bottom_y
        #        |
        #      bottom_s

        if xa == xb:  # vertical segment
            xs = xa
            top_s = min(ya, yb)
            bottom_s = ya if top_s == yb else yb

            if (left_x < xs < right_x) and (top_s <= top_y and bottom_s > top_y):
                return True
        else:  # horizontal segment
            assert ya == yb
            ys = ya
            left_s = min(xa, xb)
            right_s = xa if left_s == xb else xb

            if (top_y < ys < bottom_y) and (left_s <= left_x and right_s > left_x):
                return True
    return False


def part2(filename: str) -> int:
    data = read_data(filename)

    for area, p1, p2 in sorted(rectangles(data), key=lambda x: x[0], reverse=True):
        if not crossed_by_segment(p1, p2, pairwise(data + [data[0]])):
            return area

    return -1


# ic.disable()

assert ic(part1("./sample.txt")) == 50
assert ic(part1("./input.txt")) == 4769758290

assert ic(part2("./sample.txt")) == 24
assert ic(part2("./input.txt")) == 1588990708

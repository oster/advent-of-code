from icecream import ic
from typing import Optional
import sys


def read_data(filename: str):
    data = {}

    shapes = []
    regions = []

    with open(filename, "r") as input_file:

        for block in input_file.read().split('\n\n'):

            if block[1] == ':':
                shape_index = int(block[0])
                shape = list(map(list, block[3:].split()))
                shapes.append(shape)
            else:            
                for region_spec in block.strip().split('\n'):
                    area_spec, gifts_spec = region_spec.split(':')
                    area_size = tuple(map(int, area_spec.split('x')))

                    gifts_count = list(map(int, gifts_spec.split()))
                    regions.append((area_size, gifts_count))

    return (shapes, regions)


def minmax(shape: list[list[str]]) -> Optional[tuple[int, int, int, int]]:
    min_x = len(shape[0])
    max_x = 0
    min_y = len(shape)
    max_y = 0

    for y, row in enumerate(shape):
        for x, ch in enumerate(row):
            if ch == "#":
                if x < min_x: min_x = x
                if y < min_y: min_y = y
                if x > max_x: max_x = x
                if y > max_y: max_y = y

    if min_x == len(shape):  # no '#'
        return None

    return min_x, min_y, max_x, max_y


def part1(filename: str) -> int:
    shapes_spec, regions = read_data(filename)

    count = 0
    needed_dashes = {}

    for idx, shape in enumerate(shapes_spec):
        min_x, min_y, max_x, max_y = minmax(shape)
        w = max_x - min_x + 1
        h = max_y - min_y + 1
        needed_dashes[idx] = w*h

    for (w,h), shape_counts in regions:
        area = w * h
        s = 0
        for idx, cc in enumerate(shape_counts):
            s = s + cc * needed_dashes[idx]

        if s <= area:
            count += 1

    return count

# assert ic(part1("./sample.txt")) == 2
assert ic(part1("./input.txt")) == 499

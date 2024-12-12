from typing import Counter, Generator
from dataclasses import dataclass
from icecream import ic
import math
import sys
from enum import IntEnum

type Grid = dict[Pos, str]
type Pos = tuple[int, int]

# from typing import NewType
# Pos = NewType('Pos', tuple[int, int])
# Grid = NewType('Grid', dict[Pos, str])


def window2(iterable):
    it = iter(iterable)
    last = next(it)
    for current in it:
        yield last, current
        last = current



def sort_points_clockwise(points):
    """
    Sort a list of points (x, y) in clockwise order.

    Args:
        points (list of tuples): List of (x, y) coordinates.

    Returns:
        list of tuples: Sorted list of points in clockwise order.
    """
    # Calculate the centroid as the center point
    center_x = sum(x for x, y in points) / len(points)
    center_y = sum(y for x, y in points) / len(points)

    # Define a function to calculate the angle
    def angle_from_center(point):
        x, y = point
        return math.atan2(y - center_y, x - center_x)

    # Sort points by angle in descending order for clockwise order
    sorted_points = sorted(points, key=angle_from_center, reverse=True)
    return sorted_points


class Side(IntEnum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

    def opposite(self):
        return Side((self + 2) % 4)
    
    @staticmethod
    def horizontal_sides():
        yield Side.TOP
        yield Side.BOTTOM

    @staticmethod
    def vertical_sides():
        yield Side.RIGHT
        yield Side.LEFT


@dataclass
class Region:
    name : str
    plots : set[Pos]
    edges : set[tuple[Pos, Pos, Side]]
    sides : set[tuple[Pos, Pos]]

    def __init__(self, name: str):
        self.name = name    
        self.plots = set()
        self.edges = set()
        self.sides = set()


    # def add_to_boundaries(pos: Pos):

    def add_plot(self, pos: Pos):
        x, y = pos
        self.plots.add(pos)
        self.add_edges(pos)


    def add_edges(self, pos: Pos):
        x, y = pos

        edges = (
            ((x, y), (x + 1, y), Side.TOP),
            ((x + 1, y), (x + 1, y + 1), Side.RIGHT),
            ((x, y + 1), (x + 1, y + 1), Side.BOTTOM),
            ((x, y), (x, y + 1), Side.LEFT)
        )

        for edge in edges:
            start, end, side = edge

            if (start, end, side.opposite()) in self.edges:
                self.edges.remove((start, end, side.opposite()))
            else:
                self.edges.add(edge)


    def area(self) -> int:
        return len(self.plots)
    

    def perimeter(self) -> int:
        return len(self.edges)


    def cost(self) -> int:
        return self.area() * self.perimeter()


    def __merge_edges(self) -> set[tuple[Pos, Pos]]:
        merged = set()


        horizontal = {}
        for s in Side.horizontal_sides():
            horizontal[s] = []

        vertical = {}
        for s in Side.vertical_sides():
            vertical[s] = []

        for edge in self.edges:
            (x1, y1), (x2, y2), side = edge

            if x1 == x2:
                vertical[side].append(edge)
            elif y1 == y2:
                horizontal[side].append(edge)
            else:
                raise ValueError("Invalid edge")





        for s in Side.horizontal_sides():
            horizontal[s].sort(key=lambda edge: edge[0])


        horizontal_by_y = {}
        for s in Side.horizontal_sides():
            horizontal_by_y[s] = {}

        for s in Side.horizontal_sides():
            for edge in horizontal[s]:
                (x1, y1), (x2, y2), side = edge
                assert side == s
                assert y1 == y2
                if y1 not in horizontal_by_y[s]:
                    horizontal_by_y[s][y1] = []
                horizontal_by_y[s][y1].append(edge)


        for s in Side.horizontal_sides():
            for y in horizontal_by_y[s]:
                edges_at_same_y = horizontal_by_y[s][y]

                current = edges_at_same_y[0]

                for idx in range(1, len(edges_at_same_y)):
                    next = edges_at_same_y[idx]
                    (x1, y1), (x2, y2), side_current = current
                    (x3, y3), (x4, y4), side_next = next

                    assert y1 == y2 == y3 == y4
                    assert side_current == side_next == s

                    if x2 == x3:
                        current = ((x1, y1), (x4, y1), side_current)
                    else:
                        merged.add(current)
                        current = next
                merged.add(current)


        for s in Side.vertical_sides():
            vertical[s].sort(key=lambda edge: edge[1])

        vertical_by_x = {}
        for s in Side.vertical_sides():
            vertical_by_x[s] = {}

        for s in Side.vertical_sides():
            for edge in vertical[s]:
                (x1, y1), (x2, y2), side = edge
                assert x1 == x2
                assert side == s
                if x1 not in vertical_by_x[s]:
                    vertical_by_x[s][x1] = []
                vertical_by_x[s][x1].append(edge)

        for s in Side.vertical_sides():        
            for x in vertical_by_x[s]:
                edges_at_same_x = vertical_by_x[s][x]

                current = edges_at_same_x[0]
                for idx in range(1, len(edges_at_same_x)):
                    next = edges_at_same_x[idx]
                    (x1, y1), (x2, y2), current_side = current
                    (x3, y3), (x4, y4), next_side = next

                    assert x1 == x2 == x3 == x4
                    assert current_side == next_side == s

                    if y2 == y3:
                        current = ((x1, y1), (x1, y4), current_side)
                    else:
                        merged.add(current)
                        current = next
                merged.add(current)


        return merged


    def sides_count(self) -> int:
        if self.sides == set():
            self.sides = self.__merge_edges()
        return len(self.sides)


    def side_cost(self) -> int:
        return self.sides_count() * self.area()



def read_data(filename: str) -> tuple[dict[Pos, str], int]:
    grid = {}
    grid_size: int = 0

    with open(filename, "r") as input_file:
        for y, line in enumerate(input_file.readlines()):
            grid_size += 1
            for x, c in enumerate(line.strip()):
                grid[(x, y)] = c
    return grid, grid_size


def four_neighbors(pos: Pos) -> Generator[Pos, None, None]:
    x, y = pos
    yield (x - 1, y)
    yield (x, y - 1)
    yield (x + 1, y)
    yield (x, y + 1)


def flood_region(region_id: str, pos: Pos, grid: Grid, grid_size: int) -> set[Pos]:
    visited_cells = set()

    stack = [ pos ]
    while stack:
        pos = stack.pop()

        if pos in visited_cells:
            continue

        visited_cells.add(pos)
        grid[pos] = '.'

        for neighbor in four_neighbors(pos):
            if grid.get(neighbor, None) == region_id:
                stack.append(neighbor)

    return visited_cells


def find_regions(grid: Grid, grid_size: int) -> list[Region]:
    regions = []

    for pos in grid:        
        region_id = grid[pos]

        if region_id == '.':
            continue

        cells = flood_region(region_id, pos, grid, grid_size)
        r = Region(region_id)
        for cell in cells:
            r.add_plot(cell)

        regions.append(r)

    return regions



def part1(filename: str) -> int:
    grid, grid_size = read_data(filename)
    regions = find_regions(grid, grid_size)

    return sum(( region.cost() for region in regions ))

def part2(filename: str) -> int:
    grid, grid_size = read_data(filename)
    regions = find_regions(grid, grid_size)

    return sum(( region.side_cost() for region in regions ))


# ic.disable()

assert ic(part1('./sample.txt')) == 140
assert ic(part1('./sample3.txt')) == 1930
assert ic(part1('./input.txt')) == 1424472


assert ic(part2('./sample.txt')) == 80
assert ic(part2('./sample2.txt')) == 436
assert ic(part2('./sample4.txt')) == 236
assert ic(part2('./sample5.txt')) == 368
assert ic(part2('./sample3.txt')) == 1206
assert ic(part2('./input.txt')) == 870202


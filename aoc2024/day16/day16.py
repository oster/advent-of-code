import heapq
from typing import Generator
from icecream import ic
from enum import IntEnum
from collections import defaultdict, deque

# from typing import NewType

type Grid = dict[Pos, str]
type Pos = tuple[int, int]

# Pos = NewType('Pos', tuple[int, int])
# Grid = NewType('Grid', dict[Pos, str])


def die(msg: str):
    raise Exception(msg)


class Direction(IntEnum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3
    EXIT = 666

    def right(self):
        return Direction((self + 1) % 4)

    def left(self):
        return Direction((self - 1) % 4)

    def as_str(self):
        return {
            Direction.EAST: ">",
            Direction.SOUTH: "v",
            Direction.WEST: "<",
            Direction.NORTH: "^",
        }[self]


def one_step(pos: Pos, dir: Direction) -> Pos:
    x, y = pos
    match dir:
        case Direction.EAST:
            return (x + 1, y)
        case Direction.SOUTH:
            return (x, y + 1)
        case Direction.WEST:
            return (x - 1, y)
        case Direction.NORTH:
            return (x, y - 1)
    return (x, y)


SYMBOL_TO_DIRECTION = {
    ">": Direction.EAST,
    "v": Direction.SOUTH,
    "<": Direction.WEST,
    "^": Direction.NORTH,
}


def read_data(filename: str) -> tuple[Grid, Pos, Pos]:
    grid = {}
    with open(filename, "r") as input_file:
        for y, line in enumerate(input_file.readlines()):
            for x, c in enumerate(line.strip()):
                if c == "#":
                    grid[x, y] = c
                elif c == "S":
                    start = (x, y)
                    pass
                elif c == "E":
                    end = (x, y)
                elif c == ".":
                    pass
                else:
                    die(f"invalid character {c}")

    return grid, start, end


def print_grid(grid: Grid, start: Pos, end: Pos) -> None:
    min_x = min([x for x, _ in grid.keys()])
    max_x = max([x for x, _ in grid.keys()])
    min_y = min([y for _, y in grid.keys()])
    max_y = max([y for _, y in grid.keys()])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if start == (x, y):
                print("S", end="")
            elif end == (x, y):
                print("E", end="")
            else:
                print(grid.get((x, y), "."), end="")
        print()


def print_path(grid: Grid, path: list[Pos]) -> None:
    min_x = min([x for x, _ in grid.keys()])
    max_x = max([x for x, _ in grid.keys()])
    min_y = min([y for _, y in grid.keys()])
    max_y = max([y for _, y in grid.keys()])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in path:
                print("o", end="")
            else:
                print(grid.get((x, y), "."), end="")
        print()


def compute_min_path(
    grid: Grid, start: Pos, start_dir: Direction, end: Pos
) -> tuple[int, dict[tuple[Pos, Direction, int], set[tuple[Pos, Direction, int]]]]:

    def is_valid(pos: Pos) -> bool:
        return pos not in grid or grid[pos] != "#"

    def is_end(pos: Pos) -> bool:
        return pos == end

    def neighbors(
        pos: Pos, dir: Direction
    ) -> Generator[tuple[int, tuple[Pos, Direction]], None, None]:
        for new_dir in [dir.left(), dir, dir.right()]:
            new_pos = one_step(pos, new_dir)
            if is_valid(new_pos):
                yield (1 if new_dir == dir else 1001, (new_pos, new_dir))

    cost_so_far = {}
    cost_so_far[(start, Direction.EAST)] = 0
    came_from = defaultdict(set)

    queue = [(0, (start, start_dir))]
    # heapq.heappush(queue, ))

    while queue:
        cost_until_there, (pos, dir) = heapq.heappop(queue)

        if is_end(pos):
            break

        best_cost_for_pos = cost_so_far[(pos, dir)]

        if (pos, dir) in cost_so_far:
            if cost_until_there > best_cost_for_pos:
                continue

        for cost, new_state in neighbors(pos, dir):
            new_cost = best_cost_for_pos + cost
            if new_state not in cost_so_far or new_cost <= cost_so_far[new_state]:
                cost_so_far[new_state] = new_cost
                new_pos, new_dir = new_state
                came_from[new_pos, new_dir, new_cost].add(
                    (pos, dir, best_cost_for_pos)
                )
                heapq.heappush(queue, (new_cost, new_state))

    min_cost = [cost for ((pos, _), cost) in cost_so_far.items() if pos == end].pop()

    return min_cost, came_from


def print_places(grid: Grid, places: set[Pos]) -> None:
    min_x = min([x for x, _ in grid.keys()])
    max_x = max([x for x, _ in grid.keys()])
    min_y = min([y for _, y in grid.keys()])
    max_y = max([y for _, y in grid.keys()])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in places:
                print("o", end="")
            else:
                print(grid.get((x, y), "."), end="")
        print()


def part1(filename: str) -> int:
    grid, start, end = read_data(filename)
    start_dir = Direction.EAST
    cost, _ = compute_min_path(grid, start, start_dir, end)
    return cost


def part2(filename: str) -> int:
    grid, start, end = read_data(filename)
    start_dir = Direction.EAST
    min_cost, came_from = compute_min_path(grid, start, start_dir, end)

    visited_tiles: set[Pos] = set()


    states = deque()

    states.extend([
        (pos, dir, cost)
        for (pos, dir, cost) in came_from
        if pos == end # and cost == min_cost
    ])

    while states:
        state = states.popleft()
        pos, _, _ = state
        visited_tiles.add(pos)
        for s in came_from[state]:
            states.append(s)

    return len(visited_tiles)


# ic.disable()

assert ic(part1("./sample.txt")) == 7036
assert ic(part1("./sample2.txt")) == 11048
assert ic(part1("./input.txt")) == 115500

assert ic(part2("./sample.txt")) == 45
assert ic(part2("./sample2.txt")) == 64
assert ic(part2("./input.txt")) == 679

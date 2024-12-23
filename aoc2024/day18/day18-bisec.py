import heapq
from typing import Generator
from icecream import ic
from collections import defaultdict

from typing import NewType

type Grid = dict[Pos, int]
type Pos = tuple[int, int]

# Pos = NewType("Pos", tuple[int, int])
# Grid = NewType("Grid", dict[Pos, str])


MAX_TIME = 16384


def read_data(filename: str) -> tuple[dict[Pos, int], int]:
    with open(filename, "r") as data_file:
        time = 1
        values = defaultdict(lambda: MAX_TIME)
        for x, y in (
            map(int, line.strip().split(",")) for line in data_file.readlines()
        ):
            values[(x, y)] = time
            time += 1

    return values, time


def print_grid(grid: Grid, start: Pos, end: Pos, time: int = MAX_TIME) -> None:
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
                if (x, y) in grid and grid[(x, y)] < time:
                    print("X", end="")
                else:
                    print(".", end="")
                # print(grid.get((x, y), "."), end="")
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


def find_shortest_path(
    start: Pos, end: Pos, grid: Grid, grid_size: int, until_time: int
) -> tuple[int, list[Pos]]:

    def in_bounds(pos: Pos) -> bool:
        return pos[0] >= 0 and pos[0] < grid_size and pos[1] >= 0 and pos[1] < grid_size

    def is_valid(pos: Pos) -> bool:
        return in_bounds(pos) and grid[pos] > until_time

    def is_end(pos: Pos) -> bool:
        return pos == end

    def four_neighbors(pos: Pos) -> Generator[Pos, None, None]:
        x, y = pos
        return (
            pos
            for pos in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
            if is_valid(pos)
        )

    def build_path(came_from: dict, end: Pos, start: Pos) -> list[Pos]:
        path = [end]
        current = end
        while current != start:
            current = came_from[current]
            path.append(current)
        path.append(start)
        path.reverse()
        return path

    cost_so_far = {}
    cost_so_far[(start)] = 0
    came_from = {}

    queue = [(0, (start))]
    # heapq.heappush(queue, ))

    while queue:
        cost_until_there, pos = heapq.heappop(queue)

        if is_end(pos):
            return cost_until_there, build_path(came_from, end, start)

        best_cost_for_pos = cost_so_far[pos]

        if pos in cost_so_far:
            if cost_until_there > best_cost_for_pos:
                continue

        for new_state in four_neighbors(pos):
            new_cost = best_cost_for_pos + 1
            if new_state not in cost_so_far or new_cost < cost_so_far[new_state]:
                cost_so_far[new_state] = new_cost
                new_pos = new_state
                came_from[new_pos] = pos
                heapq.heappush(queue, (new_cost, new_state))

    return 1e9, []


def part1(filename: str, grid_size: int, at_time: int, end: Pos) -> int:
    grid, _ = read_data(filename)
    length, _ = find_shortest_path((0, 0), end, grid, grid_size, at_time)
    return length


from bisect import bisect

def part2(filename: str, grid_size: int, end: Pos) -> Pos:
    grid, max_time = read_data(filename)

    rock_at_time: dict[int, Pos] = {t: r for r, t in grid.items()}
    need_recompute = True
    path = []
    length = 0

    rock_at_time = list(rock_at_time.values())

    def path(at_time: int) -> int:
        len, _ = find_shortest_path((0, 0), end, grid, grid_size, at_time) 
        return len

    p = bisect(range(len(rock_at_time)), 1e9-1, key=path)
    return rock_at_time[p-1]

    # stop_time = -1
    # for time in range(1, max_time + 1):
    #     need_recompute = need_recompute or rock_at_time[time] in path
    #     if need_recompute:
    #         need_recompute = False
    #         length, path = find_shortest_path((0, 0), end, grid, grid_size, time)
    #         if length == 1e9:
    #             stop_time = time
    #             break
    # return rock_at_time[stop_time]


# ic.disable()

assert ic(part1("./sample.txt", 7, 12, (6, 6))) == 22
assert ic(part1("./input.txt", 71, 1024, (70, 70))) == 416

assert ic(part2("./sample.txt", 7, (6, 6))) == (6, 1)
assert ic(part2("./input.txt", 71, (70, 70))) == (50, 23)

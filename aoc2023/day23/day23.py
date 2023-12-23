from collections import deque
from typing import Any, Optional
from enum import Enum
import sys
from queue import PriorityQueue
from typing import Callable


class Direction(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


type Pos = tuple[int, int]


def read_input(filename: str) -> tuple[list[list[str]], Pos, Pos]:
    data = []
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            data.append(list(line.rstrip()))

    start = (data[0].index("."), 0)
    end = (data[-1].index("."), len(data) - 1)
    return data, start, end


def die(msg: str):
    raise Exception(msg)


def print_grid(grid: list[list[Any]]):
    for line in grid:
        for val in line:
            print(f"{val:1}", end="")
        print()
    print()


heading_char = [">", "v", "<", "^"]


def next_positions_part1(
    current: tuple[int, int, Direction], grid: list[list[int]]
) -> list[tuple[int, int, Direction]]:
    size = len(grid)
    x, y, heading = current

    next_pos = (
        (x, y + 1, Direction.SOUTH),
        (x + 1, y, Direction.EAST),
        (x - 1, y, Direction.WEST),
        (x, y - 1, Direction.NORTH),
    )
    next_pos = filter(
        lambda pos: pos[2].value != ((heading.value + 2) % 4), next_pos
    )  # cannot go back

    filtered = filter(
        lambda pos: (pos[0] >= 0 and pos[0] < size and pos[1] >= 0 and pos[1] < size)
        and (
            grid[pos[1]][pos[0]] == "."
            or (
                (pos[2] == Direction.NORTH and grid[pos[1]][pos[0]] == "^")
                or (pos[2] == Direction.SOUTH and grid[pos[1]][pos[0]] == "v")
                or (pos[2] == Direction.EAST and grid[pos[1]][pos[0]] == ">")
                or (pos[2] == Direction.WEST and grid[pos[1]][pos[0]] == "<")
            )
        ),
        next_pos,
    )

    return list(filtered)


def print_pos(pos: tuple[int, int, Direction]):
    if pos:
        (x, y, head) = pos
        print(f"({x},{y},{heading_char[head.value]})")
    else:
        print("()")


def print_path(path: list[tuple[int, int, Direction]], grid: list[list[str]]):
    size = len(grid)
    g = [[grid[y][x] for x in range(size)] for y in range(size)]
    for step in path:
        x, y, _ = step
        g[y][x] = "O"

    print_grid(g)


def build_path_back(src, dst, from_to):
    # reconstruct path
    path = []
    c = src
    while c != dst:
        path.append(c)
        c = from_to[c]
    return list(reversed(path))


def search(
    start: tuple[int, int, Direction],
    end: Pos,
    grid: list[list[str]],
    all_next_positions: Callable,
) -> Optional[tuple[list, int]]:
    end_x, end_y = end

    all_path = []

    cost_to = {}  # pos -> cost to arrive at
    from_to = {}  # pos_dst -> pos_src

    states = PriorityQueue()

    states.put((0, start))
    from_to[start] = start
    cost_to[start] = 0

    while True:
        if states.empty():
            break
            return None

        _, current_tmp = states.get()
        current_x, current_y, current_heading_int = current_tmp
        current = (current_x, current_y, Direction(current_heading_int))

        if current_x == end_x and current_y == end_y:
            all_path.append(build_path_back(current, start, from_to))
            continue

        # print_path(build_path_back(current, start, from_to), grid)
        # input()

        for next_pos in all_next_positions(current, grid):
            cost_to_next = -1
            new_cost = cost_to[current] + cost_to_next  # cost(current, next_pos, grid)

            if next_pos not in cost_to or new_cost < cost_to[next_pos]:
                cost_to[next_pos] = new_cost
                next_pos_x, next_pos_y, next_pos_heading = next_pos
                priority = -new_cost
                states.put((priority, (next_pos_x, next_pos_y, next_pos_heading.value)))
                from_to[next_pos] = current

    max_path = []
    max = 0
    for p in all_path:
        if len(p) > max:
            max = len(p)
            max_path = p
    return max_path, len(max_path)


def part1(filename: str) -> int:
    grid, start, end = read_input(filename)

    # print_path([], grid)

    _, dist = search((*start, Direction.SOUTH), end, grid, next_positions_part1)
    return dist


def get_interconnections(grid: list[list[str]]) -> list[Pos]:
    interconnections = []
    size = len(grid)
    for y in range(size):
        for x in range(size):
            if grid[y][x] != "#":
                voisins = [(x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)]
                valid_neighbors = filter(
                    lambda pos: pos[0] >= 0
                    and pos[0] < size
                    and pos[1] >= 0
                    and pos[1] < size,
                    voisins,
                )
                exit = 0
                for nx, ny in valid_neighbors:
                    if grid[ny][nx] != "#":
                        exit += 1
                if exit > 2:
                    interconnections.append((x, y))
    return interconnections


def get_connections(
    node: Pos, start: Pos, end: Pos, grid: list[list[str]], interconnections: list[Pos]
) -> list[tuple[Pos, int]]:
    states = deque()
    connections = []

    visited = set()
    node_X, node_Y = node
    states.append(((node_X, node_Y), 0))

    def neighbors(
        x: int, y: int, grid: list[list[str]], visited: set[Pos]
    ) -> list[Pos]:
        size = len(grid)
        next_pos = ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1))
        filtered = filter(
            lambda pos: (
                pos[0] >= 0 and pos[0] < size and pos[1] >= 0 and pos[1] < size
            )
            and (grid[pos[1]][pos[0]] != "#"),
            next_pos,
        )
        return list(filtered)

    while states:
        pos, dist = states.popleft()
        if pos in visited:
            continue
        else:
            visited.add(pos)

        x, y = pos
        for n in neighbors(x, y, grid, visited):
            if n == node:
                continue

            if n == start:
                connections.append((start, dist + 1))
                continue
            if n == end:
                connections.append((end, dist + 1))
                continue

            if n in interconnections:
                connections.append((n, dist + 1))
                continue

            states.append((n, dist + 1))

    return connections


def dump_connection_as_dot(
    graph: dict[Pos, list[tuple[Pos, int]]], start: Pos, end: Pos, grid: list[list[str]]
):
    # TODO: dump will motify the graph (to remove double edges), should be fixed one day

    with open("graph.dot", "w") as output_file:
        output_file.write("graph G {" + "\n")
        # output_file.write('digraph G {'+'\n')
        # output_file.write('  rankdir=LR;'+'\n')
        # output_file.write('  node [shape=record];'+'\n')

        output_file.write(
            f'  "{start}" [style=filled,fillcolor=green,shape=doublecircle,label="start"];'
            + "\n"
        )
        output_file.write(
            f'  "{end}" [style=filled,fillcolor=red,shape=doublecircle,label="end"];'
            + "\n"
        )

        for node in graph:
            output_file.write(f'  "{node}" [label="{node}"];' + "\n")

        for node in graph:
            for connection, dist in graph[node]:
                output_file.write(
                    f'  "{node}" -- "{connection}" [label={dist}];' + "\n"
                )

                if connection in graph:
                    for conn in graph[connection]:
                        if conn[0] == node:
                            graph[connection].remove(conn)
                            break

        output_file.write("}" + "\n")


def longest_path(start: Pos, end: Pos, graph: dict[Pos, list[tuple[Pos, int]]]):
    visited = set()
    distances = {node: 0 for node in graph.keys()}
    distances[start] = 0

    def longest_path_brute_force(
        current: Pos,
        sum_dist: int,
        all_nodes: dict[Pos, list[tuple[Pos, int]]],
        distances: dict[Pos, int],
    ):
        if current in visited:
            return
        visited.add(current)

        if distances[current] < sum_dist:
            distances[current] = sum_dist

        for other_node, dist in all_nodes[current]:
            longest_path_brute_force(other_node, sum_dist + dist, all_nodes, distances)

        visited.remove(current)

    longest_path_brute_force(start, 0, graph, distances)

    return distances[end]


def part2(filename: str) -> int:
    grid, start, end = read_input(filename)

    interconnections = get_interconnections(grid)
    graph = {}

    graph[start] = get_connections(start, start, end, grid, interconnections)
    graph[end] = get_connections(end, start, end, grid, interconnections)

    for node in interconnections:
        graph[node] = get_connections(node, start, end, grid, interconnections)

    # dump_connection_as_dot(graph, start, end, grid)

    max_dist = longest_path(start, end, graph)
    return max_dist


assert part1("./sample.txt") == 94
assert part1("./input.txt") == 2414

assert part2("./sample.txt") == 154
assert part2("./input.txt") == 6598

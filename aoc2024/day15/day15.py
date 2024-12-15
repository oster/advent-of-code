from icecream import ic
from enum import IntEnum

type Grid = dict[Pos, str]
type Pos = tuple[int, int]


def die(msg: str):
    raise Exception(msg)


class Direction(IntEnum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def next_pos(self, pos: Pos) -> Pos:
        x, y = pos
        match self:
            case Direction.UP:
                return (x, y - 1)
            case Direction.DOWN:
                return (x, y + 1)
            case Direction.LEFT:
                return (x - 1, y)
            case Direction.RIGHT:
                return (x + 1, y)
            case _:
                die("invalid direction")

    def is_horizontal(self) -> bool:
        return self == Direction.LEFT or self == Direction.RIGHT

    def is_vertical(self) -> bool:
        return self == Direction.UP or self == Direction.DOWN

    @classmethod
    def from_char(cls, c: str) -> "Direction":
        match c:
            case "^":
                return Direction.UP
            case "v":
                return Direction.DOWN
            case "<":
                return Direction.LEFT
            case ">":
                return Direction.RIGHT
            case _:
                die("invalid direction")


def read_data(filename: str) -> tuple[Pos, Grid, list[Direction]]:
    with open(filename, "r") as data_file:
        grid = {}
        all = data_file.read()
        g, ins = all.split("\n\n")

        for y, line in enumerate(g.split("\n")):
            for x, char in enumerate(line.strip()):
                if char == ".":
                    continue
                if char == "@":
                    start = (x, y)
                else:
                    grid[(x, y)] = char

        movements = [ Direction.from_char(c) for c in ins if c != "\n"]

        return start, grid, movements


def print_grid(grid: Grid, robot: Pos):
    min_x = min([x for x, _ in grid.keys()])
    max_x = max([x for x, _ in grid.keys()])
    min_y = min([y for _, y in grid.keys()])
    max_y = max([y for _, y in grid.keys()])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if robot == (x, y):
                print("@", end="")
            else:
                print(grid.get((x, y), "."), end="")
        print()


def move(pos: Pos, direction: Direction, grid: Grid) -> tuple[bool, Pos]:
    x, y = pos
    symbol = grid.get((x, y), None)

    match symbol:
        case None:
            return True, pos
        case "#":
            return False, pos
        case "O" | "@":
            new_pos = direction.next_pos(pos)
            ok, _ = move(new_pos, direction, grid)
            if not ok:
                return False, pos
            else:
                del grid[(x, y)]
                grid[new_pos] = symbol
                return True, new_pos
        case _:
            die("invalid symbol")


def part1(filename: str) -> int:
    start, grid, movements = read_data(filename)
    current = start

    for direction in movements:
        grid[current] = "@"
        can_move, new_pos = move(current, direction, grid)
        if can_move:
            current = new_pos

    return sum((y * 100) + x for (x, y), c in grid.items() if c == "O")


def scale_up(grid: Grid) -> Grid:
    new_grid = {}

    for (x, y), c in grid.items():
        match c:
            case "#":
                new_grid[(2 * x, y)] = c
                new_grid[(2 * x + 1, y)] = c
            case "O":
                new_grid[(2 * x, y)] = "["
                new_grid[(2 * x + 1, y)] = "]"
            case _:
                pass

    return new_grid


def can_move(pos: Pos, direction: Direction, grid: Grid) -> bool:
    symbol = grid.get(pos, None)

    match symbol:
        case None:
            return True
        case "#":
            return False

    new_pos = direction.next_pos(pos)

    if direction.is_horizontal():
        if symbol == "[" or symbol == "]" or symbol == "@":
            return can_move(new_pos, direction, grid)
        else:
            die("invalid symbol")

    nx, ny = new_pos
    match symbol:
        case "@":
            return can_move(new_pos, direction, grid)
        case "[":
            return can_move(new_pos, direction, grid) and can_move(
                (nx + 1, ny), direction, grid
            )
        case "]":
            return can_move(new_pos, direction, grid) and can_move(
                (nx - 1, ny), direction, grid
            )
        case _:
            die("invalid symbol")


def collect_to_push_dfs(pos: Pos, dy: int, grid: Grid, to_push: set[Pos]):
    x, y = pos

    to_push.add(pos)

    nx, ny = x, y + dy

    match grid.get((nx, ny), None):
        case None:
            return
        case "#":
            die("something went wrong")
        case "@":
            to_push.add((nx, ny))
        case "[":
            # assert grid[(nx + 1, ny)] == ']'
            to_push.add((nx, ny))
            collect_to_push_dfs((nx, ny), dy, grid, to_push)
            to_push.add((nx + 1, ny))
            collect_to_push_dfs((nx + 1, ny), dy, grid, to_push)
        case "]":
            # assert grid[(nx - 1, ny)] == '['
            to_push.add((nx - 1, ny))
            collect_to_push_dfs((nx - 1, ny), dy, grid, to_push)
            to_push.add((nx, ny))
            collect_to_push_dfs((nx, ny), dy, grid, to_push)


def move_for_part2(pos: Pos, direction: Direction, grid: Grid) -> Pos:
    x, y = pos

    if direction.is_horizontal():
        dx = +1 if direction == Direction.RIGHT else -1

        to_push = set()
        nx = x
        while (nx, y) in grid:
            to_push.add((nx, y))
            nx += dx

        for px, py in sorted(
            to_push, key=lambda p: p[0], reverse=(direction == Direction.RIGHT)
        ):
            if (px, py) in grid:
                grid[(px + dx, py)] = grid[(px, py)]
                del grid[(px, py)]

    else:
        dy = +1 if direction == Direction.DOWN else -1

        to_push = set()
        collect_to_push_dfs((x, y), dy, grid, to_push)

        for px, py in sorted(
            to_push, key=lambda p: p[1], reverse=(direction == Direction.DOWN)
        ):
            if (px, py) in grid:
                grid[(px, py + dy)] = grid[(px, py)]
                del grid[(px, py)]

    return direction.next_pos(pos)


def part2(filename: str) -> int:
    start, grid, movements = read_data(filename)
    grid = scale_up(grid)
    start: Pos = (2 * start[0], start[1])

    current = start
    for direction in movements:
        grid[current] = "@"
        if can_move(current, direction, grid):
            current = move_for_part2(current, direction, grid)

    return sum((y * 100) + x for (x, y), c in grid.items() if c == "[")


# ic.disable()

assert ic(part1("./sample.txt")) == 10092
assert ic(part1("./input.txt")) == 1490942

assert ic(part2("./sample.txt")) == 9021
assert ic(part2("./input.txt")) == 1519202

from collections import deque
from typing import Any, Optional
from enum import Enum
import sys
from queue import PriorityQueue
import heapq
from typing import Callable

class Direction(Enum):
    EAST=0
    SOUTH=1
    WEST=2
    NORTH=3


def read_input(filename: str) -> list[list[int]]:
    data = []
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            data.append(list(map(int, list(line.rstrip()))))
    return data


def die(msg: str):
    raise Exception(msg)


def print_grid(grid: list[list[Any]]):
    for line in grid:
        for val in line:
            print(f"{val:2}", end="")
        print()
    print()


heading_char = [ '>', 'v', '<', '^' ]


def next_positions(current : tuple[int, int, Direction], grid : list[list[int]], min_step: int, max_step:int) -> list[tuple[tuple[int, int, Direction], int]]:
    size = len(grid)
    x, y, head = current

    if x == size - 1 and y == size -1:
        return []

    positions = []
    match head:        
        case Direction.EAST | Direction.WEST:
            cost = 0
            for i in range(1, min_step):
                if y-i >= 0:
                    cost += grid[y-i][x]
            for shift in range(min_step, max_step+1):
                if y-shift >= 0:
                    cost += grid[y-shift][x]
                    positions.append(((x, y-shift, Direction.NORTH), cost))
            cost = 0
            for i in range(1, min_step):
                if y+i < size:
                    cost += grid[y+i][x]
            for shift in range(min_step, max_step+1):
                if y+shift < size:
                    cost += grid[y+shift][x]
                    positions.append(((x, y+shift, Direction.SOUTH), cost))

        case Direction.NORTH | Direction.SOUTH:
            cost = 0
            for i in range(1, min_step):
                if x-i >= 0:
                    cost += grid[y][x-i]
            for shift in range(min_step, max_step+1):
                if x-shift >= 0:
                    cost += grid[y][x-shift]
                    positions.append(((x-shift, y, Direction.WEST), cost))

            cost = 0
            for i in range(1, min_step):
                if x+i < size:
                    cost += grid[y][x+i]
            for shift in range(min_step, max_step+1):
                if x+shift < size:
                    cost += grid[y][x+shift]
                    positions.append(((x+shift, y, Direction.EAST), cost))        
        case _:
                die("Invalid heading.")    

    return positions


def next_positions_part1(current : tuple[int, int, Direction], grid : list[list[int]]) -> list[tuple[tuple[int, int, Direction], int]]:
    return next_positions(current, grid, 1, 3)



def print_pos(pos: tuple[int, int, Direction]):
    if pos:
        (x, y, head) = pos
        print(f'({x},{y},{heading_char[head.value]})')
    else:
        print('()')



def print_path(path: list[tuple[int,int]], grid: list[list[int]]):
    size = len(grid)
    g = [ [ '.' for _ in range(size) ] for _ in range(size) ]
    for (x,y) in path:
        g[y][x] = '#'

    print_grid(g)


def manhattan(a: tuple[int, int], b: tuple[int, int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def search(start: tuple[int, int, Direction], end: tuple[int, int], grid: list[list[int]], all_next_positions: Callable[[tuple[int, int, Direction], list[list[int]]], list[tuple[tuple[int, int, Direction], int]]]) -> Optional[tuple[list, int]]:
    end_x, end_y = end

    cost_to = {} # pos -> cost to arrive at
    from_to = {} # pos_dst -> pos_src 

    states = [(0, start)]

    from_to[start] = start
    cost_to[start] = 0

    while True:
        if not states:
            return None
        
        _, current_tmp  = heapq.heappop(states)
        current_x, current_y, current_heading_int = current_tmp
        current = (current_x, current_y, Direction(current_heading_int))
        # print(f'current: {current}')
        
        if current_x == end_x and current_y == end_y:
            # reconstruct path
            path = []
            c = current
            # print(f'stop at current: {current} whose cost = {cost_to[current]}')
            while c != start:
                path.append(c)
                c = from_to[c]
            return (list(reversed(path)), cost_to[current])

        for next_pos, cost_to_next in all_next_positions(current, grid):
            new_cost = cost_to[current] + cost_to_next # cost(current, next_pos, grid) 
            if next_pos not in cost_to or new_cost < cost_to[next_pos]:
                cost_to[next_pos] = new_cost
                # print(f'cost from {current} to {next_pos} = {new_cost}')

                next_pos_x, next_pos_y, next_pos_heading = next_pos


                priority = new_cost  + 2*manhattan((next_pos_x, next_pos_y), end)
                heapq.heappush(states, (priority, (next_pos_x, next_pos_y, next_pos_heading.value)))


                from_to[next_pos] = current


def part1(filename: str) -> int:
    grid = read_input(filename)
    size = len(grid)

    path_a, cost_a = search((0,0, Direction.EAST), (size-1,size-1), grid, next_positions_part1)
    path_b, cost_b = search((0,0, Direction.SOUTH), (size-1,size-1), grid, next_positions_part1)

    return min(cost_a, cost_b)


assert part1("./sample.txt") == 102, f"Expected 102, got {part1('./sample.txt')}"
assert part1("./input.txt") == 855


def next_positions_part2(current : tuple[int, int, Direction], grid : list[list[int]]) -> list[tuple[tuple[int, int, Direction], int]]:
    return next_positions(current, grid, 4, 10)


def part2(filename: str) -> int:
    grid = read_input(filename)
    size = len(grid)

    path_a, cost_a = search((0,0, Direction.EAST), (size-1,size-1), grid, next_positions_part2)
    path_b, cost_b = search((0,0, Direction.SOUTH), (size-1,size-1), grid, next_positions_part2)

    return min(cost_a, cost_b)

assert part2("./sample.txt") == 94
assert part2("./input.txt") == 980

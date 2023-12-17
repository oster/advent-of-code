from collections import deque
from typing import Any, Optional
from enum import Enum
import sys
from queue import PriorityQueue
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


def next_positions_part1(current : tuple[int, int, Direction], grid : list[list[int]]) -> list[tuple[tuple[int, int, Direction], int]]:
    size = len(grid)
    x, y, head = current

    if x == size - 1 and y == size -1:
        return []

    positions = []
    match head:        
        case Direction.EAST | Direction.WEST:
            cost = 0
            for shift in range(1, 4):
                if y-shift >= 0:
                    cost += grid[y-shift][x]
                    positions.append(((x, y-shift, Direction.NORTH), cost))
            cost = 0
            for shift in range(1, 4):
                if y+shift < size:
                    cost += grid[y+shift][x]
                    positions.append(((x, y+shift, Direction.SOUTH), cost))

        case Direction.NORTH | Direction.SOUTH:
            cost = 0
            for shift in range(1, 4):
                if x-shift >= 0:
                    cost += grid[y][x-shift]
                    positions.append(((x-shift, y, Direction.WEST), cost))
            cost = 0
            for shift in range(1, 4):
                if x+shift < size:
                    cost += grid[y][x+shift]
                    positions.append(((x+shift, y, Direction.EAST), cost))        
        case _:
                die("Invalid heading.")    

    return positions


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


def path_cost(path : list[tuple[tuple[int,int,Direction],int]]):
    s = 0
    for (_, dist) in path:
        s += dist
    return s

distances = {}


# does not work ;(
def min_path(pos : tuple[int, int, Direction], grid: list[list[int]], visited: list[tuple[int, int]]) -> tuple[Optional[int], list[tuple[tuple[int,int,Direction],int]]]:
    size = len(grid)

    if pos in distances:
        return distances[pos]

    x, y, _ = pos
    current = (x,y)
    if current in visited:
        # cycle
        return None, []


    if x == size - 1 and y == size - 1:
        return 0, []

    minimum = sys.maxsize
    best_path = []

    visited.append(current)
    nexts = next_positions_part1(pos, grid)
    # print(f"nexts({pos}): {nexts}")
    if nexts == []:
        minimum = None
    else:
        for (next_pos, cost) in sorted(nexts, key=lambda p:  abs(p[0][0]-(size-1))+abs(p[0][1]-(size-1)), reverse=True):
            dist, path = min_path(next_pos, grid, visited)
            if dist != None:
                k = cost + dist
                if k < minimum:
                    minimum = k
                    best_path = [ (next_pos, cost) ] + path

    visited.pop()

    # if minimum != None:
    distances[pos] = minimum, best_path
    return minimum, best_path


def compute_part1(grid : list[list[int]]) -> int:
    global distances
    distances = {}

    a, path_a = min_path((0,0, Direction.EAST), grid, list())
    print(f'a: {a}')
    print(f'path_a: {path_a}')

    assert path_cost(path_a) == a

    b, path_b = min_path((0,0, Direction.SOUTH), grid, list())
    print(f'b: {b}')    
    print(f'path_b: {path_b}')

    assert path_cost(path_b) == b

    m = min(a, b)
    print(f'min: {m}')

    return m
    


def manhattan(a: tuple[int, int], b: tuple[int, int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def cost(src: tuple[int,int, Direction], dst: tuple[int,int, Direction], grid: list[list[int]]) -> int:
    x1, y1, heading1 = src
    x2, y2, heading2 = dst
    res = 0
    if x1 == x2:
        if y1 < y2:
            for y in range(y1+1, y2+1):
                res += grid[y][x1]
        elif y1 > y2:
            for y in range(y1-1, y2-1, -1):
                res += grid[y][x1]
        else:
            return res
	
    if y1 == y2:
        if x1 < x2:
            for x in range(x1 + 1,x2+1):
                res += grid[y1][x]
        elif x1 > x2:
            for x in range(x1 - 1, x2-1, -1):
                res += grid[y1][x]
        else:
            return res

    return res


def search(start: tuple[int, int, Direction], end: tuple[int, int], grid: list[list[int]], all_next_positions: Callable[[tuple[int, int, Direction], list[list[int]]], list[tuple[tuple[int, int, Direction], int]]]) -> Optional[tuple[list, int]]:
    end_x, end_y = end

    cost_to = {} # pos -> cost to arrive at
    from_to = {} # pos_dst -> pos_src 

    states = PriorityQueue()

    states.put((0, start))
    from_to[start] = start
    cost_to[start] = 0

    while True:
        if states.empty():
            return None
        
        _, current_tmp  = states.get()
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

                priority = new_cost # + manhattan((next_pos_x, next_pos_y), end)
                states.put((priority, (next_pos_x, next_pos_y, next_pos_heading.value)))
                from_to[next_pos] = current



def part1(filename: str) -> int:
    grid = read_input(filename)
    size = len(grid)

    path_a, cost_a = search((0,0, Direction.EAST), (size-1,size-1), grid, next_positions_part1)
    path_b, cost_b = search((0,0, Direction.SOUTH), (size-1,size-1), grid, next_positions_part1)

    return min(cost_a, cost_b)


assert part1("./sample.txt") == 102
assert part1("./input.txt") == 855


def next_positions_part2(current : tuple[int, int, Direction], grid : list[list[int]]) -> list[tuple[tuple[int, int, Direction], int]]:
    size = len(grid)
    x, y, head = current

    if x == size - 1 and y == size -1:
        return []

    positions = []
    match head:        
        case Direction.EAST | Direction.WEST:
            cost = 0
            for i in range(1, 4):
                if y-i >= 0:
                    cost += grid[y-i][x]
            for shift in range(4, 11):
                if y-shift >= 0:
                    cost += grid[y-shift][x]
                    positions.append(((x, y-shift, Direction.NORTH), cost))
            cost = 0
            for i in range(1, 4):
                if y+i < size:
                    cost += grid[y+i][x]
            for shift in range(4, 11):
                if y+shift < size:
                    cost += grid[y+shift][x]
                    positions.append(((x, y+shift, Direction.SOUTH), cost))

        case Direction.NORTH | Direction.SOUTH:
            cost = 0
            for i in range(1, 4):
                if x-i >= 0:
                    cost += grid[y][x-i]
            for shift in range(4, 11):
                if x-shift >= 0:
                    cost += grid[y][x-shift]
                    positions.append(((x-shift, y, Direction.WEST), cost))

            cost = 0
            for i in range(1, 4):
                if x+i < size:
                    cost += grid[y][x+i]
            for shift in range(4, 11):
                if x+shift < size:
                    cost += grid[y][x+shift]
                    positions.append(((x+shift, y, Direction.EAST), cost))        
        case _:
                die("Invalid heading.")    

    return positions


def part2(filename: str) -> int:
    grid = read_input(filename)
    size = len(grid)

    path_a, cost_a = search((0,0, Direction.EAST), (size-1,size-1), grid, next_positions_part2)
    path_b, cost_b = search((0,0, Direction.SOUTH), (size-1,size-1), grid, next_positions_part2)

    return min(cost_a, cost_b)

assert part2("./sample.txt") == 94
assert part2("./input.txt") == 980

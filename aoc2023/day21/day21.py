from collections import deque
from typing import Any
import sys

def die(msg: str):
    raise Exception(msg)


def print_grid(grid: list[list[Any]]):
    for line in grid:
        for val in line:
            print(f"{val:2}", end="")
        print()
    print()


def read_input(filename: str) -> tuple[list[list[str]], tuple[int, int]]:
    data = []
    start = (0, 0)
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            row = list(line.rstrip())
            data.append(row)
            if "S" in row:
                start = (row.index("S"), len(data) - 1)

    return data, start


def neighbors(current: tuple[int, int], grid: list[list[str]]) -> set[tuple[int, int]]:
    size = len(grid)
    x, y = current

    next_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    next_positions = filter(
        lambda pos: pos[0] >= 0 and pos[0] < size and pos[1] >= 0 and pos[1] < size,
        next_positions,
    )
    next_positions = filter(lambda pos: grid[pos[1]][pos[0]] != "#", next_positions)

    return set(next_positions)


def part1(filename: str, max_step: int) -> int:
    grid, start = read_input(filename)

    states = deque()
    states.append((0, [start]))

    while states:
        step, nodes = states.popleft()

        if step >= max_step:
            return len(nodes)

        neighbors_for_step = set()
        for node in nodes:
            for n in neighbors(node, grid):
                neighbors_for_step.add(n)

        states.append((step + 1, neighbors_for_step))
    return -1


# assert part1("./sample.txt", 6) == 16
# assert part1("./input.txt", 64) == 3830


def neighbors_part2(current: tuple[int, int], grid: list[list[str]]) -> set[tuple[int, int]]:
    size = len(grid)
    x, y = current

    next_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    next_positions = filter(lambda pos: grid[(size+pos[1])%size][(size+pos[0])%size] != "#", next_positions)

    return set(next_positions)



def print_nodes_on_extended_grid(grid: list[list[Any]], nodes: set[tuple[int, int]]):
    size = len(grid)

    x_min = sys.maxsize
    x_max = 0
    y_min = sys.maxsize
    y_max = 0
    for node in nodes:
        x_min = min(x_min, node[0])
        x_max = max(x_max, node[0])
        y_min = min(y_min, node[1])
        y_max = max(y_max, node[1])

    left = (x_min // size)
    right = ((x_max+size) // size)
    up = (y_min // size)
    down = ((y_max+size) // size)

    line_width=((right-left)*size)+(right-left)+1

    for y in  range(left * size, (right)*size):
        if y % size == 0:
            print("-" * line_width)
        for x in range(up * size, (down)*size):
            if x % size == 0:
                print(f"|", end="")

            if (x, y) in nodes:
                print(f"O", end="")
            else:
                print(" ", end="")
        print('|')
    print('-' * line_width)



def part2(filename: str, looking_for_step: int, cycle_detection=False) -> int:
    grid, start = read_input(filename)

    states = deque()
    states.append((0, [start]))
    size=len(grid)

    old_n, old_δ, old_Δ = 0, 0, 0

    while states:
        step, nodes = states.popleft()

        # if step % size == 0:
        #     print_nodes_on_extended_grid(grid, nodes)            

        if cycle_detection:
            if step % size == looking_for_step % size:  # there is a kind of cycle in patterns every 'size' steps according to the printing 
                n = len(nodes)
                δ = n - old_n
                Δ = δ - old_δ
                print(f'step: {step:6}, δ: {δ:6}, Δ: {Δ:6}')

                if Δ == old_Δ:
                    print('cycle detected!')
                    k = (looking_for_step-step) // size
                    triangle_k = (k*(k+1))//2
                    res = n + k*δ+ triangle_k*Δ
                    print('count:', res)
                    return res

                old_n, old_δ, old_Δ  = n, δ, Δ
        else:
            if step == looking_for_step:
                return len(nodes)
            
        neighbors_for_step = set()
        for node in nodes:
            for neighbor in neighbors_part2(node, grid):
                neighbors_for_step.add(neighbor)

        states.append((step + 1, neighbors_for_step))
    return -1


# part2("./sample.txt", 11) # 63
# part2("./sample.txt", 22) # 261  δ=198
# part2("./sample.txt", 33) # 644  δ=383  Δ=185  
# part2("./sample.txt", 44) # 1196 δ=552  Δ=169
# part2("./sample.txt", 55) # 1914 δ=718  Δ=166
# part2("./sample.txt", 66) # 2794 δ=880  Δ=162
# part2("./sample.txt", 77) # 3836 δ=1042 Δ=162

# part2("./sample.txt", 88) # 5040
# part2("./sample.txt", 99) # 6406
# part2("./sample.txt", 110) # 7934
# part2("./sample.txt", 121) # 9624
# part2("./sample.txt", 132) # 11476
# part2("./sample.txt", 143) # 13490


assert part2("./sample.txt", 6) == 16
assert part2("./sample.txt", 10) == 50
assert part2("./sample.txt", 50) == 1594

assert part2("./sample.txt", 100, True) == 6536
assert part2("./sample.txt", 500, True) == 167004
assert part2("./sample.txt", 1000, True) == 668697
assert part2("./sample.txt", 5000, True) == 16733044

assert(part2("./input.txt", 26501365, True)) == 637087163925555

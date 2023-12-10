from typing import Generator

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()

def parse_input(filename : str) -> tuple[tuple[int, int], list[list[str]]]:
    input = read_input(filename)

    grid = []
    start = (-1, -1)

    for row_index, lines in enumerate(input) : 
        lines = lines.replace('|', '│')
        lines = lines.replace('-', '─')
        lines = lines.replace('F', '┌')
        lines = lines.replace('L', '└')
        lines = lines.replace('7', '┐')
        lines = lines.replace('J', '┘')

        row = list(lines)
        if 'S' in row:
            start = (row_index, row.index('S'))
        grid.append(list(lines))


    assert start != (-1, -1)

    return (start, grid)



def print_grid(grid : list[list[str]]) -> None:
    for row in grid:
        print(''.join(row))
    print()

def print_numbers(grid : list[list[int]]) -> None:
    for row in grid:
        for colum in row:
            if colum == -1:
                print('SS', end='')
            elif colum == 0:
                print('..', end='')
            else:
                print(f"{colum:02d}", end='')
        print()
    print()

def find_max(numbers : list[list[int]]) -> int:
    max = 0
    for row in numbers:
        for colum in row:
            if colum > max:
                max = colum
    return max  


def flood(y, x, step, h, w, g, n):
    if y < 0 or y >= h or x < 0 or x >= w:
        return
    if n[y][x] != 0 and n[y][x] <= step:
        return
    n[y][x] = step

    if g[y][x] == '│':
        flood(y+1, x, step+1, h, w, g, n)
        flood(y-1, x, step+1, h, w, g, n)
    elif g[y][x] == '─':
        flood(y, x+1, step+1, h, w, g, n)
        flood(y, x-1, step+1, h, w, g, n)
    elif g[y][x] == '┌':
        flood(y+1, x, step+1, h, w, g, n)
        flood(y, x+1, step+1, h, w, g, n)
    elif g[y][x] == '└':
        flood(y, x+1, step+1, h, w, g, n)
        flood(y-1, x, step+1, h, w, g, n)
    elif g[y][x] == '┐':
        flood(y, x-1, step+1, h, w, g, n)
        flood(y+1, x, step+1, h, w, g, n)
    elif g[y][x] == '┘':
        flood(y-1, x, step+1, h, w, g, n)
        flood(y, x-1, step+1, h, w, g, n)




def compute_main_loop(start, grid : list[list[str]]) -> list[list[int]]:
    height = len(grid)
    width = len(grid[0])
    numbers = [ [ 0 ] * width for _ in range(height) ]

    h = height
    w = width
    g = grid 
    n = numbers


    step = 0
    sy, sx = start

    numbers[sy][sx] = -1

    if g[sy][sx+1] == '─' or g[sy][sx+1] == '┐' or g[sy][sx+1] == '┘':
        flood(sy, sx+1, step + 1, h, w, g, n)

    if g[sy][sx-1] == '─' or g[sy][sx-1] == '┌' or g[sy][sx-1] == '└':
        flood(sy, sx-1, step + 1, h, w, g, n)


    if g[sy+1][sx] == '│' or g[sy+1][sx] == '┘' or g[sy+1][sx] == '└':
        flood(sy+1, sx, step + 1, h, w, g, n)

    if g[sy-1][sx] == '│' or g[sy-1][sx] == '┌' or g[sy-1][sx] == '┐':
        flood(sy+1, sx, step + 1, h, w, g, n)

    return numbers


def part1(filename : str) -> int:
    start, grid = parse_input(filename)
    numbers = compute_main_loop(start, grid)
    challenge = find_max(numbers)

    return challenge



def scale_up(grid : list[list[str]]) -> list[list[str]]:
    height = len(grid)
    width = len(grid[0])

    scaled_grid = []
    for row in grid:
        scaled_row = []

        scaled_row.append('.')
        for x in range(len(row)):
            scaled_row.append(row[x])
            if row[x] in ['S','┌', '─', '└'] and x+1 < width and row[x+1] in ['┐', '─', '┘', 'S']:
                scaled_row.append('─')
            else:
                scaled_row.append('.')
        scaled_grid.append(scaled_row)

    scaled_grid_2 = []
    scaled_grid_2.append(['.'] * ((width+1) * 2 - 1) )
    for y in range(len(scaled_grid)):
        scaled = []
        for x in range(len(scaled_grid[y])):
            if scaled_grid[y][x] in ['S', '┌', '│', '┐'] and y+1 < height and scaled_grid[y+1][x] in ['└', '│', '┘']:
                scaled.append('│')
            else:
                scaled.append('.')
        scaled_grid_2.append(scaled_grid[y])            
        scaled_grid_2.append(scaled)

    return scaled_grid_2


def scale_down(grid : list[list[str]]) -> list[list[str]]:
    height = len(grid)
    width = len(grid[0])

    scaled_grid = []
    for y in range(1, height, 2):
        scaled_row = []
        for x in range(1, width, 2):
            scaled_row.append(grid[y][x])
        scaled_grid.append(scaled_row)

    return scaled_grid



def flood_grid(y, x, h, w, g):
    if y < 0 or y >= h or x < 0 or x >= w:
        return

    if g[y][x] == '.':
        g[y][x] = 'O'

    if x+1 < w and g[y][x+1] == '.':
        flood_grid(y, x+1, h, w, g)
    if x > 1 and g[y][x-1] == '.':
        flood_grid(y, x-1, h, w, g)
    if y+1 < h and g[y+1][x] == '.':
        flood_grid(y+1, x, h, w, g)
    if y > 1 and g[y-1][x] == '.':
        flood_grid(y-1, x, h, w, g)


def count_char(c : str, grid : list[list[str]]) -> int:
    count = 0
    for row in grid:
        for colum in row:
            if colum == c:
                count += 1
    return count


def keep_main_loop(height, width, grid, numbers):
    new_grid = [ [ '.' ] * width for _ in range(height) ]
    for row in range(height):
        for colum in range(width):
            if numbers[row][colum] != 0:
                new_grid[row][colum] = grid[row][colum]
    return new_grid    

def part2(filename : str) -> int:
    start, grid = parse_input(filename)

    height = len(grid)
    width = len(grid[0])

    # print_grid(grid)

    numbers = compute_main_loop(start, grid)
    # print_numbers(numbers)
    
    grid = keep_main_loop(height, width, grid, numbers)
    # print_grid(grid)

    scaled_grid = scale_up(grid)
    # print_grid(scaled_grid)

    scaled_height = len(scaled_grid)
    scaled_width = len(scaled_grid[0])
    flood_grid(0, 0, scaled_height, scaled_width, scaled_grid)
    # print_grid(scaled_grid)

    scaled_down_grid = scale_down(scaled_grid)
    # print_grid(scaled_down_grid)

    challenge = count_char('.', scaled_down_grid)


    return challenge


import sys
sys.setrecursionlimit(100000)

assert part1('./sample.txt') == 4
assert part1('./sample2.txt') == 8

assert part1('./input.txt') == 7066

assert part2('./sample3.txt') == 4
assert part2('./sample4.txt') == 4
assert part2('./sample5.txt') == 8
assert part2('./sample6.txt') == 10

assert part2('./input.txt') == 401

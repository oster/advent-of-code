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
        
        grid.append(row)

    assert start != (-1, -1)

    return (start, grid)


def print_grid(grid : list[list[str]]) -> None:
    for row in grid:
        print(''.join(row).replace('│', '║').replace('─','═').replace('┌','╔').replace('┐','╗').replace('└','╚').replace('┘','╝')) #.replace('.','█'))
    print()


def print_numbers(grid : list[list[int]]) -> None:
    for row in grid:
        for column in row:
            if column == -1:
                print('S', end='')
                # print('SS', end='')
            elif column == 0:
                print('.', end='')
                # print('..', end='')
            else:
                print(f"{column}", end='')
                # print(f"{colum:02d}", end='')
        print()
    print()


def find_max_in_grid(numbers : list[list[int]]) -> int:
    max = 0
    for row in numbers:
        for colum in row:
            if colum > max:
                max = colum
    return max  


from collections import deque
def flood_pipe_bfs(y, x, step, h, w, g, n):

    states = deque()
    states.append((y, x, step))

    while states:
        (cy, cx, step) = states.popleft()

        if cy < 0 or cy >= h or cx < 0 or cx >= w:
            continue
        if n[cy][cx] != 0 and n[cy][cx] <= step:
            continue

        n[cy][cx] = step
        step = step + 1

        match g[cy][cx]:
            case '│':
                states.append((cy+1, cx, step))
                states.append((cy-1, cx, step))
            case '─':
                states.append((cy, cx+1, step))
                states.append((cy, cx-1, step))
            case '┌':
                states.append((cy+1, cx, step))
                states.append((cy, cx+1, step))
            case '┐':
                states.append((cy, cx-1, step))
                states.append((cy+1, cx, step))
            case '┘':
                states.append((cy-1, cx, step))
                states.append((cy, cx-1, step))
            case '└':
                states.append((cy, cx+1, step))
                states.append((cy-1, cx, step))
            case _:
                continue        


def flood_pipe(y, x, step, h, w, g, n):
    if y < 0 or y >= h or x < 0 or x >= w:
        return
    if n[y][x] != 0 and n[y][x] <= step:
        return
    n[y][x] = step

    match g[y][x]:
        case '│':
            flood_pipe(y+1, x, step+1, h, w, g, n)
            flood_pipe(y-1, x, step+1, h, w, g, n)
        case '─':
            flood_pipe(y, x+1, step+1, h, w, g, n)
            flood_pipe(y, x-1, step+1, h, w, g, n)
        case '┌':
            flood_pipe(y+1, x, step+1, h, w, g, n)
            flood_pipe(y, x+1, step+1, h, w, g, n)
        case '┐':
            flood_pipe(y, x-1, step+1, h, w, g, n)
            flood_pipe(y+1, x, step+1, h, w, g, n)
        case '┘':
            flood_pipe(y-1, x, step+1, h, w, g, n)
            flood_pipe(y, x-1, step+1, h, w, g, n)
        case '└':
            flood_pipe(y, x+1, step+1, h, w, g, n)
            flood_pipe(y-1, x, step+1, h, w, g, n)
        case _:
            return


def compute_main_pipe_loop(start : tuple[int,int], grid : list[list[str]]) -> list[list[int]]:
    height = len(grid)
    width = len(grid[0])
    numbers = [ [ 0 ] * width for _ in range(height) ]

    step = 0
    sy, sx = start
    numbers[sy][sx] = -1

    if grid[sy][sx+1] in ['─', '┐', '┘']:
        flood_pipe_bfs(sy, sx+1, step + 1, height, width, grid, numbers)

    if grid[sy][sx-1] in ['─','┌','└']:
        flood_pipe_bfs(sy, sx-1, step + 1, height, width, grid, numbers)

    if grid[sy+1][sx] in ['│', '┘', '└']:
        flood_pipe_bfs(sy+1, sx, step + 1, height, width, grid, numbers)

    if grid[sy-1][sx] in ['│', '┌', '┐']:
        flood_pipe_bfs(sy+1, sx, step + 1, height, width, grid, numbers)

    return numbers


def part1(filename : str) -> int:
    start, grid = parse_input(filename)
    numbers = compute_main_pipe_loop(start, grid)
    challenge = find_max_in_grid(numbers)

    return challenge



def scale_up(grid : list[list[str]]) -> list[list[str]]:
    height = len(grid)
    width = len(grid[0])

    scaled_x_grid = []
    for row in grid:
        scaled_row = []
        scaled_row.append('.')
        for x in range(len(row)):
            scaled_row.append(row[x])
            if row[x] in ['S','┌', '─', '└'] and x+1 < width and row[x+1] in ['┐', '─', '┘', 'S']:
                scaled_row.append('─')
            else:
                scaled_row.append('.')
        scaled_x_grid.append(scaled_row)

    scaled_xy_grid = []
    scaled_xy_grid.append(['.'] * ((width+1) * 2 - 1) )
    for y in range(len(grid)):
        scaled = []
        for x in range(len(scaled_x_grid[y])):
            if scaled_x_grid[y][x] in ['S', '┌', '│', '┐'] and y+1 < height and scaled_x_grid[y+1][x] in ['└', '│', '┘']:
                scaled.append('│')
            else:
                scaled.append('.')
        scaled_xy_grid.append(scaled_x_grid[y])            
        scaled_xy_grid.append(scaled)

    return scaled_xy_grid


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


def flood_grid_bfs(y, x, height, width, grid):
    states = deque()
    states.append((y, x))

    while states:
        cy, cx = states.popleft()

        if grid[cy][cx] == ' ':
            continue

        if grid[cy][cx] == '.':
            grid[cy][cx] = ' ' #'█'

        for nexty, nextx in [(cy+1, cx), (cy-1, cx), (cy, cx+1), (cy, cx-1)]:

            if nexty < 0 or nexty >= height or nextx < 0 or nextx >= width:
                continue

            if grid[nexty][nextx] == '.':
                states.append((nexty, nextx))


def flood_grid(y, x, height, width, grid):
    if  x < 0 or x >= width or y < 0 or y >= height:
        return

    if grid[y][x] == 'x':
        return

    if grid[y][x] == '.':
        grid[y][x] = 'x' #'█'

    for nexty, nextx in [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]:
        if nexty < 0 or nexty >= height or nextx < 0 or nextx >= width:
            continue
        if grid[nexty][nextx] == '.':
            flood_grid(nexty, nextx, height, width, grid)

    # if x+1 < w and g[y][x+1] == '.':
    #     flood_grid(y, x+1, h, w, g)
    # if x > 1 and g[y][x-1] == '.':
    #     flood_grid(y, x-1, h, w, g)
    # if y+1 < h and g[y+1][x] == '.':
    #     flood_grid(y+1, x, h, w, g)
    # if y > 1 and g[y-1][x] == '.':
    #     flood_grid(y-1, x, h, w, g)


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

    numbers = compute_main_pipe_loop(start, grid)
    # print_numbers(numbers)

    grid = keep_main_loop(height, width, grid, numbers)
    # print_grid(grid)

    scaled_grid = scale_up(grid)
    # print_grid(scaled_grid)

    scaled_height = len(scaled_grid)
    scaled_width = len(scaled_grid[0])
    flood_grid_bfs(0, 0, scaled_height, scaled_width, scaled_grid)
    # print_grid(scaled_grid)

    scaled_down_grid = scale_down(scaled_grid)
    # print_grid(scaled_down_grid)

    challenge = count_char('.', scaled_down_grid)

    return challenge


# import sys
# sys.setrecursionlimit(20000)

assert part1('./sample.txt') == 4
assert part1('./sample2.txt') == 8

assert part1('./input.txt') == 7066

assert part2('./sample3.txt') == 4
assert part2('./sample4.txt') == 4
assert part2('./sample5.txt') == 8
assert part2('./sample6.txt') == 10

assert part2('./input.txt') == 401

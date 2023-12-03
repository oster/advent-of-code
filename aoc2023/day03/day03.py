from typing import Generator, Optional
from functools import reduce

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()

def parse_input(filename : str) -> list:
    return [ list(line) for line in read_input(filename) ]

def print_schema(schema : list) -> None:
    for x in range(len(schema)):
        for y in range(len(schema[x])):
            print(schema[x][y], end='')
        print()

def eight_neighbors(x : int, y : int, height : int, width : int) -> Generator[tuple[int, int], None, None]:
    if y > 0:
        if x > 0:
            yield (x-1, y-1)
        yield (x, y-1)
        if x < width - 1:
            yield (x+1, y-1)        

    if x < width - 1:
        yield (x+1, y)        

    if y < height - 1:
        if x < width - 1:
            yield (x+1, y+1)        
        yield (x, y+1)
        if x > 0:
            yield (x-1, y+1)

    if x > 0:
        yield (x-1, y)

def issymbol(c : str) -> bool:
    return c != '.' and not c.isdigit()

def check_connection(x : int, y : int, schema : list, height : int, width : int) -> bool:
    return any([ issymbol(schema[next_y][next_x]) for next_x, next_y in eight_neighbors(x, y, height, width) ])

def part1(filename : str) -> int:
    schema = parse_input(filename)
    height = len(schema)
    width = len(schema[0])

    numbers = [] # all numbers in the schema
    connected = False # True if we have found a connection to a symbol for the current number
    reading_number = False # True if we are currently parsing a number
    num = 0 # current number to be parsed

    for y in range(height):
        for x in range(width):
            if schema[y][x].isdigit():
                reading_number = True
                num = num * 10 + int(schema[y][x])
                if not connected:
                    connected = check_connection(x, y, schema, height, width)
            else: # not schema[y][x].isdigit():
                if reading_number:
                    if connected:
                        numbers.append(num)
                    reading_number = False
                    num = 0
                    connected = False

    return sum(numbers)


def isgear(c : str) -> bool:
    return c == '*'


def check_connection_with_star(x : int, y : int, schema : list, height : int, width : int) -> Optional[tuple[int, int]]:
    for next_x, next_y in eight_neighbors(x, y, height, width):
        if isgear(schema[next_y][next_x]):
            return (next_x, next_y)
    return None

ID_COUNT = 0

def next_id():
    global ID_COUNT
    ID_COUNT += 1
    return ID_COUNT

def part2(filename : str) -> int:
    schema = parse_input(filename)
    height = len(schema)
    width = len(schema[0])

    number_id = next_id()
    numbers_by_id = {} # all numbers in the schema { id => number }
    gears = {} # all gears in the schema { (pos_x, pos_y) => [number_id, number_id, ...] }

    numbers = [] # all numbers in the schema
    connected = False # True if we have found a connection to a symbol for the current number
    reading_number = False # True if we are currently parsing a number
    num = 0 # current number to be parsed

    for y in range(height):
        for x in range(width):
            if schema[y][x].isdigit():
                reading_number = True
                num = num * 10 + int(schema[y][x])
                if not connected:
                    gear_id = check_connection_with_star(x, y, schema, height, width)
                    if gear_id:
                        connected = True
                        if not gear_id in gears:
                            gears[gear_id] = []
                        if not number_id in gears[gear_id]:
                            gears[gear_id].append(number_id)
            else: # not schema[y][x].isdigit():
                if reading_number:
                    if connected:
                        numbers.append(num)
                        numbers_by_id[number_id] = num
                    reading_number = False
                    num = 0
                    connected = False
                    number_id = next_id()

    sum_gear_ratio = 0
    for gear_id, number_ids in gears.items():
        gear_ratio = reduce(lambda id_a, id_b: numbers_by_id[id_a] * numbers_by_id[id_b], number_ids) if len(number_ids) == 2 else 0
        sum_gear_ratio += gear_ratio

    return sum_gear_ratio

assert part1('./sample.txt') == 4361
assert part1('./input.txt') == 521601

assert part2('./sample.txt') == 467835
assert part2('./input.txt') == 80694070

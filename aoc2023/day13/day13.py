def read_input(filename : str) -> list[list]:
    with open(filename, 'r') as input_file:
        data = input_file.read().split('\n\n')

        schemas = []
        for schema in data:
            schemas.append(parse_schema(schema))

        return schemas
    
def parse_schema(schema : str) -> list:
    s = []
    for line in schema.split('\n'):
        if line != '':
            s.append(list(line.rstrip()))
    return s


def convert_to_int(line) -> int:
    res = 0
    for c in line:
        res = res << 1
        if c == '#':
            res += 1
    return res


def convert_x(schema: list[str]) -> list[int]:
    return [ convert_to_int(s) for s in schema ]


def convert_y(schema: list[str]) -> list[int]:
    int_schemas = []
    w = len(schema[0])
    for x in range(w):
        c = convert_to_int([line[x] for line in schema])
        int_schemas.append(c)
    return int_schemas


def find_symmetric(schema: list[int]) -> int:
    width = len(schema)
    for x in range(width-1):
        v = schema[x]
        if v != schema[x+1]:
            continue

        dec = 0
        bad = False
        while x-dec >= 0 and x+dec+1 < width:
            if schema[x-dec] != schema[x+dec+1]:
                bad = True
                break
            dec += 1
        if not bad:
            return x+1

    return 0


def print_schema(schema):
    for line in schema:
        for c in line:
            print(c, end='')
        print()
    print()


def part1(filename : str) -> int:
    schemas = read_input(filename)

    sum = 0
    for schema in schemas:
        s_y = find_symmetric(convert_y(schema))
        if s_y > 0:
            sum += s_y
            continue

        s_x = find_symmetric(convert_x(schema))
        if s_x > 0:
            sum += s_x*100

    return sum


# print(find_symmetric([89, 24, 103, 66, 37, 37, 66, 103, 24]))
# print(find_symmetric([358, 90, 385, 385, 90, 102, 346]))
# print(find_symmetric([281, 265, 103, 502, 502, 103, 265]))
# print(find_symmetric([109, 12, 30, 30, 76, 97, 30, 30, 115]))
# print(find_symmetric([39, 16, 18, 62, 104, 104, 126, 18, 16, 39, 124, 9, 25, 124, 124]))


# assert find_symmetric([89, 24, 103, 66, 37, 37, 66, 103, 24]) == 5
# assert find_symmetric([358, 90, 385, 385, 90, 102, 346]) == 0
# assert find_symmetric([281, 265, 103, 502, 502, 103, 265]) == 4
# assert find_symmetric([109, 12, 30, 30, 76, 97, 30, 30, 115]) == 0


assert part1('./sample.txt') == 405
assert part1('./input.txt') == 34772


def find_all_symmetric(schema: list[int]) -> list[int]:
    width = len(schema)
    res = []
    for x in range(width-1):
        v = schema[x]
        if v != schema[x+1]:
            continue

        dec = 0
        bad = False
        while x-dec >= 0 and x+dec+1 < width:
            if schema[x-dec] != schema[x+dec+1]:
                bad = True
                break
            dec += 1
        if not bad:
            res.append(x+1)

    return res


def part2(filename : str) -> int:
    schemas = read_input(filename)

    sum = 0
    for schema in schemas:
        s_y = find_symmetric(convert_y(schema))
        s_x = find_symmetric(convert_x(schema))
        
        for y in range(len(schema)):
            for x in range(len(schema[0])):
                old = schema[y][x]

                if schema[y][x] == '#': # switch char
                    schema[y][x] = '.'
                else:
                    schema[y][x] = '#'

                new_s_xs = find_all_symmetric(convert_x(schema))
                for new_s_x in new_s_xs:
                    if (new_s_x > 0 and new_s_x != s_x):
                        sum += new_s_x*100 

                new_s_ys = find_all_symmetric(convert_y(schema))
                for new_s_y in new_s_ys:
                    if (new_s_y > 0 and new_s_y != s_y):
                        sum += new_s_y

                schema[y][x] = old # restore char

    return sum // 2

assert part2('./sample.txt') == 400
assert part2('./input.txt') == 35554


# from icecream import ic

def read_data(filename: str) -> list[tuple[int, tuple[int, ...]]]:
    with open(filename, "r") as data_file:
        return [(int(challenges), tuple(map(int, values.split()))) for challenges, values in (line.split(':') for line in data_file.readlines())]


def solve_rec(challenge: int, values: tuple[int, ...], depth: int, current: int) -> bool:
    if depth >= len(values):
        return current == challenge

    if current > challenge:
        return False
    
    return ( solve_rec(challenge, values, depth + 1, current * values[depth]) 
            or solve_rec(challenge, values, depth + 1, current + values[depth])
    )


def part1(filename: str) -> int:
    challenges = read_data(filename)
    return sum(challenge for challenge, values in challenges if solve_rec(challenge, values, 1, values[0]))


def concat_op(a : int , b: int) -> int:
    # return int(str(a) + str(b))
    # return a * 10**int(log10(b)+1) + b
    n = b
    while n != 0:  
        n = n // 10
        a = a * 10
    return a + b

def solve2_rec(challenge: int, values: tuple[int, ...], depth: int, current: int) -> bool:
    if depth >= len(values):
        return current == challenge

    if current > challenge:
        return False

    # for op in [int.__mul__, int.__add__, concat_op]:
    #     if solve2_rec(challenge, values, depth + 1, op(current, values[depth])):
    #         return True

    return ( solve2_rec(challenge, values, depth + 1, current * values[depth]) 
            or solve2_rec(challenge, values, depth + 1, current + values[depth]) 
            or solve2_rec(challenge, values, depth + 1, concat_op(current, values[depth]))
    )


def part2(filename: str) -> int:
    challenges = read_data(filename)
    return sum(challenge for challenge, values in challenges if solve2_rec(challenge, values, 1, values[0]))


# ic.disable()

# assert ic(part1('./sample.txt')) == 3749
# assert ic(part1('./input.txt')) == 5030892084481

# assert ic(part2('./sample.txt')) == 11387
# assert ic(part2('./input.txt')) == 91377448644679


assert part1('./sample.txt') == 3749
assert part1('./input.txt') == 5030892084481
assert part2('./sample.txt') == 11387
assert part2('./input.txt') == 91377448644679

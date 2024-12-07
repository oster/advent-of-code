
def read_data(filename: str) -> list[tuple[int, list[int]]]:
    with open(filename, "r") as data_file:
        return [(int(challenges), list(map(int, values.split()))) for challenges, values in (line.split(':') for line in data_file.readlines())]


def solve_rec(challenge: int, values: list[int], current) -> bool:
    if values == []:
        return challenge == current
    
    h, t = values[0], values[1:]
    return solve_rec(challenge, t, current*h) or solve_rec(challenge, t, current+h)


def part1(filename: str) -> int:
    challenges = read_data(filename)
    return sum(challenge for challenge, values in challenges if solve_rec(challenge, values[1:], values[0]))


def concat_op(a : int , b: int) -> int:
    # return int(str(a) + str(b))
    # return a * 10**int(log10(b)+1) + b
    n = b
    while n != 0:  
        n = n // 10
        a = a * 10
    return a + b


def solve2_rec(challenge: int, values: list[int], current) -> bool:
    if values == []:
        return challenge == current
    
    h, t = values[0], values[1:]
    return solve2_rec(challenge, t, current*h) or solve2_rec(challenge, t, current+h) or solve2_rec(challenge, t, concat_op(current, h)) 


def part2(filename: str) -> int:
    challenges = read_data(filename)
    return sum(challenge for challenge, values in challenges if solve2_rec(challenge, values[1:], values[0]))


assert part1('./sample.txt') == 3749
assert part1('./input.txt') == 5030892084481
assert part2('./sample.txt') == 11387
assert part2('./input.txt') == 91377448644679

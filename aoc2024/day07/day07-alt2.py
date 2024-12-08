
def read_data(filename: str) -> list[tuple[int, list[int]]]:
    with open(filename, "r") as data_file:
        return [(int(challenges), list(map(int, values.split()))) for challenges, values in (line.split(':') for line in data_file.readlines())]


def solve_rec(challenge: int, values: list[int]) -> bool:
    if values == []:
        return challenge == 0
    
    if challenge == 0:
        return len(values) == 0 # or all the remaining values are 0

    h, t = values[0], values[1:]

    return ((challenge % h == 0 and solve_rec(challenge // h, t)) 
            or (challenge - h >= 0 and solve_rec(challenge - h, t))
    )


def part1(filename: str) -> int:
    challenges = read_data(filename)
    return sum(challenge for challenge, values in challenges if solve_rec(challenge, list(reversed(values))))


def solve2_rec(challenge: int, values: list[int]) -> bool:
    if values == []:
        return challenge == 0
    
    if challenge == 0:
        return len(values) == 0 # or all the remaining values are 0

    h, t = values[0], values[1:]

    if (challenge % h == 0 and solve2_rec(challenge // h, t)) or (challenge - h >= 0 and solve2_rec(challenge - h, t)):
        return True

    digits_count = 0
    n = h
    while n != 0:  
        n = n // 10
        digits_count += 1

    remaining = challenge // 10**digits_count
    z = challenge % 10**digits_count
    
    return z == h and solve2_rec(remaining, t)


def part2(filename: str) -> int:
    challenges = read_data(filename)
    return sum(challenge for challenge, values in challenges if solve2_rec(challenge, list(reversed(values))))


assert part1('./sample.txt') == 3749
assert part1('./input.txt') == 5030892084481

assert part2('./sample.txt') == 11387
assert part2('./input.txt') == 91377448644679

# ic(solve2_rec(729, list(reversed([6, 6, 7, 37, 650]))))
# ic(solve2_rec(156, [56, 1]))
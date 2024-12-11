from icecream import ic


def read_data(filename: str) -> list[int]:
    with open(filename, "r") as data_file:
        values = list(map(int, data_file.read().split()))
    return values


def digit_count(n: int) -> int:
    if n == 0:
        return 1
    k = n
    digit_count = 0
    while k > 0:
        k //= 10
        digit_count += 1
    return digit_count


# assert digit_count(1234) == 4
# assert digit_count(123) == 3
# assert digit_count(12) == 2
# assert digit_count(1) == 1
# assert digit_count(0) == 1


def split_int_in_two(n: int) -> tuple[int, int]:
    p = 10 ** (digit_count(n) // 2)
    return n // p, n % p


# assert split_int_in_two(1234) == (12, 34)
# assert split_int_in_two(12) == (1, 2)


stones_generation = {}  # { (stone, blink): stones_count }


def transform(stone: int, blink: int, mem={}) -> int:
    if (stone, blink) in mem:
        return mem[(stone, blink)]

    if blink == 0:
        return 1

    stones_count = 0

    if stone == 0:
        stones_count += transform(1, blink - 1, mem)
    else:
        digits = digit_count(stone)
        if digits % 2 == 0:
            stone_left, stone_right = split_int_in_two(stone)
            stones_count += transform(stone_left, blink - 1, mem)
            stones_count += transform(stone_right, blink - 1, mem)

        else:
            stones_count += transform(stone * 2024, blink - 1, mem)

    mem[(stone, blink)] = stones_count

    return stones_count


def part1(filename: str) -> int:
    stones = read_data(filename)
    return sum([transform(stone, 25) for stone in stones])


def part2(filename: str) -> int:
    stones = read_data(filename)
    return sum([transform(stone, 75) for stone in stones])


# ic.disable()

assert ic(part1("./sample.txt")) == 55312
assert ic(part1("./input.txt")) == 216996

assert ic(part2("./input.txt")) == 257335372288947

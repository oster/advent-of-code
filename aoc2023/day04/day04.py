from typing import Generator

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()

def parse_input(filename : str) -> list[tuple[list, list]]:
    res = []
    for line in read_input(filename):
        winning_numbers = [ int(x) for x in line[line.index(':')+1:line.index('|')-1].split() ]
        numbers = [ int(x) for x in line[line.index('|')+1:].split() ]
        res.append((winning_numbers, numbers))
    return res

def part1(filename : str) -> int:
    cards = parse_input(filename)

    points = 0
    for winning_numbers, numbers in cards:
        winning_numbers = set(winning_numbers)
        numbers = set(numbers)
        gold_numbers = winning_numbers.intersection(numbers)
        card_points = 2 ** (len(gold_numbers)-1) if len(gold_numbers) > 0 else 0
        points += card_points
    return points

def part2(filename : str) -> int:
    cards = parse_input(filename)

    wins = []
    for winning_numbers, numbers in cards:
        winning_numbers = set(winning_numbers)
        numbers = set(numbers)
        gold_numbers = winning_numbers.intersection(numbers)
        wins.append(len(gold_numbers))

    instances = [1] * len(cards)
    for idx, gold_numbers_count in enumerate(wins):
        for idx2 in range(idx+1, idx+gold_numbers_count+1):
            instances[idx2] += instances[idx]

    return sum(instances)

assert part1('./sample.txt') == 13
assert part1('./input.txt') == 17803

assert part2('./sample.txt') == 30
assert part2('./input.txt') == 5554894

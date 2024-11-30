import sys

type Card = list[list[int]]
SIZE = 5


def dump_card(card: Card) -> None:
    for row in card:
        for col in row:
            print(f"{col:2d}", end=" ")
        print()
    print()


def read_data(filename: str) -> tuple[list[int], list[Card]]:
    numbers = None
    cards = []
    with open(filename, "r") as data_file:
        numbers_desc, *cards_desc = data_file.read().split("\n\n")
        cards_desc[len(cards_desc) - 1] = cards_desc[len(cards_desc) - 1].rstrip()

        numbers = list(map(int, numbers_desc.rstrip().split(",")))

        cards = []
        for card_desc in cards_desc:
            card = []
            for line in card_desc.split("\n"):
                card.append(list(map(int, line.rstrip().split())))
            cards.append(card)

    return numbers, cards


def is_winning(card: Card) -> tuple[bool, int]:
    winning = False
    all_sum = 0
    col_sums = [0] * 5

    for row in card:
        row_sum = 0
        for idx_col, col in enumerate(row):
            row_sum += col
            col_sums[idx_col] += col
            all_sum += col if col != -1 else 0
        if row_sum == -SIZE:
            winning = True
    if not winning and (-5 in col_sums):
        winning = True

    return winning, all_sum


def mark_number(num: int, card: Card) -> Card:
    for row in card:
        for idx_col, col in enumerate(row):
            if col == num:
                row[idx_col] = -1
    return card


def part1(filename: str) -> int:
    numbers, cards = read_data(filename)

    for num in numbers:
        for card in cards:
            card = mark_number(num, card)
            has_won, all_sum = is_winning(card)
            if has_won:
                return num * all_sum

    return -1


def part2(filename: str) -> int:
    numbers, cards = read_data(filename)

    for num in numbers:
        cards_to_remove = []
        for card in cards:
            card = mark_number(num, card)
            has_won, all_sum = is_winning(card)

            if has_won:
                if len(cards) == 1:
                    return num * all_sum
                cards_to_remove.append(card)

        if len(cards_to_remove) > 0:
            for card in cards_to_remove:
                cards.remove(card)

    return -1


assert part1("sample.txt") == 4512
assert part1("input.txt") == 54275

assert part2("sample.txt") == 1924
assert part2("input.txt") == 13158

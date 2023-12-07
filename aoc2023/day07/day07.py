from typing import Generator

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIRS = 3
ONE_PAIR = 2
HIGH_CARD = 1

def hand_type(cards, card_symbols) -> int:
    occurrences = [0] * len(card_symbols)
    for card in cards:
        occurrences[card-1] += 1
    occurrences = sorted(occurrences, reverse=True)
    max = occurrences[0]
    max2 = occurrences[1]

    match max:
        case 5: return FIVE_OF_A_KIND
        case 4: return FOUR_OF_A_KIND
        case 3:
            match max2:
                case 2: return FULL_HOUSE
                case _: return THREE_OF_A_KIND
        case 2: 
            match max2:
                case 2: return TWO_PAIRS
                case _: return ONE_PAIR
        case _: return HIGH_CARD


def hand_type_part2(cards, card_symbols) -> int:
    cards = cards[:]

    joker_value = 1
    joker_count = cards.count(joker_value) # joker is the last card

    cards_without_joker = list(filter(lambda card: joker_value != card, cards))
    type = hand_type(cards_without_joker, card_symbols)

    if joker_count == 0:
        return hand_type(cards, card_symbols)

    # so there is at least one joker
    if joker_count == 5:
        return FIVE_OF_A_KIND
    if joker_count == 4: 
        return FIVE_OF_A_KIND
    if joker_count == 3:
        if type == ONE_PAIR:
            return FIVE_OF_A_KIND
        return FOUR_OF_A_KIND
    if joker_count == 2:
        if type == THREE_OF_A_KIND:
            return FIVE_OF_A_KIND
        if type == ONE_PAIR:
            return FOUR_OF_A_KIND
        return THREE_OF_A_KIND
    # if joker_count == 1:
    if type == FOUR_OF_A_KIND:
        return FIVE_OF_A_KIND
    if type == THREE_OF_A_KIND:
        return FOUR_OF_A_KIND
    if type == TWO_PAIRS:
        return FULL_HOUSE
    if type == ONE_PAIR:
        return THREE_OF_A_KIND            
    return ONE_PAIR


def encode_cards(cards):
    return  (((cards[0] << 4 | cards[1]) << 4 | cards[2]) << 4 | cards[3]) << 4 | cards[4]


def parse_input(filename : str, card_symbols, hand_typer) -> list:
    inputs = read_input(filename)

    hands = []
    for line in inputs:
        cards, bids = line.split()
        # cards_str = str(cards)
        cards = [ 1 + card_symbols.index(card) for card in cards ]

        hand_type = hand_typer(cards, card_symbols)
        value = hand_type << 20 | encode_cards(cards)

        bids = int(bids)
        hands.append((cards, value, bids))

    return hands


def compute_winnings(hands):
    res = 0
    for rank, hand in enumerate(sorted(hands, key=lambda hand: hand[1])):
        res += hand[2] * (rank + 1)
    return res


def part1(filename : str) -> int:
    hands = parse_input(filename, ['2','3','4','5','6','7','8','9','T','J','Q','K','A'], hand_type)
    return compute_winnings(hands)

def part2(filename : str) -> int:
    hands = parse_input(filename, ['J','2','3','4','5','6','7','8','9','T','Q','K','A'], hand_type_part2)
    return compute_winnings(hands)


assert part1('./sample.txt') == 6440
assert part1('./input.txt') == 252295678

assert part2('./sample.txt') == 5905
assert part2('./input.txt') == 250577259

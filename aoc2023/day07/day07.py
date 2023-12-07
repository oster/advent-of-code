from typing import Generator, Callable
from enum import Enum

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()


class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


def compute_hand_type(cards : str, card_symbols : list[str]) -> HandType:
    occurrences = sorted([ cards.count(card_symbols[idx]) for idx in range(len(card_symbols))], reverse=True)

    max, max2 = occurrences[0], occurrences[1]

    match max:
        case 5: 
            return HandType.FIVE_OF_A_KIND
        case 4: 
            return HandType.FOUR_OF_A_KIND
        case 3:
            match max2:
                case 2: 
                    return HandType.FULL_HOUSE
                case _: 
                    return HandType.THREE_OF_A_KIND
        case 2: 
            match max2:
                case 2: 
                    return HandType.TWO_PAIRS
                case _: 
                    return HandType.ONE_PAIR
        case _: 
            return HandType.HIGH_CARD


def compute_hand_type_with_joker(cards : str, card_symbols : list[str]) -> HandType:
    joker_count = cards.count('J') # joker is the last card
    cards_without_joker = ''.join(filter(lambda card: card != 'J', cards))
    hand_type = compute_hand_type(cards_without_joker, card_symbols)

    match joker_count:
        case 5: return HandType.FIVE_OF_A_KIND
        case 4: return HandType.FIVE_OF_A_KIND
        case 3:
            match hand_type:
                case HandType.ONE_PAIR: 
                    return HandType.FIVE_OF_A_KIND
                case _: 
                    return HandType.FOUR_OF_A_KIND
        case 2:
            match hand_type:
                case HandType.THREE_OF_A_KIND: 
                    return HandType.FIVE_OF_A_KIND
                case HandType.ONE_PAIR: 
                    return HandType.FOUR_OF_A_KIND
                case _: 
                    return HandType.THREE_OF_A_KIND
        case 1:
            match hand_type:
                case HandType.FOUR_OF_A_KIND: 
                    return HandType.FIVE_OF_A_KIND
                case HandType.THREE_OF_A_KIND: 
                    return HandType.FOUR_OF_A_KIND
                case HandType.TWO_PAIRS: 
                    return HandType.FULL_HOUSE
                case HandType.ONE_PAIR: 
                    return HandType.THREE_OF_A_KIND
                case _: 
                    return HandType.ONE_PAIR
        case 0:
                return compute_hand_type(cards, card_symbols)
        case _: 
            return HandType.HIGH_CARD
        

def encode_cards(cards : str, card_symbols) -> int:
    def value(card : str) -> int:
        return card_symbols.index(card)
    return  (((value(cards[0]) << 4 | value(cards[1])) << 4 | value(cards[2])) << 4 | value(cards[3])) << 4 | value(cards[4])


def parse_input(filename : str, card_symbols, hand_typer : Callable[[str, list[str]], HandType]) -> list[tuple[str, int, int]]:
    inputs = read_input(filename)

    hands = []
    for line in inputs:
        cards, bids = line.split()
        hand_type = hand_typer(cards, card_symbols)
        value = hand_type.value << 20 | encode_cards(cards, card_symbols)
        bids = int(bids)
        hands.append((cards, value, bids))

    return hands


def compute_winnings(hands : list[tuple[str, int, int]]) -> int:
    res = 0
    for rank, hand in enumerate(sorted(hands, key=lambda hand: hand[1])):
        res += hand[2] * (rank + 1)
    return res


def part1(filename : str) -> int:
    hands = parse_input(filename, ['2','3','4','5','6','7','8','9','T','J','Q','K','A'], compute_hand_type)
    return compute_winnings(hands)


def part2(filename : str) -> int:
    hands = parse_input(filename, ['J','2','3','4','5','6','7','8','9','T','Q','K','A'], compute_hand_type_with_joker)
    return compute_winnings(hands)


assert part1('./sample.txt') == 6440
assert part1('./input.txt') == 252295678

assert part2('./sample.txt') == 5905
assert part2('./input.txt') == 250577259

use std::fs;

pub fn read_values_from_file(filename: &str) -> String {
    let binding = fs::read_to_string(filename).unwrap();

    return binding;
}

#[derive(Debug, Clone)]
pub enum HandKind {
    FiveOfAKind = 7,
    FourOfAKind = 6,
    FullHouse = 5,
    ThreeOfAKind = 4,
    TwoPairs = 3,
    OnePair = 2,
    HighCard = 1,
}

pub fn compute_hand_kind(cards: &str, card_symbols: &Vec<char>) -> HandKind {
    let mut card_occurrences = (0..card_symbols.len())
        .map(|idx| cards.chars().filter(|c| *c == card_symbols[idx]).count() as u64)
        .collect::<Vec<u64>>();

    card_occurrences.sort();
    card_occurrences.reverse();

    let (max, max2) = (card_occurrences[0], card_occurrences[1]);

    match max {
        5 => HandKind::FiveOfAKind,
        4 => HandKind::FourOfAKind,
        3 => match max2 {
            2 => HandKind::FullHouse,
            _ => HandKind::ThreeOfAKind,
        },
        2 => match max2 {
            2 => HandKind::TwoPairs,
            _ => HandKind::OnePair,
        },
        _ => HandKind::HighCard,
    }
}

pub fn compute_hand_kind_with_joker(cards: &str, card_symbols: &Vec<char>) -> HandKind {
    let joker_count = cards.chars().filter(|c| *c == 'J').count() as u64;

    let cards_without_joker = cards.chars().filter(|c| *c != 'J').collect::<String>();
    let hand_kind = compute_hand_kind(&cards_without_joker, &card_symbols);

    match joker_count {
        5 => HandKind::FiveOfAKind,
        4 => HandKind::FiveOfAKind,
        3 => match hand_kind {
            HandKind::OnePair => HandKind::FiveOfAKind,
            _ => HandKind::FourOfAKind,
        },
        2 => match hand_kind {
            HandKind::ThreeOfAKind => HandKind::FiveOfAKind,
            HandKind::OnePair => HandKind::FourOfAKind,
            _ => HandKind::ThreeOfAKind,
        },
        1 => match hand_kind {
            HandKind::FourOfAKind => HandKind::FiveOfAKind,
            HandKind::ThreeOfAKind => HandKind::FourOfAKind,
            HandKind::TwoPairs => HandKind::FullHouse,
            HandKind::OnePair => HandKind::ThreeOfAKind,
            _ => HandKind::OnePair,
        },
        0 => compute_hand_kind(cards, card_symbols),
        _ => HandKind::HighCard,
    }
}

pub fn compute_hand_strength(cards: &str, kind: HandKind, card_symbols: &Vec<char>) -> u64 {
    let mut strength = kind as u64;

    for card in cards.chars() {
        let card_value = card_symbols.iter().position(|&c| c == card).unwrap() as u64;

        strength <<= 4;
        strength |= card_value;
    }

    return strength;
}

pub fn parse_input(
    filename: &str,
    card_symbols: Vec<char>,
    hand_kind_computer: fn(&str, &Vec<char>) -> HandKind,
) -> Vec<(String, u64, u64)> {
    let hands: Vec<(String, u64, u64)> = read_values_from_file(filename)
        .lines()
        .map(|line| {
            let parts: Vec<&str> = line.split_whitespace().collect();
            let cards = parts[0];
            let kind = hand_kind_computer(cards, &card_symbols);
            let value = compute_hand_strength(cards, kind, &card_symbols);
            let bids = parts[1].parse::<u64>().unwrap();

            (cards.to_owned(), value, bids)
        })
        .collect();

    hands
}

pub fn compute_winnings(hands: &mut Vec<(String, u64, u64)>) -> u64 {
    let mut res = 0;
    hands.sort_by_key(|k| k.1);

    for (rank, hand) in hands.iter().enumerate() {
        res += hand.2 * ((rank as u64) + 1);
    }
    return res;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sample_part1() {
        let mut values = parse_input(
            "./sample.txt",
            vec![
                '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A',
            ],
            compute_hand_kind,
        );
        let value = compute_winnings(&mut values);
        let expected_value = 6440;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let mut values = parse_input(
            "./sample.txt",
            vec![
                'J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A',
            ],
            compute_hand_kind_with_joker,
        );
        let value = compute_winnings(&mut values);
        let expected_value = 5905;
        assert_eq!(expected_value, value);
    }
}

use std::{fs, collections::HashSet};

#[derive(Debug)]
pub struct Card {
    pub id: u32,
    pub winning: HashSet<u32>,
    pub numbers: HashSet<u32>,
}

pub fn read_values_from_file(filename: &str) -> Vec<Card> {
    let lines : Vec<String> = fs::read_to_string(filename)
        .unwrap()
        .lines()
        .map(|line| line.to_string())
        .collect();

    let mut cards = Vec::new();

    for line in lines {
        let mut card = Card {
            id: 0,
            winning: HashSet::new(),
            numbers: HashSet::new(),
        };

        let r : Vec<&str> = line.split(":").collect();
        card.id = r[0][("Card").len()..].trim().parse::<u32>().unwrap();

        let r2 : Vec<&str> = r[1].split("|").collect();
        card.winning = r2[0].split(" ").filter(|&x| !x.is_empty()).map(|x| x.trim().parse::<u32>().unwrap()).collect();
        card.numbers = r2[1].split(" ").filter(|&x| !x.is_empty()).map(|x| x.trim().parse::<u32>().unwrap()).collect();

        cards.push(card);
    }

    return cards;
}

pub fn compute_part1(cards: &Vec<Card>) -> u32 {
    let mut points = 0;
    for card in cards {
        let gold_numbers_count = card.winning.intersection(&card.numbers).count();
        if gold_numbers_count > 0 {
            points += 2u32.pow((gold_numbers_count-1) as u32);
        }
    }
    points
}

pub fn compute_part2(cards: &Vec<Card>) -> u32 {
    let mut gold_numbers_count_per_card = Vec::new();

    for card in cards {
        let gold_numbers_count = card.winning.intersection(&card.numbers).count();
        gold_numbers_count_per_card.push(gold_numbers_count);
    }

    let mut instances = vec![1; cards.len()];
    for (idx, gold_numbers_count) in gold_numbers_count_per_card.iter().enumerate() {
        for id2 in idx+1..idx+gold_numbers_count+1 {
            instances[id2] += instances[idx];
        }
    }

    instances.iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sample_part1() {
        let _values = read_values_from_file("./sample.txt");

        // todo
        let value = compute_part1(&_values);
        let expected_value = 13;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let _values = read_values_from_file("./sample.txt");

        // todo
        let value = compute_part2(&_values);
        let expected_value = 30;
        assert_eq!(expected_value, value);
    }
}

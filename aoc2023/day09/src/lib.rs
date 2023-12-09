use std::fs;

pub fn read_values_from_file(filename: &str) -> String {
    let binding = fs::read_to_string(filename).unwrap();

    return binding;
}

pub fn parse_input(input: &String) -> Vec<Vec<i64>> {
    let histories: Vec<Vec<i64>> = input
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|x| x.parse::<i64>().unwrap())
                .collect()
        })
        .collect();

    histories
}

pub fn compute_part1(histories: &Vec<Vec<i64>>) -> i64 {
    let challenge = histories
        .iter()
        .map(|history| {
            let mut h = history.clone();
            let mut last_values: Vec<i64> = Vec::new();
            while h.iter().any(|&x| x != 0) {
                last_values.push(*h.last().unwrap());
                h = h.windows(2).map(|w| w[1] - w[0]).collect();
            }
            last_values.iter().sum::<i64>()
        })
        .sum::<i64>();

    challenge
}

pub fn compute_part2(histories: &Vec<Vec<i64>>) -> i64 {
    let challenge = histories
        .iter()
        .map(|history| {
            let mut h = history.clone();
            let mut first_values: Vec<i64> = Vec::new();
            while h.iter().any(|&x| x != 0) {
                first_values.push(*h.first().unwrap());
                h = h.windows(2).map(|w| w[1] - w[0]).collect();
            }

            first_values.iter().rev().fold(0, |acc, x| x - acc)
        })
        .sum::<i64>();

    challenge
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sample_part1() {
        let values = parse_input(&read_values_from_file("./sample.txt"));
        let value = compute_part1(&values);
        let expected_value = 114;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let values = parse_input(&read_values_from_file("./sample.txt"));
        let value = compute_part2(&values);
        let expected_value = 2;
        assert_eq!(expected_value, value);
    }
}

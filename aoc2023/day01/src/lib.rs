use std::fs;

pub fn read_values_from_file(filename: &str) -> Vec<String> {
    fs::read_to_string(filename)
        .unwrap()
        .lines()
        .map(|line| line.to_string())
        .collect()
}

pub fn get_first_and_last_digits(line: &String) -> u32 {
    let mut first = '\0';
    let mut last = '\0';

    for c in line.chars() {
        if c.is_digit(10) {
            if first == '\0' {
                first = c;
            }
            last = c;
        }
    }

    return first.to_digit(10).unwrap() * 10 + last.to_digit(10).unwrap() as u32;
}

pub fn compute_part1(lines: &Vec<String>) -> u32 {
    let mut sum = 0;
    for line in lines {
        sum += get_first_and_last_digits(&line);
    }
    return sum;
}

static NUMBER_NAMES: [&str; 9] = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
];

pub fn get_first_last_digits_or_number_names(line: &String) -> u32 {
    let mut first = 0;
    let mut last = 0;

    let chars = line.as_bytes();
    let line_len = chars.len();

    for i in 0..line_len {
        let c = chars[i];

        if c >= b'0' && c <= b'9' {
            if first == 0 {
                first = c - b'0';
            }
            last = c - b'0';
        } else {
            for (idx, w) in NUMBER_NAMES.iter().enumerate() {
                let numbername_len = i+w.len();
                if numbername_len <= line_len && chars[i..numbername_len] == *w.as_bytes() {
                    if first == 0 {
                        first = (idx + 1) as u8;
                    }
                    last = (idx + 1) as u8;
                    break;
                }
            }
        }
    }

    return first as u32 * 10 + last as u32;
}

pub fn compute_part2(lines: &Vec<String>) -> u32 {
    let mut sum = 0;
    for line in lines {
        sum += get_first_last_digits_or_number_names(&line);
    }
    return sum;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_value() {
        let line = "1abc2".to_string();
        let v = get_first_and_last_digits(&line);
        assert_eq!(v, 12);
    }

    #[test]
    fn test_sample_part1() {
        let lines = read_values_from_file("./sample.txt");

        let value = compute_part1(&lines);

        let expected_value = 142;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let lines = read_values_from_file("./sample2.txt");

        let value = compute_part2(&lines);

        let expected_value = 281;
        assert_eq!(expected_value, value);
    }
}

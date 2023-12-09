use std::{fs, collections::HashMap};

pub fn read_values_from_file(filename: &str) -> String {
    let binding = fs::read_to_string(filename).unwrap();

    return binding;
}

fn convert_base26_to_decimal(s: &str) -> usize {
    s.bytes()
        .map(|c| (c - 'A' as u8) as usize)
        .fold(0, |acc, x| acc * 26 + x)
}

pub fn parse_input(input: &String) -> (Vec<usize>, [[usize; 2]; 17576]) {
    let instructions: Vec<usize> = input
        .lines()
        .next()
        .unwrap()
        .chars()
        .map(|c| if c == 'L' { 0 as usize } else { 1 as usize })
        .collect();
    let mut states: [[usize; 2]; 17576] = [[0, 0]; 26 * 26 * 26];

    input.lines().skip(2).for_each(|line| {
        let src = convert_base26_to_decimal(&line[0..3]);
        let dst1 = convert_base26_to_decimal(&line[7..10]);
        let dst2 = convert_base26_to_decimal(&line[12..15]);
        states[src] = [dst1, dst2];
    });

    (instructions, states)
}

pub fn compute_part1((instructions, states): &(Vec<usize>, [[usize; 2]; 17576])) -> u64 {
    let start = 0 as usize; // "AAA"
    let mut i = 0;
    let n = instructions.len();
    let mut step = 0;

    let mut current = start;

    while current != 26 * 26 * 26 - 1 {
        // "ZZZ"
        step += 1;
        current = states[current][instructions[i]];
        i = (i + 1) % n;
    }

    step
}

// pub fn gcd(a: u64, b: u64) -> u64 {
//     if b == 0 { a } else { gcd(b, a % b) }
// }

pub fn gcd(a: u64, b: u64) -> u64 {
    let mut a = a;
    let mut b = b;
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    return a;
}

// pub fn lcm(a: u64, b: u64) -> u64 {
//     a * b / gcd(a, b)
// }

pub fn lcms(a: Vec<u64>) -> u64 {
    a.iter().fold(1, |acc, &x| acc * x / gcd(acc, x))
}

pub fn compute_part2((instructions, states): &(Vec<usize>, [[usize; 2]; 17576])) -> u64 {
    let end = 26 * 26 * 26 - 1 as usize; // "ZZZ"

    let starts: Vec<usize> = (0..end - 1)
        .filter(|&idx| states[idx as usize] != [0, 0] && idx % 26 == 0)
        .collect::<Vec<usize>>();

    let mut cycles: Vec<u64> = Vec::new();
    let n = instructions.len();

    for start in starts {
        let mut i = 0;
        let mut step = 0;

        let mut current = start;
        while current % 26 != 25 {
            // "..Z"
            step += 1;
            current = states[current][instructions[i]];
            i = (i + 1) % n;
        }

        cycles.push(step);
    }

    lcms(cycles)
}


// Implementing the same with a hashmap to see how it compares

pub fn parse_input_hashmap(input: &String) -> (Vec<usize>, HashMap<&str, [&str; 2]>) {
    let instructions: Vec<usize> = input
        .lines()
        .next()
        .unwrap()
        .chars()
        .map(|c| if c == 'L' { 0 as usize } else { 1 as usize })
        .collect();

    let mut states: HashMap<&str, [&str; 2]> = HashMap::new();

    input.lines().skip(2).for_each(|line| {
        let src = &line[0..3];
        let dst1 = &line[7..10];
        let dst2 = &line[12..15];

        states.insert(src, [dst1, dst2]);
    });

    (instructions, states)
}

pub fn compute_part2_hashmap((instructions, states): &(Vec<usize>, HashMap<&str, [&str; 2]>)) -> u64 {
    let mut cycles: Vec<u64> = Vec::new();
    let n = instructions.len();

    let starts : Vec<&str> = states.keys().map(|&x| x).filter(|key| key.chars().last().unwrap() == 'A').collect();
    for start in starts {
        let mut i = 0;
        let mut step = 0;

        let mut current: &str = start;
        while current.chars().last() != Some('Z') {
            step += 1;
            current = states[current][instructions[i]];
            i = (i + 1) % n;
        }

        cycles.push(step);
    }

    lcms(cycles)
}



#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_base_conversion() {
        let x = convert_base26_to_decimal("AAA");
        assert_eq!(x, 0);

        let y = convert_base26_to_decimal("AAZ");
        assert_eq!(y, 25);

        let z = convert_base26_to_decimal("ZZZ");
        assert_eq!(z, 26 * 26 * 26 - 1);
    }

    #[test]
    fn test_sample_part1() {
        let values = parse_input(&read_values_from_file("./sample.txt"));
        let value = compute_part1(&values);
        let expected_value = 2;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part1b() {
        let values = parse_input(&read_values_from_file("./sample2.txt"));
        let value = compute_part1(&values);
        let expected_value = 6;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let values = parse_input(&read_values_from_file("./sample3b.txt"));
        let value = compute_part2(&values);
        let expected_value = 6;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2_hashmap() {
        let input = read_values_from_file("./sample3b.txt");
        let values = parse_input_hashmap(&input);
        let value = compute_part2_hashmap(&values);
        let expected_value = 6;
        assert_eq!(expected_value, value);
    }

}



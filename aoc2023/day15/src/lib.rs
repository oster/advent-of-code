use std::fs;
use std::iter;

pub fn read_values_from_file(filename: &str) -> String {
    fs::read_to_string(filename).unwrap()
}

pub fn parse_input_part1(input: &String) -> &str {
    input.strip_suffix("\n").unwrap()
}

fn hash(input: &str) -> u64 {
    input
        .chars()
        .map(|c| c as u64)
        .fold(0, |acc, c| ((acc + c) * 17) & 0xff)
}

pub fn compute_part1(data: &str) -> u64 {
    data.split(",").map(|line| hash(line) as u64).sum()
}

pub fn parse_input_part2(input: &String) -> Vec<(char, String, u8)> {
    input
        .strip_suffix("\n")
        .unwrap()
        .split(",")
        .map(|ins| {
            if ins.chars().last().unwrap() == '-' {
                ('-', ins[0..ins.len() - 1].to_string(), 0 as u8)
            } else {
                (
                    '=',
                    ins[0..ins.len() - 2].to_string(),
                    ins[ins.len() - 1..ins.len()].parse::<u8>().unwrap(),
                )
            }
        })
        .collect()
}

fn focusing_power(boxes: &[Vec<(&String, &u8)>]) -> u64 {
    boxes
        .iter()
        .enumerate()
        .map(|(idx_box, one_box)| {
            one_box
                .iter()
                .enumerate()
                .map(|(idx_lens, (_, &lens_focal))| {
                    (idx_box as u64 + 1) * (idx_lens as u64 + 1) * (lens_focal as u64)
                })
                .sum::<u64>()
        })
        .sum()
}

pub fn compute_part2(instructions: &Vec<(char, String, u8)>) -> u64 {
    let mut boxes_vec = iter::repeat(Vec::<(&String, &u8)>::new())
        .take(256)
        .collect::<Vec<Vec<(&String, &u8)>>>();
    let boxes = boxes_vec.as_mut_slice();

    for instruction in instructions {
        match instruction {
            ('-', label, _) => {
                let box_idx = hash(label);
                for (idx, (lens_label, _)) in boxes[box_idx as usize].iter().enumerate() {
                    if *lens_label == label {
                        boxes[box_idx as usize].remove(idx);
                        break;
                    }
                }
            }
            ('=', label, focal_length) => {
                let mut idx_lens: Option<usize> = None;
                let some_box = &mut boxes[hash(label) as usize];
                for (idx, (lens_label, _)) in some_box.iter().enumerate() {
                    if *lens_label == label {
                        idx_lens = Some(idx);
                    }
                }

                match idx_lens {
                    Some(idx) => {
                        some_box[idx] = (label, focal_length);
                    }
                    None => {
                        some_box.push((label, focal_length));
                    }
                }
            }
            _ => {
                panic!("Unknown instruction: {:?}", instruction);
            }
        }
    }

    focusing_power(boxes)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hash() {
        let value = hash("HASH");
        let expected_value = 52;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part1() {
        let input = read_values_from_file("./sample.txt");
        let value = compute_part1(&mut parse_input_part1(&input));
        let expected_value = 1320;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_input_part1() {
        let input = read_values_from_file("./input.txt");
        let value = compute_part1(&mut parse_input_part1(&input));
        let expected_value = 513172;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let input = read_values_from_file("./sample.txt");
        let value = compute_part2(&parse_input_part2(&input));
        let expected_value = 145;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_input_part2() {
        let input = read_values_from_file("./input.txt");
        let value = compute_part2(&parse_input_part2(&input));
        let expected_value = 237806;
        assert_eq!(expected_value, value);
    }
}

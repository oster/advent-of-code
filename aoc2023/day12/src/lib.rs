use std::collections::HashMap;
use std::fs;

pub fn read_values_from_file(filename: &str) -> String {
    let binding = fs::read_to_string(filename).unwrap();

    return binding;
}

pub fn parse_input(input: &String) -> Vec<(&[u8], Vec<u64>)> {
    let records: Vec<(&[u8], Vec<u64>)> = input
        .lines()
        .map(|line| {
            let mut i = 0;
            for c in line.chars() {
                match c {
                    '?' | '#' | '.' => i += 1,
                    _ => break,
                }
            }
            let springs = line[0..i].as_bytes();
            let record = line[i + 1..]
                .split(",")
                .map(|s| s.parse::<u64>().unwrap())
                .collect::<Vec<u64>>();

            (springs, record)
        })
        .collect();

    records
}

pub fn search_rec(
    springs: &[u8],
    record: &Vec<u64>,
    idx_spring: usize,
    idx_record: usize,
    cache: &mut HashMap<(Vec<u8>, Vec<u64>, u64, u64), u64>,
) -> u64 {
    let cache_key = (
        springs[idx_spring..].to_vec(),
        record[idx_record..].to_vec(),
        idx_spring as u64,
        idx_record as u64,
    );
    match cache.get(&cache_key) {
        Some(v) => return *v,
        None => (),
    }

    let record_len = record.len();

    if idx_record == record_len {
        // we have reached the end of the record
        if !springs[idx_spring..].contains(&b'#') {
            // there should be no more springs
            cache.insert(cache_key, 1);
            return 1;
        } else {
            cache.insert(cache_key, 0);
            return 0;
        }
    }

    let mut count = 0;
    let num = record[idx_record] as usize; // number of springs to place
    let mut idx = idx_spring;

    // skip all '.'
    while idx < springs.len() && springs[idx] == b'.' {
        idx += 1;
    }

    if idx == springs.len() {
        // we have reached the end of the springs
        cache.insert(cache_key, 0);
        return 0;
    }

    for mut idx in idx..springs.len() - num + 1 {
        if springs[idx_spring..idx].contains(&b'#') {
            continue;
        }

        let mut tmp = springs.to_owned();
        let new_springs: &mut [u8] = tmp.as_mut_slice();
        let mut goto_next_index = false;

        for i in 0..num {
            let spring = springs[idx + i];

            match spring {
                b'#' => continue,
                b'?' => {
                    new_springs[idx + i] = b'X';
                    continue;
                }
                b'.' => {
                    goto_next_index = true;
                    break;
                }
                _ => (),
            }
        }
        if goto_next_index {
            continue;
        }

        // fill to keep printing consistent
        for k in idx_spring..idx + num {
            if new_springs[k] == b'?' {
                new_springs[k] = b'~';
            }
        }

        idx += num;

        if idx == springs.len() && idx_record == record_len - 1 {
            count += 1;
            continue;
        }

        if idx >= springs.len() {
            continue;
        }

        match springs[idx] {
            b'#' => continue, // bad: we place a spring (right)next to another one
            b'.' => {
                // good, we can call the function recursively to place the next spring
            }
            b'?' => {
                new_springs[idx] = b'_'; // we place a '.' to separate with next spring
                idx += 1;
            }
            _ => (),
        }

        count += search_rec(&new_springs, &record, idx, idx_record + 1, cache);
    }

    cache.insert(cache_key, count);
    count
}

pub fn search(springs: &[u8], record: &Vec<u64>) -> u64 {
    let mut cache: HashMap<(Vec<u8>, Vec<u64>, u64, u64), u64> = HashMap::new();

    search_rec(springs, record, 0, 0, &mut cache)
}

pub fn compute(records: &Vec<(&[u8], Vec<u64>)>) -> u64 {
    let mut res = 0;
    for (springs, record) in records {
        res += search(springs, record)
    }

    res
}

pub fn compute_part1(records: &Vec<(&[u8], Vec<u64>)>) -> u64 {
    compute(records)
}

pub fn compute_part2(records: &Vec<(&[u8], Vec<u64>)>) -> u64 {
    let mut expanded_records = Vec::new();

    for (springs, record) in records {
        // TODO: find a way to repeat the springs 5 times

        // let elt = String::from_utf8(springs.to_vec()).unwrap();
        // let elt2: String = std::iter::repeat(elt).take(5).collect::<String>();
        // let el3 = elt2.to_owned();
        // let new_springs: &[u8]  = elt3.as_bytes();

        // let mut some_str = String::new();
        // some_str.push_str(&elt);
        // some_str.push_str(&elt);
        // some_str.push_str(&elt);
        // some_str.push_str(&elt);
        // some_str.push_str(&elt);
        // let new_springs = some_str.as_bytes();

        // let new_springs: [u8] = elt.repeat(5).as_bytes();
        //let new_springs = new_springs.to_owned();

        // let new_springs = std::iter::repeat(springs.to_vec()).take(5).flatten().collect::<Vec<u8>>().as_slice();

        let new_springs = *springs;

        let new_record = std::iter::repeat(record)
            .take(5)
            .flatten()
            .map(|&v| v)
            .collect::<Vec<u64>>();

        expanded_records.push((new_springs, new_record));
    }

    compute(&expanded_records)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_search() {
        let expected = 1;
        let got = search("???.###".as_bytes(), &[1, 1, 3].to_vec());
        assert_eq!(expected, got, "Expected {}, got {}", expected, got);

        let expected = 4;
        let got = search(".??..??...?##.".as_bytes(), &[1, 1, 3].to_vec());
        assert_eq!(expected, got, "Expected {}, got {}", expected, got);

        let expected = 1;
        let got = search("?#?#?#?#?#?#?#?".as_bytes(), &[1, 3, 1, 6].to_vec());
        assert_eq!(expected, got, "Expected {}, got {}", expected, got);

        let expected = 1;
        let got = search("????.#...#...".as_bytes(), &[4, 1, 1].to_vec());
        assert_eq!(expected, got, "Expected {}, got {}", expected, got);

        let expected = 4;
        let got = search("????.######..#####.".as_bytes(), &[1, 6, 5].to_vec());
        assert_eq!(expected, got, "Expected {}, got {}", expected, got);

        let expected = 10;
        let got = search("?###????????".as_bytes(), &[3, 2, 1].to_vec());
        assert_eq!(expected, got, "Expected {}, got {}", expected, got);
    }

    #[test]
    fn test_sample_part1() {
        let input = read_values_from_file("./sample.txt");
        let values = parse_input(&input);
        let value = compute_part1(&values);
        let expected_value = 21;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part1_input() {
        let input = read_values_from_file("./input.txt");
        let values = parse_input(&input);
        let value = compute_part1(&values);
        let expected_value = 8419;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let input = read_values_from_file("./sample2.txt");
        let values = parse_input(&input);
        let value = compute_part1(&values);
        let expected_value = 525152;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2_input() {
        let input = read_values_from_file("./input2.txt");
        let values = parse_input(&input);
        let value = compute_part1(&values);
        let expected_value = 160500973317706;
        assert_eq!(expected_value, value);
    }
}

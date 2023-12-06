use std::fs;
use std::iter::zip;
use itertools::Itertools;

pub fn read_values_from_file(filename: &str) -> String {
    let binding = fs::read_to_string(filename)
        .unwrap();

    return binding;
}

pub fn parse_input_part1(filename: &str) -> Vec<(u64, u64)> {
    let lines : Vec<Vec<u64>> = read_values_from_file(filename)
        .lines()
        .map(|line| {
            let idx = line.find(":").unwrap();
            line[idx+1..].split_whitespace().map(|s| {
                match s.trim().parse::<u64>() {
                    Ok(n) => n,
                    Err(_) => { 
                        println!("Error parsing number: '{}'", s);
                        0
                    }
                }
            }).collect()
        }) 
        .collect();

    let res = zip(lines[0].iter(), lines[1].iter())
        .map(|(a, b)| (*a, *b))
        .collect::<Vec<(u64, u64)>>();  

    return res;

}

pub fn compute_part1(data: Vec<(u64, u64)>) -> u64 {
    let mut res = 1;
    for (allotted_time, best_distance) in data {
        let mut count = 0;
        for push_time in 0..allotted_time+1 {
            if (allotted_time - push_time) * push_time > best_distance {
                count += 1;
            }
        }
        res *= count;
    }

    return res;
}


pub fn parse_input_part2(filename: &str) -> (u64, u64) {
    let values = read_values_from_file(filename)
        .lines()
        .map(|line| {
            let idx = line.find(":").unwrap();
            line[idx+1..].replace(" ", "").parse::<u64>().unwrap()
        }).collect_tuple().unwrap();
    
    return values;
}


pub fn compute_part2_brute(data: (u64, u64)) -> u64 {
    let (allotted_time, best_distance) = data;

    let mut count = 0;
    for push_time in 0..allotted_time+1 {
        if (allotted_time - push_time) * push_time > best_distance {
            count += 1;
        }
    }

    return count;
}


pub fn compute_part2(data: (u64, u64)) -> u64 {
    let (allotted_time, best_distance) : (i64, i64) = (data.0 as i64, data.1 as i64);

    let (a  , b, c) = (-1, allotted_time, -best_distance);

    // Δ = b² - 4ac
    let delta = (b * b) - 4 * (a * c);

    // x1 = -b - √Δ / 2a 
    let x1 = (-b - ((delta as f64).sqrt()) as i64) / (2 * a);

    // x2 = -b + √Δ / 2a
    let x2 = (-b + ((delta as f64).sqrt()) as i64) / (2 * a);

    return (x1 - x2) as u64;
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sample_part1() {
        let values = parse_input_part1("./sample.txt");
        let value = compute_part1(values);
        let expected_value = 288;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let values = parse_input_part2("./sample.txt");
        let value = compute_part2(values);
        let expected_value = 71503;
        assert_eq!(expected_value, value);
    }

}

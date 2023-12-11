use std::fs;

pub fn read_values_from_file(filename: &str) -> String {
    let binding = fs::read_to_string(filename).unwrap();

    return binding;
}

pub fn parse_input(input: &String) -> Vec<(u64, u64, u64)> {
    let mut id: u64 = 0;

    let galaxies: Vec<(u64, u64, u64)> = input
        .lines()
        .enumerate()
        .map(|(row, line)| {
            line.chars()
                .enumerate()
                .map(|(col, c)| match c {
                    '#' => {
                        id += 1;
                        Some((id, col as u64, row as u64))
                    }
                    _ => None,
                })
                .filter_map(|f| f)
                .collect::<Vec<(u64, u64, u64)>>()
        })
        .flatten()
        .collect();

    galaxies
}

fn manhattan_distance(g1: (u64, u64, u64), g2: (u64, u64, u64)) -> u64 {
    (if g1.1 >= g2.1 {
        g1.1 - g2.1
    } else {
        g2.1 - g1.1
    }) + (if g1.2 >= g2.2 {
        g1.2 - g2.2
    } else {
        g2.2 - g1.2
    })
}

fn sum_of_manhattan_distances(galaxies: &Vec<(u64, u64, u64)>) -> u64 {
    let mut sum = 0;
    for i in 0..galaxies.len() {
        let g1 = galaxies[i];
        for j in i + 1..galaxies.len() {
            let g2 = galaxies[j];
            let d = manhattan_distance(g1, g2);
            sum += d;
        }
    }
    sum
}

pub fn compute(galaxies: &Vec<(u64, u64, u64)>, expansion: u64) -> u64 {
    // expand on y-axis
    let mut frontiers: Vec<usize> = Vec::new();
    // galaxies are already sorted by y
    let start_y = galaxies[0].2;
    let end_y = galaxies[galaxies.len() - 1].2;
    for y in start_y..end_y {
        if galaxies.iter().filter(|&g| g.2 == y).count() == 0 {
            frontiers.push(y as usize);
        }
    }

    let mut expanded_galaxies: Vec<(u64, u64, u64)> = Vec::new();
    let mut idx: usize = 0;
    for g in galaxies {
        while idx < frontiers.len() && frontiers[idx] < g.2 as usize {
            idx += 1;
        }
        expanded_galaxies.push((g.0, g.1, g.2 + (idx as u64 * (expansion - 1))));
    }

    // expand on x-axis
    let mut galaxies = expanded_galaxies;
    frontiers.clear();
    // sort galaxies by x
    galaxies.sort_unstable_by_key(|galaxy| galaxy.1);
    let start_x = galaxies[0].1;
    let end_x = galaxies[galaxies.len() - 1].1;
    for x in start_x..end_x {
        if galaxies.iter().filter(|&g| g.1 == x).count() == 0 {
            frontiers.push(x as usize);
        }
    }

    let mut expanded_galaxies: Vec<(u64, u64, u64)> = Vec::new();
    let mut idx: usize = 0;
    for g in galaxies {
        while idx < frontiers.len() && frontiers[idx] < g.1 as usize {
            idx += 1;
        }
        expanded_galaxies.push((g.0, g.1 + (idx as u64 * (expansion - 1)), g.2));
    }

    // sort galaxies by id
    expanded_galaxies.sort_unstable_by_key(|galaxy| galaxy.0);
    sum_of_manhattan_distances(&expanded_galaxies)
}

pub fn compute_part1(galaxies: &Vec<(u64, u64, u64)>) -> u64 {
    compute(galaxies, 2)
}

pub fn compute_part2(galaxies: &Vec<(u64, u64, u64)>, expansion: u64) -> u64 {
    compute(galaxies, expansion)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sample_part1() {
        let values = parse_input(&read_values_from_file("./sample.txt"));
        let value = compute_part1(&values);
        let expected_value = 374;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part1_input() {
        let values = parse_input(&read_values_from_file("./input.txt"));
        let value = compute_part1(&values);
        let expected_value = 9623138;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let values = parse_input(&read_values_from_file("./sample.txt"));
        let value = compute_part2(&values, 10);
        let expected_value = 1030;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2b() {
        let values = parse_input(&read_values_from_file("./sample.txt"));
        let value = compute_part2(&values, 100);
        let expected_value = 8410;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2_input() {
        let values = parse_input(&read_values_from_file("./input.txt"));
        let value = compute_part2(&values, 1000000);
        let expected_value = 726820169514;
        assert_eq!(expected_value, value);
    }
}

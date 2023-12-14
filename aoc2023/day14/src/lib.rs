use std::collections::HashMap;
use std::fs;

#[derive(Clone)]
pub struct Grid {
    grid: Vec<Vec<char>>,
    size: usize,
}

impl Grid {
    fn new(grid: Vec<Vec<char>>) -> Self {
        let mut g = Grid { grid, size: 0 };

        g.size = g.grid.len();

        g
    }

    #[allow(dead_code)]
    fn dump(&self) {
        for row in &self.grid {
            for c in row {
                print!("{}", c);
            }
            println!();
        }
    }

    fn update(&mut self, other: &Grid) {
        self.grid = other.grid.clone();
    }

    fn rotate_clockwise_90_inplace(&mut self) {
        let size = self.size;
        for i in 0..(size / 2) {
            for j in i..(size - i - 1) {
                let temp = self.grid[i][j];
                self.grid[i][j] = self.grid[size - 1 - j][i];
                self.grid[size - 1 - j][i] = self.grid[size - 1 - i][size - 1 - j];
                self.grid[size - 1 - i][size - 1 - j] = self.grid[j][size - 1 - i];
                self.grid[j][size - 1 - i] = temp;
            }
        }
    }
}

fn tilted_column_north(tilted: &mut Grid, x: usize, last_square_rock_y: i64, round_rocks: i64) {
    let i = last_square_rock_y + 1;
    for k in i..(i + round_rocks) {
        tilted.grid[k as usize][x] = 'O';
    }

    if last_square_rock_y != -1 {
        tilted.grid[last_square_rock_y as usize][x] = '#';
    }
}

fn tilted_grid_north(tilted: &mut Grid, grid: &Grid) {
    for x in 0..grid.size {
        let mut round_rocks = 0;
        let mut last_square_rock_y = -1;

        for y in 0..grid.size {
            match grid.grid[y][x] {
                'O' => {
                    round_rocks += 1;
                }
                '#' => {
                    tilted_column_north(tilted, x, last_square_rock_y, round_rocks);
                    round_rocks = 0;
                    last_square_rock_y = y as i64;
                }
                '.' => {
                    // pass
                }
                _ => {
                    panic!("Invalid character.");
                }
            }
        }
        tilted_column_north(tilted, x, last_square_rock_y, round_rocks);
    }
}

fn compute_sum_grid(grid: &Grid) -> i64 {
    let mut sum = 0;

    for y in 0..grid.size {
        sum += grid.grid[y].iter().filter(|c| **c == 'O').count() as i64 * (grid.size - y) as i64;
    }

    sum
}

fn compute_part1_alt(grid: &Grid) -> i64 {
    let mut tilted = Grid::new(vec![vec!['.'; grid.size]; grid.size]);
    tilted_grid_north(&mut tilted, grid);

    compute_sum_grid(&tilted)
}

pub fn read_values_from_file(filename: &str) -> String {
    let binding = fs::read_to_string(filename).unwrap();

    return binding;
}

pub fn parse_input(input: &String) -> Grid {
    let grid: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();

    Grid::new(grid)
}

fn compute_section_sum(round_rocks: i64, last_square_rock_y: i64, height: i64) -> i64 {
    if round_rocks == 0 {
        return 0;
    }

    let i = height - (last_square_rock_y + round_rocks);
    // Σ k for k [i,i+r[
    round_rocks * (2 * i + round_rocks - 1) / 2
}

pub fn compute_part1(grid: &mut Grid) -> i64 {
    let mut sum_values = 0;

    for x in 0..grid.size {
        let mut round_rocks = 0;
        let mut last_square_rock_y = -1;

        let mut sum_column = 0;
        for y in 0..grid.size {
            match grid.grid[y][x] {
                'O' => {
                    round_rocks += 1;
                }
                '#' => {
                    sum_column +=
                        compute_section_sum(round_rocks, last_square_rock_y, grid.size as i64);
                    round_rocks = 0;
                    last_square_rock_y = y as i64;
                }
                '.' => {
                    // pass
                }
                _ => {
                    panic!("Invalid character.");
                }
            }
        }
        sum_column += compute_section_sum(round_rocks, last_square_rock_y, grid.size as i64);
        sum_values += sum_column;
    }

    sum_values
}

pub fn compute_part2(grid: &mut Grid) -> i64 {
    let mut sums_of_cycle: Vec<i64> = vec![0; 4];
    let mut sums_at_cycle: HashMap<(i64, i64, i64, i64), i64> = HashMap::new();
    let mut cycle: i64 = 0;

    while cycle <= 1000000000 {
        for rotation in 0..4 {
            let mut tilted = Grid::new(vec![vec!['.'; grid.size]; grid.size]);
            tilted_grid_north(&mut tilted, grid);
            tilted.rotate_clockwise_90_inplace();
            sums_of_cycle[rotation] = compute_sum_grid(&tilted);
            grid.update(&tilted);
        }

        // println!("cycle {}: {:?}", cycle, sums_of_cycle);
        let key = (
            sums_of_cycle[0],
            sums_of_cycle[1],
            sums_of_cycle[2],
            sums_of_cycle[3],
        );
        if !sums_at_cycle.contains_key(&key) {
            sums_at_cycle.insert(key, cycle);
        } else {
            // println!(">> cycle {} ({:?}) already seen at {}", cycle, sums_of_cycle, sums_at_cycle.get(&key).unwrap());
            let cycle_start = sums_at_cycle.get(&key).unwrap();
            let cycle_length = cycle - cycle_start;
            let cycle_to_found = cycle_start + (1000000000 - 1 - cycle) % cycle_length;

            let key = sums_at_cycle
                .iter()
                .find(|(_, v)| **v == cycle_to_found)
                .unwrap()
                .0;
            return key.3;
        }

        cycle += 1;
    }

    -1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sample_part1() {
        let input = read_values_from_file("./sample.txt");
        let value = compute_part1(&mut parse_input(&input));
        let expected_value = 136;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_input_part1() {
        let input = read_values_from_file("./input.txt");
        let value = compute_part1(&mut parse_input(&input));
        let expected_value = 113078;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part1_alt() {
        let input = read_values_from_file("./sample.txt");
        let value = compute_part1_alt(&mut parse_input(&input));
        let expected_value = 136;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_input_part1_alt() {
        let input = read_values_from_file("./input.txt");
        let value = compute_part1_alt(&mut parse_input(&input));
        let expected_value = 113078;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let input = read_values_from_file("./sample.txt");
        let value = compute_part2(&mut parse_input(&input));
        let expected_value = 64;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_input_part2() {
        let input = read_values_from_file("./input.txt");
        let value = compute_part2(&mut parse_input(&input));
        let expected_value = 94255;
        assert_eq!(expected_value, value);
    }
}

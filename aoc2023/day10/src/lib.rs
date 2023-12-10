use std::fs;
use std::collections::VecDeque;


#[derive(Clone)]
pub struct Grid {
    grid: Vec<Vec<char>>,
    numbers : Option<Vec<Vec<i32>>>,
    start: (usize, usize),
    height: usize,
    width: usize,
}


impl Grid {
    fn new(grid: Vec<Vec<char>>, start: (usize, usize)) -> Self {
        let mut g = Grid {
            grid: grid,
            start: start,
            height: 0,
            width: 0,
            numbers: None,
        };

        g.height = g.grid.len();
        g.width = g.grid[0].len();

        g
    }

    #[allow(dead_code)]
    fn dump(&self) {
        for row in &self.grid {
            for c in row {
                match c {
                    '┌' => print!("╔"),
                    '─' => print!("═"),
                    '┐' => print!("╗"),
                    '│' => print!("║"),
                    '┘' => print!("╝"),
                    '└' => print!("╚"),
                    // '.' => print!("█"),
                    _ => print!("{}", c),

                }
            }
            println!();
        }
        
    }

    #[allow(dead_code)]
    fn dump_numbers(&self) {
        match &self.numbers {
            Some(numbers) => {
                for row in numbers {
                    for c in row {
                        if *c == -1 {
                            print!("S");
                        } else if *c == 0 {
                            print!(".");
                        } else {
                            print!("{}", c);
                        }
                    }
                    println!();
                }
            },
            None => { println!("no numbers"); },
        }

    }


    fn init_numbers(&mut self) {
        self.numbers = Some(Vec::with_capacity(self.height));
        for _ in 0..self.height {
            let mut row = Vec::with_capacity(self.width);
            for _ in 0..self.width {
                row.push(0);
            }
            self.numbers.as_mut().unwrap().push(row);
        }
    }


    fn find_loop(&mut self) -> i64 {
        self.init_numbers();
        let numbers = self.numbers.as_mut().unwrap();

        let (sy, sx) = (self.start.0 as i32, self.start.1 as i32);
        // numbers[sy as usize][sx as usize] = -1;

        // perform BFS from start
        let mut states: VecDeque<(i32, i32, i32)> = VecDeque::new();
        
        // register starting states
        if sx < self.width as i32 - 1 {
            match self.grid[sy as usize][(sx+1) as usize] {
                '─' => states.push_back((sy, sx+1, 1)),
                '┐' => states.push_back((sy, sx+1, 1)),
                '┘' => states.push_back((sy, sx+1, 1)),
                _ => (),
            }
        }

        if sx > 0 {
            match self.grid[sy as usize][(sx-1)  as usize] {
                '─' => states.push_back((sy, sx-1, 1)),
                '┌' => states.push_back((sy, sx-1, 1)),
                '└' => states.push_back((sy, sx-1, 1)),
                _ => (),
            }
        }

        if sy < self.height as i32 - 1 {
            match self.grid[(sy+1) as usize][sx as usize] {
                '│' => states.push_back((sy+1, sx, 1)),
                '┘' => states.push_back((sy+1, sx, 1)),
                '└' => states.push_back((sy+1, sx, 1)),
                _ => (),
            }
        }

        if sy > 0 {
            match self.grid[(sy-1) as usize][sx as usize] {
                '│' => states.push_back((sy-1, sx, 1)),
                '┌' => states.push_back((sy-1, sx, 1)),
                '┐' => states.push_back((sy-1, sx, 1)),
                _ => (),
            }
        }

        let mut max_step = 0;

        while !states.is_empty() {
            let (cy, cx, mut step) = states.pop_front().unwrap();

            if cy < 0 || cy >= self.height as i32 || cx < 0 || cx >= self.width as i32 {
                continue;
            }


            if numbers[cy as usize][cx as usize] != 0 && numbers[cy as usize][cx as usize] <= step {
                continue;
            }

            numbers[cy as usize][cx as usize] = step;

            if step > max_step {
                max_step = step;
            }

            step = step + 1;

            match self.grid[cy as usize][cx as usize] {
                '│' => {
                    states.push_back((cy+1, cx, step));
                    states.push_back((cy-1, cx, step));
                },
                '─' => {
                    states.push_back((cy, cx+1, step));
                    states.push_back((cy, cx-1, step));
                },
                '┌' => {
                    states.push_back((cy+1, cx, step));
                    states.push_back((cy, cx+1, step));
                },
                '┐' => {
                    states.push_back((cy, cx-1, step));
                    states.push_back((cy+1, cx, step));
                },
                '┘' => {
                    states.push_back((cy-1, cx, step));
                    states.push_back((cy, cx-1, step));
                },
                '└' => {
                    states.push_back((cy, cx+1, step));
                    states.push_back((cy-1, cx, step));
                },
                _ => (),
            }
        }

        max_step as i64
    }

    fn clear_keep_loop(&mut self) {
        match &mut self.numbers {
            Some(numbers) => {
                for row_index in 0..self.height {
                    for col_index in 0..self.width {
                        if numbers[row_index][col_index] == 0 {
                            self.grid[row_index][col_index] = ' ';
                        }
                    }
                }
            },
            None => (),
        }
    }

    fn fill_loop(&mut self) {
        let mut inside = false;


        // TODO: take care of last read caracter

        for row_index in 0..self.height {
            inside = false;
            for col_index in 0..self.width {
                match self.grid[row_index][col_index] {
                    'S' => {
                        inside = !inside;
                    },
                    '┌' => {
                        inside = !inside;
                    },
                    '─' => {
                        //inside = !inside;
                    },
                    '┐' => {
                        inside = !inside;
                    },
                    '│' => {
                        inside = !inside;
                    },
                    '┘' => {
                        inside = !inside;
                    },
                    '└' => {
                        inside = !inside;
                    },
                    _ => {
                        if inside {
                            self.grid[row_index][col_index] = '.';
                        }
                    },
                }
            }
        }
    }

}


pub fn read_values_from_file(filename: &str) -> String {
    let binding = fs::read_to_string(filename).unwrap();

    return binding;
}

pub fn parse_input(input: &String) -> Grid {
    let mut start : (usize, usize) = (0, 0);

    let grid: Vec<Vec<char>> = input
        .lines()
        .enumerate()
        .map(|(row_index, line)| {
            let mut row = Vec::new();
            for (index, c) in line.chars().enumerate() {
                if c == 'S' {
                    start = (row_index, index);
                }
                match c {
                    'F' => row.push('┌'),
                    '-' => row.push('─'),
                    '7' => row.push('┐'),
                    '|' => row.push('│'),
                    'J' => row.push('┘'),
                    'L' => row.push('└'),
                    _ => row.push(c),
                }
            }
            row
        })          
        .collect();

        let mut g = Grid::new(grid, start);
        g.height = g.grid.len();
        g.width = g.grid[0].len();

        g
}


pub fn compute_part1(grid : &mut Grid) -> i64 {
    // grid.dump();
    grid.find_loop()
}

pub fn compute_part2(grid : &mut Grid) -> i64 {
    grid.find_loop();
    grid.clear_keep_loop();

    grid.dump();

    grid.fill_loop();

    grid.dump();

    0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sample_part1() {
        let mut values = parse_input(&read_values_from_file("./sample.txt"));
        let value = compute_part1(&mut values);
        let expected_value = 4;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part1b() {
        let mut values = parse_input(&read_values_from_file("./sample2.txt"));
        let value = compute_part1(&mut values);
        let expected_value = 8;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part1_input() {
        let mut values = parse_input(&read_values_from_file("./input.txt"));
        let value = compute_part1(&mut values);
        let expected_value = 7066;
        assert_eq!(expected_value, value);
    }


    #[test]
    fn test_sample_part2() {
        let mut values = parse_input(&read_values_from_file("./sample3.txt"));
        let value = compute_part2(&mut values);
        let expected_value = 4;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2b() {
        let mut values = parse_input(&read_values_from_file("./sample4.txt"));
        let value = compute_part2(&mut values);
        let expected_value = 4;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2c() {
        let mut values = parse_input(&read_values_from_file("./sample5.txt"));
        let value = compute_part2(&mut values);
        let expected_value = 8;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2d() {
        let mut values = parse_input(&read_values_from_file("./sample6.txt"));
        let value = compute_part2(&mut values);
        let expected_value = 10;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2_input() {
        let mut values = parse_input(&read_values_from_file("./input.txt"));
        let value = compute_part2(&mut values);
        let expected_value = 401;
        assert_eq!(expected_value, value);
    }

}

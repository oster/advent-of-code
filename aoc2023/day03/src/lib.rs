use std::fs;
use std::collections::HashMap;

pub fn read_values_from_file(filename: &str) -> Vec<Vec<char>> {
    fs::read_to_string(filename)
        .unwrap()
        .lines()
        .map(|line| line.chars().collect())
        .collect()
}


pub fn is_symbol(c : char) -> bool {
    c != '.' && ! (c >= '0' && c <= '9') // c.is_digit(10)
}


pub fn eight_neighbors(x : usize, y:usize, height : usize, width : usize) -> Vec<(usize, usize)> {
    let mut result = Vec::new();

    if y > 0 {
        if x > 0 {
            result.push((x-1, y-1));
        }
        result.push((x, y-1));
        if x < width - 1 {
            result.push((x+1, y-1));
        }
    }

    if x < width - 1 {
        result.push((x+1, y));
    }

    if y < height - 1 {
        if x < width - 1 {
            result.push((x+1, y+1));
        }
        result.push((x, y+1));
        if x > 0  {
            result.push((x-1, y+1));
        }
    }
    if x > 0 {
        result.push((x-1, y));
    }
    return result;
}


pub fn is_connected(x:usize , y : usize, schema : &Vec<Vec<char>>, height : usize, width : usize) -> bool {
    // for (next_x, next_y) in eight_neighbors(x, y, height, width) {
    //     if is_symbol(schema[next_y][next_x]) {
    //         return true;
    //     }
    // }
    // return false;

    return eight_neighbors(x, y, height, width).iter().map(|&(next_x, next_y)| is_symbol(schema[next_y][next_x])).any(|x| x == true);
}

pub fn compute_part1(schema: &Vec<Vec<char>>) -> u32 {
    let height: usize = schema.len();
    let width : usize = schema[0].len();

    let mut numbers : Vec<u32> = Vec::new(); // all connected numbers in the schema
    let mut connected : bool = false; // True if we have found a connection to a symbol for the current number
    let mut reading_number : bool = false; // True if we are currently parsing a number 
    let mut num : u32 = 0; // current number to be parsed

    for y in 0..height {
        for x in 0..width {
            if schema[y][x].is_digit(10) {
                reading_number = true;
                num = num * 10 + (schema[y][x] as u32 - '0' as u32);
                if !connected {
                    connected = is_connected(x, y, schema, height, width);
                }
            } else { // schema[y][x] is not a digit
                if reading_number {
                    if connected {
                        numbers.push(num);
                    }
                    reading_number = false;
                    num = 0;
                    connected = false;
                }
            }
        }
    }

    numbers.iter().sum()
}


pub fn is_star(c : char) -> bool {
    c == '*'
}

pub fn is_connected_with_star(x:usize , y : usize, schema : &Vec<Vec<char>>, height : usize, width : usize) -> Option<(usize, usize)> {
    for (next_x, next_y) in eight_neighbors(x, y, height, width) {
        if is_star(schema[next_y][next_x]) {
            return Some((next_x, next_y));
        }
    }
    return None;
}

pub fn next_id() -> u32 {
    static mut ID : u32 = 0;
    unsafe {
        ID += 1;
        return ID;
    }
}

pub fn compute_part2(schema: &Vec<Vec<char>>) -> u32 {
    let height: usize = schema.len();
    let width : usize = schema[0].len();

    let mut number_id = next_id();
    let mut numbers_by_id: HashMap<u32, u32> = HashMap::new(); // all connected numbers in the schema { id => number }
    let mut gears: HashMap<(usize, usize), Vec<u32>> = HashMap::new(); // all gears in the schema { (pos_x, pos_y) => [number_id, number_id, ...] }

    let mut numbers : Vec<u32> = Vec::new(); // all numbers in the schema
    let mut connected : bool = false; // True if we have found a connection to a symbol for the current number
    let mut reading_number : bool = false; // True if we are currently parsing a number 
    let mut num : u32 = 0; // current number to be parsed

    for y in 0..height {
        for x in 0..width {
            if schema[y][x].is_digit(10) {
                reading_number = true;
                num = num * 10 + (schema[y][x] as u32 - '0' as u32);
                if !connected {
                    match is_connected_with_star(x, y, schema, height, width) {
                        Some(gear_pos) => {
                            connected = true;

                            // let connected_numbers = 
                            gears.entry(gear_pos).or_insert_with(|| vec![]).push(number_id);
                            // connected_numbers.push(number_id);                        
                        },
                        None => {}
                    }
                }
            } else { // schema[y][x] is not a digit
                if reading_number {
                    if connected {
                        numbers.push(num);
                        numbers_by_id.insert(number_id, num);
                    }
                    reading_number = false;
                    num = 0;
                    connected = false;
                    number_id = next_id();
                }
            }
        }
    }

    let mut sum_gear_ratio: u32 = 0;
    for (_gear_id, number_ids) in gears.iter() {
        let mut gear_ratio = 0;
        if number_ids.len() == 2 {
            gear_ratio = number_ids.iter().fold(1, |acc, number_id| acc * numbers_by_id[number_id]);
        }

        sum_gear_ratio += gear_ratio
    }
    return sum_gear_ratio
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sample_part1() {
        let schema = read_values_from_file("./sample.txt");
        let value = compute_part1(&schema);
        let expected_value = 4361;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let schema = read_values_from_file("./sample.txt");
        let value = compute_part2(&schema);
        let expected_value = 467835;
        assert_eq!(expected_value, value);
    }
}

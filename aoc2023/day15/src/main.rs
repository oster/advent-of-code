use day15::*;
use std::time::Instant;

fn main() {
    // Puzzle 1
    let now = Instant::now();
    let input = read_values_from_file("./input.txt");
    let mut values = parse_input_part1(&input);
    let value = compute_part1(&mut values);
    let timing = now.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 1: = {} in {} ms", value, timing); // 513172

    // // Puzzle 2
    let now2 = Instant::now();
    let input = read_values_from_file("./input.txt");
    let mut values = parse_input_part2(&input);
    let value = compute_part2(&mut values);
    let timing2 = now2.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 2: = {} in {} ms", value, timing2); // 237806
}

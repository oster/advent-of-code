use day01::*;

use std::time::Instant;

fn main() {
    // Puzzle 1
    let lines = read_values_from_file("./input.txt");

    let now = Instant::now();
    let value = compute_part1(&lines);
    let timing = now.elapsed().as_micros() as f64 / 1000.0;

    println!("Part 1: = {} in {} ms", value, timing); //55712

    // Puzzle 2
    let now2 = Instant::now();
    let value = compute_part2(&lines);
    let timing2 = now2.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 2: = {} in {} ms", value, timing2); // 55413

}

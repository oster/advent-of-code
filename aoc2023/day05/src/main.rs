use day05::*;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let data = read_values_from_file("./input.txt");

    // Puzzle 1
    // let now = Instant::now();
    let value = compute_part1(data.clone());
    let timing = now.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 1: = {} in {} ms", value, timing); // 836040384

    // Puzzle 2
    let now2 = Instant::now();
    let value = compute_part2(data);
    let timing2 = now2.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 2: = {} in {} ms", value, timing2); // 10834440
}

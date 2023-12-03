use day03::*;
use std::time::Instant;


fn main() {
    let values = read_values_from_file("./input.txt");

    // Puzzle 1
    let now = Instant::now();
    let value = compute_part1(&values);
    let timing = now.elapsed().as_micros() as f64 / 1000.0;

    println!("Part 1: = {} in {} ms", value, timing); // 521601

    // Puzzle 2
    let now2 = Instant::now();
    let value = compute_part2(&values);
    let timing2 = now2.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 2: = {} in {} ms", value, timing2); // 80694070

}

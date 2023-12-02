use day02::*;
use std::time::Instant;

fn main() {
    let lines = read_values_from_file("./input.txt");
    let games = parse_input(&lines);

    // Puzzle 1
    let now = Instant::now();
    let value = compute_part1(&games);
    let timing = now.elapsed().as_micros() as f64 / 1000.0;

    println!("Part 1: = {} in {} ms", value, timing); // 2716

    // Puzzle 2
    let now2 = Instant::now();
    let value = compute_part2(&games);
    let timing2 = now2.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 2: = {} in {} ms", value, timing2); // 72227
}

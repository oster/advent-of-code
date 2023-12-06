use day06::*;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let data = parse_input_part1("./input.txt");

    // Puzzle 1
    // let now = Instant::now();
    let value = compute_part1(data.clone());
    let timing = now.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 1: = {} in {} ms", value, timing); // 1624896

    // Puzzle 2
    let now2 = Instant::now();
    let data2 = parse_input_part2("./input.txt");
    let value = compute_part2(data2);
    let timing2 = now2.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 2: = {} in {} ms", value, timing2); // 32583852
}

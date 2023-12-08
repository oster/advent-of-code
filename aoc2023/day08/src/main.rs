use day08::*;
use std::time::Instant;

fn main() {
    let nowp = Instant::now();
    let input = read_values_from_file("./input.txt");
    let values = parse_input(&input);
    let timingp = nowp.elapsed().as_micros() as f64 / 1000.0;
    println!("Parsing in {} ms", timingp);

    // Puzzle 1
    let now = Instant::now();
    let value = compute_part1(&values);
    let timing = now.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 1: = {} in {} ms", value, timing); // 14257

    // Puzzle 2
    let now2 = Instant::now();
    let value = compute_part2(&values);
    let timing2 = now2.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 2: = {} in {} ms", value, timing2); // 16187743689077
}

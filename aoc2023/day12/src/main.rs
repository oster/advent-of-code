use day12::*;
use std::time::Instant;

fn main() {
    let nowp = Instant::now();
    let input = read_values_from_file("./input.txt");
    let mut values = parse_input(&input);
    let timingp = nowp.elapsed().as_micros() as f64 / 1000.0;
    println!("Parsing in {} ms", timingp);

    // Puzzle 1
    let now = Instant::now();
    let value = compute_part1(&mut values);
    let timing = now.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 1: = {} in {} ms", value, timing); // 9623138

    // Puzzle 2
    // let now2 = Instant::now();
    // let value = compute_part2(&mut values, 1000000);
    // let timing2 = now2.elapsed().as_micros() as f64 / 1000.0;
    // println!("Part 2: = {} in {} ms", value, timing2); // 726820169514
}

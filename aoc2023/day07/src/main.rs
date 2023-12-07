use day07::*;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let input = read_values_from_file("./input.txt");

    // Puzzle 1
    //let now = Instant::now();
    let mut values = parse_input(
        &input,
        vec![
            '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A',
        ],
        compute_hand_kind,
    );
    let value = compute_winnings(&mut values);
    let timing = now.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 1: = {} in {} ms", value, timing); // 252295678

    // Puzzle 2
    let now2 = Instant::now();
    let mut values = parse_input(
        &input,
        vec![
            'J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A',
        ],
        compute_hand_kind_with_joker,
    );
    let value = compute_winnings(&mut values);
    let timing2 = now2.elapsed().as_micros() as f64 / 1000.0;
    println!("Part 2: = {} in {} ms", value, timing2); // 250577259
}

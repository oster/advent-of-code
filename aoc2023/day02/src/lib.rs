use std::cmp::max;
use std::fs;

pub fn read_values_from_file(filename: &str) -> Vec<String> {
    fs::read_to_string(filename)
        .unwrap()
        .lines()
        .map(|line| line.to_string())
        .collect()
}

#[derive(Debug)]
pub struct Game {
    id: u32,
    draws: Vec<(u32, u32, u32)>,
}

pub fn parse_draw(draw: &str) -> (u32, u32, u32) {
    // " 3 blue, 4 red"
    let draw = draw
        .trim()
        .split(",")
        .map(|c| {
            let pair = c.trim().split(' ').collect::<Vec<&str>>();

            let cubes_count = pair[0].trim().parse::<u32>().unwrap();
            let color = pair[1].trim();

            (color, cubes_count)
        })
        .collect::<Vec<(&str, u32)>>();

    let mut res: (u32, u32, u32) = (0, 0, 0);
    for i in 0..draw.len() {
        match draw[i].0 {
            "red" => res.0 = draw[i].1,
            "green" => res.1 = draw[i].1,
            "blue" => res.2 = draw[i].1,
            _ => panic!(),
        };
    }

    return res;
}

pub fn parse_input(lines: &Vec<String>) -> Vec<Game> {
    let mut games = Vec::new();
    for line in lines {
        let idx = line.find(":").unwrap();
        let draws = line[idx + 2..]
            .split(";")
            .map(|c| parse_draw(c))
            .collect::<Vec<(u32, u32, u32)>>();
        let game = Game {
            id: line[5..idx].parse::<u32>().unwrap(),
            draws,
        };
        games.push(game);
    }
    return games;
}

pub fn compute_part1(games: &Vec<Game>) -> u32 {
    let constraints = (12, 13, 14); // 'red': 12, 'green': 13, 'blue': 14

    let mut count = 0;
    for game in games {
        if game.draws.iter().all(|draw| {
            draw.0 <= constraints.0 && draw.1 <= constraints.1 && draw.2 <= constraints.2
        }) {
            count += game.id;
        }
    }

    return count;
}

pub fn compute_part2(games: &Vec<Game>) -> u32 {
    let mut count = 0;
    for game in games {
        let power = game.draws.iter().fold((0, 0, 0), |cur, next| {
            (max(cur.0, next.0), max(cur.1, next.1), max(cur.2, next.2))
        });
        count += power.0 * power.1 * power.2;
    }

    return count;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sample_part1() {
        let lines = read_values_from_file("./sample.txt");
        let games = parse_input(&lines);
        let value = compute_part1(&games);
        let expected_value = 8;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let lines = read_values_from_file("./sample.txt");
        let games = parse_input(&lines);
        let value = compute_part2(&games);
        let expected_value = 2286;
        assert_eq!(expected_value, value);
    }
}

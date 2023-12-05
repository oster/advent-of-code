use itertools::Itertools;
use std::fs;


#[derive(Debug, Clone)]
pub struct Transformer {
    pub title: String,
    pub transformations: Vec<(u64, u64, u64)>,
}

pub fn read_values_from_file(filename: &str) -> (Vec<u64>, Vec<Transformer>) {
    let lines = fs::read_to_string(filename)
        .unwrap()
        .lines()
        .map(|line| line.to_string())
        .collect::<Vec<String>>();

    let seeds: Vec<u64> = lines[0]
        .split(": ")
        .nth(1)
        .unwrap()
        .split(" ")
        .map(|x| x.parse::<u64>().unwrap())
        .collect::<Vec<u64>>();

    let mut i = 2;

    let mut transformers: Vec<Transformer> = Vec::new();

    while i < lines.len() {
        let mut transformer = Transformer {
            title: lines[i].to_string(),
            transformations: Vec::new(),
        };
        i = i + 1;

        while i < lines.len() && !lines[i].is_empty() {
            if let Some(tuple) = lines[i]
                .trim()
                .split(" ")
                .map(|x| x.parse::<u64>().unwrap())
                .collect_tuple()
            {
                transformer.transformations.push(tuple);
            } else {
                panic!("Error parsing line: {}", lines[i])
            }
            i = i + 1;
        }
        transformers.push(transformer);
        i = i + 1;
    }

    return (seeds, transformers);
}

pub fn compute_part1(data: (Vec<u64>, Vec<Transformer>)) -> u64 {
    let mut min_seed = u64::MAX;
    let (seeds, transformers) = data;
    for mut seed in seeds {
        for transformer in transformers.iter() {
            for &(dst, src, rng) in transformer.transformations.iter() {
                if seed >= src && seed < src + rng {
                    seed = dst + (seed - src);
                    break;
                }
            }
        }
        if seed < min_seed {
            min_seed = seed;
        }
    }

    return min_seed;
}

pub fn compute_part2(data: (Vec<u64>, Vec<Transformer>)) -> u64 {
    let mut min_seed = u64::MAX;
    let (seeds, transformers) = data;
    for s in seeds.chunks(2) {
        let [seed_begin, seed_length]: [u64; 2] = s.try_into().unwrap();
        for mut seed in seed_begin..seed_begin + seed_length {
            for transformer in transformers.iter() {
                for &(dst, src, rng) in transformer.transformations.iter() {
                    if seed >= src && seed < src + rng {
                        seed = dst + (seed - src);
                        break;
                    }
                }
            }
            if seed < min_seed {
                min_seed = seed;
            }
        }
    }

    return min_seed;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sample_part1() {
        let values = read_values_from_file("./sample.txt");
        let value = compute_part1(values);
        let expected_value = 35;
        assert_eq!(expected_value, value);
    }

    #[test]
    fn test_sample_part2() {
        let values = read_values_from_file("./sample.txt");
        let value = compute_part2(values);
        let expected_value = 46;
        assert_eq!(expected_value, value);
    }

}

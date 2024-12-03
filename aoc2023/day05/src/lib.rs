use itertools::Itertools;
use std::fs;
use std::cmp::max;
use std::cmp::min;
use std::vec;

#[derive(Debug, Clone)]
pub struct ClosedInterval {
    pub begin: u64,
    pub end: u64,
}

impl ClosedInterval {
    pub fn new(begin: u64, end: u64) -> ClosedInterval {
        ClosedInterval { begin, end }
    }

    pub fn len(&self) -> u64 {
        self.end - self.begin + 1
    }

    pub fn contains(&self, value: u64) -> bool {
        value >= self.begin && value <= self.end
    }

    pub fn do_overlap(&self, other: &ClosedInterval) -> bool {
        self.end >= other.begin && self.begin <= other.end
    }

    pub fn intersect(&self, other: &ClosedInterval) -> Option<ClosedInterval> {
        if self.end < other.begin || self.begin > other.end {
            return None;
        }
        let begin = max(self.begin, other.begin);
        let end = min(self.end, other.end);
        return Some(ClosedInterval::new(begin, end));
    }

    pub fn non_overlaping_intervals(&self, other: &ClosedInterval) -> Option<Vec<ClosedInterval>> {
        if self.end < other.begin || self.begin > other.end {
            return None;
        }
        let mut intervals: Vec<ClosedInterval> = Vec::new();
        if self.begin < other.begin {
            intervals.push(ClosedInterval::new(self.begin, other.begin - 1));
        } else {
            intervals.push(ClosedInterval::new(other.begin, self.begin - 1));
        }
        if self.end > other.end {
            intervals.push(ClosedInterval::new(other.end + 1, self.end));
        } else {
            intervals.push(ClosedInterval::new(self.end + 1, other.end));
        }
        return Some(intervals);
    }

}


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
        println!("seed_begin: {}, seed_length: {}", seed_begin, seed_length);
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


pub fn compute_part2_using_intervals(data: (Vec<u64>, Vec<Transformer>)) -> u64 {
    let (seeds, transformers) = data;

    // seeds.chunks(2).map(|&[begin,length]| ClosedInterval::new(begin, begin+length-1)).collect::<Vec<ClosedInterval>>();
    
    let mut seeds_intervals = Vec::new();
    for c in seeds.chunks(2) {
        let [begin, length]: [u64; 2] = c.try_into().unwrap();
        seeds_intervals.push(ClosedInterval::new(begin, begin+length-1));
    }

    println!("seeds_intervals: {:?}", seeds_intervals);


    for seeds_interval in seeds_intervals {

        let mut todo: Vec<ClosedInterval> = Vec::new();
        let mut todo_next: Vec<ClosedInterval> = Vec::new();
        let mut done: Vec<ClosedInterval> = Vec::new();
        todo.push(seeds_interval.clone());


        // for each stage
        for transformer in transformers.iter() {

            // for each transformation in a stage
            for &(dst, src, rng) in transformer.transformations.iter() {
                let transformaton_interval = ClosedInterval::new(src, src+rng-1);

                while let Some(current) = todo.pop() {
                    let intersection_interval  = current.intersect(&transformaton_interval);
                    match intersection_interval {
                        Some(interval) => {
                            done.push(ClosedInterval { begin: interval.begin - src + dst, end: interval.end - src + dst });
                        },
                        None => {
                            todo_next.push(current.clone());
                        }
                    }
                    // let non_transformed_intervals: Option<Vec<ClosedInterval>> = current.non_overlaping_intervals(&transformaton_interval);
                    // match non_transformed_intervals {
                    //     Some(intervals) => {
                    //         for interval in intervals {
                    //             todo_next.push(interval);
                    //         }
                    //     },
                    //     None => {
                    //         // nothing to do
                    //     }
                    // }     
                }

                //todo = todo_next;
                for t in todo_next.iter() {
                    todo.push(t.clone());
                }
                todo_next = Vec::new();
                // swap todo and todo_next
            } // end of a stage

            for transformed_interval in todo.iter() {
                done.push(transformed_interval.clone());
            }
        } // end of all stage

        println!("done: {:?}", done);

        let mut a_min_seed = u64::MAX;
        for x in done.iter() {
            if x.begin < a_min_seed {
                a_min_seed = x.begin;
            }   
        }
        println!("a_min_seed: {:?}", a_min_seed);

    }



    let mut min_seed = u64::MAX;
    min_seed = 46;
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

    #[test]
    fn test_sample_part2_using_intervals() {
        let values = read_values_from_file("./sample.txt");
        let value = compute_part2_using_intervals(values);
        let expected_value = 46;
        assert_eq!(expected_value, value);
    }

}

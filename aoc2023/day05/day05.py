from typing import Generator
import sys

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()


def parse_transformer(inputs) -> dict:
    transformations = []
    transformer = { 'title' : next(inputs)[:-1].rstrip(), 'transformations': transformations }

    for line in inputs:
        if line == '':
            break
        transformations.append(list(map(int, line.split())))

    return transformer


def parse_transformers(inputs) -> list:
    transformers = []
    while True:
        try:
            transformers.append(parse_transformer(inputs))
        except StopIteration:
            break
    return transformers


def parse_input_part1(filename : str) -> tuple[list, list]:
    inputs = read_input(filename)

    seeds = list(map(int, next(inputs)[len('seeds: '):].split()))
    next(inputs)

    return seeds, parse_transformers(inputs)


def parse_input_part2(filename : str) -> tuple[list, list]:
    inputs = read_input(filename)

    seeds = []
    it = map(int, next(inputs)[len('seeds: '):].split())
    for s in it:
        seeds.append([s, next(it)])

    next(inputs)

    return seeds, parse_transformers(inputs)



def part1(filename : str) -> int:
    seeds, transformers = parse_input_part1(filename)

    final_seeds = []
    for seed in seeds:
        for transformer in transformers:
            for dst, src, rng in transformer['transformations']:
                if seed >= src and seed < src+rng:
                    seed = dst + (seed - src)
                    break

        final_seeds.append(seed)

    return min(final_seeds)

def part2(filename : str) -> int:
    seeds, transformers = parse_input_part2(filename)

    # final_seeds = []
    min_seed = sys.maxsize

    for s in seeds:
        seed_begin, seed_length = tuple(s)

        for seed in range(seed_begin, seed_begin+seed_length):
            for transformer in transformers:
                for dst, src, rng in transformer['transformations']:
                    if seed >= src and seed < src+rng:
                        seed = dst + (seed - src)
                        break
            if seed < min_seed:
                min_seed = seed

    return min_seed

assert part1('./sample.txt') == 35
assert part1('./input.txt') == 836040384

assert part2('./sample.txt') == 46
# assert part2('./input.txt') == ???

from typing import Generator
import sys

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()

def parse_input(filename : str) -> list:
    return [ parse_game(line) for line in read_input(filename) ]

def parse_game(line : str) -> dict:
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    separator = line.index(':')
    return { 'id': int(line[4:separator]), 'draws': parse_draws(line[separator+1:]) }


def parse_draws(content : str) -> list:
    return [ parse_draw(draw) for draw in content.split(';') ]

def parse_draw(draw_str : str) -> dict:
    draw = {}
    for elt in draw_str.split(','):
        elts = elt.split(' ')
        value = int(elts[1])
        color = elts[2]
        draw[color] = value
    return draw


def validate_game(game : dict, constraints : dict) -> bool:
    return all(draw.get('red', 0) <= constraints['red'] and draw.get('green', 0)<= constraints['green'] and draw.get('blue', 0) <= constraints['blue'] for draw in game['draws'])

def part1(filename : str) -> int:
    games = parse_input(filename)

    constraints = { 'red': 12, 'green': 13, 'blue': 14 }

    count = 0
    for game in games:
        if validate_game(game, constraints):
            count += game['id']
    
    print(count)
    return count


def power_of_min_cubes_for_game(game : dict) -> int:
    min_red = max([ draw.get('red', 0) for draw in game['draws']])
    min_green = max([ draw.get('green', 0) for draw in game['draws']])
    min_blue = max([ draw.get('blue', 0) for draw in game['draws']])

    return min_red * min_green * min_blue

def part2(filename : str) -> int:
    games = parse_input(filename)

    values = [ power_of_min_cubes_for_game(game) for game in games ]
    
    return sum(values)

assert part1('./sample.txt') == 8
assert part1('./input.txt') == 2716

assert part2('./sample.txt') == 2286
assert part2('./input.txt') == 72227


from typing import Generator
from dataclasses import dataclass
from icecream import ic

def read_input(filename : str) -> Generator[str]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()

@dataclass(frozen=True)
class Game:
    '''A game with an id and a list of draws'''
    id: int
    draws: list[dict[str, int]]

def parse_input(filename : str) -> Generator[Game]:
    '''Parse the input file and return a generator of games'''
    return ( parse_game(line) for line in read_input(filename) )

def parse_game(line : str) -> Game:
    '''Parse a line of the input file and return a Game'''
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    separator = line.index(':')
    return Game(int(line[4:separator]), parse_draws(line[separator+1:]))
    # return { 'id': int(line[4:separator]), 'draws': parse_draws(line[separator+1:]) }

def parse_draws(content : str) -> list[dict[str, int]]:
    '''Parse the draws of a game and return a list of draws'''
    return [ parse_draw(draw) for draw in content.split(';') ]

def parse_draw(draw_str : str) -> dict[str, int]:
    '''Parse a draw and return a dictionary with the colors (key) and the number of cubes'''
    draw = {}
    for elt in draw_str.split(','):
        value, color = elt.strip().split(' ')
        draw[color] = int(value)
    return draw

# def parse_draw(draw_str: str) -> dict[str, int]:
#     '''Parse a draw and return a dictionary with the colors (key) and the number of cubes'''
#     return {
#         elts[1]: int(elts[0])
#         for elt in map(str.strip, draw_str.split(',')) for elts in [elt.split(' ')]
#     }

@dataclass(frozen=True)
class Constraints:
    '''Constraints for the game'''
    red: int
    blue: int
    green: int

def validate_game(game : Game, constraints : Constraints) -> bool:
    '''Validate a game against the constraints'''
    return all(draw.get('red', 0) <= constraints.red and draw.get('green', 0)<= constraints.green and draw.get('blue', 0) <= constraints.blue for draw in game.draws)

def part1(filename : str) -> int:
    '''Return the sum of the ids of the games that are valid'''
    games = parse_input(filename)

    # constraints = { 'red': 12, 'green': 13, 'blue': 14 }
    constraints = Constraints(red=12, green=13, blue=14)
    # count = 0
    # for game in games:
    #     if validate_game(game, constraints):
    #         count += game.id

    # return count

    return sum(game.id for game in games if validate_game(game, constraints)) 

def power_of_min_cubes_for_game(game : Game) -> int:
    '''Return the product of the minimum number of cubes of each color for a game'''
    min_red = max([ draw.get('red', 0) for draw in game.draws])
    min_green = max([ draw.get('green', 0) for draw in game.draws])
    min_blue = max([ draw.get('blue', 0) for draw in game.draws])

    return min_red * min_green * min_blue

def part2(filename : str) -> int:
    '''Parse athen compute sum of the product of the minimum number of cubes of each color for each game'''
    games = parse_input(filename)
    values = ( power_of_min_cubes_for_game(game) for game in games )
    
    return sum(values)

# ic.disable()

assert ic(part1('./sample.txt')) == 8
assert ic(part1('./input.txt')) == 2716

assert ic(part2('./sample.txt')) == 2286
assert ic(part2('./input.txt')) == 72227

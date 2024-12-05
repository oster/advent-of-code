from icecream import ic
from itertools import tee
from functools import partial, cmp_to_key


def read_data(filename: str) -> tuple[dict[tuple[int,int], bool], list[list[int]]]:
    with open(filename, "r") as data_file:
        ordering_map = { (a, b): True for a, b in ( tuple(map(int, line.strip().split('|')) ) for line in iter(data_file.readline, '\n') ) }
        updates = [ list(map(int, line.split(','))) for line in data_file ]        
    return ordering_map, updates


def value_at_middle(update: list[int]) -> int:
    return update[len(update) // 2]


def window2(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def part1(filename: str) -> int:
    ordering, updates = read_data(filename)
    return sum(value_at_middle(update) for update in updates if all((u1, u2) in ordering for (u1, u2) in window2(update)))


def compare(ordering_map: dict[tuple[int, int], bool], a: int, b: int) -> int:
    return -1 if ordering_map.get((a, b)) == True else 1


def fix_update(update: list[int], ordering: dict[tuple[int,int], bool]) -> list[int]:
    return sorted(update, key=cmp_to_key(partial(compare, ordering)), reverse=False)


def part2(filename: str) -> int:
    ordering, updates = read_data(filename)
    return sum([value_at_middle(fix_update(update, ordering)) for update in updates if any((u1, u2) not in ordering for (u1, u2) in window2(update))])


assert ic(part1('./sample.txt')) == 143
assert ic(part1('./input.txt')) == 5129

assert ic(part2('./sample.txt')) == 123
assert ic(part2('./input.txt')) == 4077


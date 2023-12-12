from typing import Generator
import array

def read_input(filename : str) -> Generator[str, None, None]:
    with open(filename, 'r') as input_file:
        for line in input_file.readlines():
            yield line.rstrip()


def parse_input(filename : str) -> list[tuple[list[str], list[int]]]:
    input = read_input(filename)
    data = []
    for line in input:
        challenge, records = line.split(' ')
        challenge = list(challenge)
        records = list(map(int, records.split(',')))
        data.append((challenge, records))

    return data


def evaluate(challenge) -> list[int]:
    if type(challenge) == list:
        challenge = ''.join(challenge)
    challenge = list(filter(lambda x: x != '', challenge.replace('?', '.').split('.')))
    return [ len(s) for s in challenge  ] 


# assert evaluate('#.#.###') == [1,1,3]
# assert evaluate('.#...#....###.') ==  [1,1,3]
# assert evaluate('.#.###.#.######') ==  [1,3,1,6]
# assert evaluate('####.#...#...') == [4,1,1]
# assert evaluate('#....######..#####.') == [1,6,5]
# assert evaluate('.###.##....#') == [3,2,1]


global cache
cache = {}

def hashcall(c, nums, idx_c, idx_n):
    return (tuple(c[idx_c:]), tuple(nums[idx_n:]), idx_c, idx_n)


def search(challenge, numbers, idx_c, idx_n) -> int:
    global cache

    numbers_count = len(numbers)
    challenge_count = len(challenge)

    hash_str = hashcall(challenge, numbers, idx_c, idx_n)
    if hash_str in cache:
        return cache[hash_str]

    if idx_n == numbers_count:
        if not '#' in challenge[idx_c:]:
            cache[hash_str] = 1
            return 1
        else:
            cache[hash_str] = 0
            return 0


    num = numbers[idx_n] # number of '#' to insert

    solution_count = 0

    # skip '.'
    while idx_c < challenge_count and challenge[idx_c] == '.':
        idx_c += 1

    if idx_c == challenge_count:
        # assert  len(numbers) - idx_n > 0
        cache[hash_str] = 0
        return 0

    # next char is either a '#' or a '?'
    for next_idx_c in range(idx_c, challenge_count-num+1):
        restart = False

        if '#' in challenge[idx_c:next_idx_c]:
            continue

        # if challenge[next_idx_c] == '.':
        #     continue

        # if next_idx_c-1 > 0 and challenge[next_idx_c-1] == '#':
        #     continue
        
        # try to put a number of '#'
        next_challenge = challenge[:]
        for i in range(num):
            current_c = challenge[next_idx_c+i]

            match current_c:
                case '#':
                    continue
                case '?':
                    next_challenge[next_idx_c+i] = 'X'
                    continue
                case '.':
                    restart = True
                    break

        if restart == True:
            continue

        # fill to keep printing consistent
        # for i in range(idx_c, next_idx_c+num):
        #     if next_challenge[i] == '?':
        #         next_challenge[i] = '.'

        next_idx_c2 = next_idx_c+num

        if next_idx_c2 == challenge_count:
            solution_count += search(next_challenge, numbers, next_idx_c2, idx_n+1)
            continue

        match challenge[next_idx_c2]:
            case '#':
                # bad -> break
                continue
            case '.':
                # good -> skip '.'
                k = next_idx_c2
                while k < challenge_count and challenge[k] == '.':
                    k += 1
                next_idx_c = k
            case '?':
                next_challenge[next_idx_c2] = '.'
                next_idx_c = next_idx_c2 + 1

        solution_count += search(next_challenge, numbers, next_idx_c, idx_n + 1)

    cache[hash_str] = solution_count
    return solution_count


# assert search(list('???.###'), [1,1,3], 0, 0) == 1
# assert search(list('.??..??...?##.'), [1,1,3], 0, 0) == 4
# assert search(list('?#?#?#?#?#?#?#?'), [1,3,1,6], 0, 0) == 1
# assert search(list('????.#...#...'), [4,1,1], 0, 0) == 1
# assert search(list('????.######..#####.'), [1,6,5], 0, 0) == 4
# assert search(list('?###????????'), [3,2,1], 0, 0) == 10


def compute(challenges) -> int:
    res = 0
    for challenge, numbers in challenges:
        res += search(challenge, numbers, 0, 0)

    return res


def part1(filename : str) -> int:
    challenges = parse_input(filename)
    res = compute(challenges)

    return res


def expand(challenges) -> list[tuple[list[str], list[int]]]:
    expanded = []
    for challenge, numbers in challenges:
        challenge = '?'.join([ ''.join(challenge) ] * 5)
        challenge = list(challenge)
        numbers = numbers * 5
        expanded.append((challenge, numbers))

    return expanded


def part2(filename : str) -> int:
    challenges = parse_input(filename)
    challenges = expand(challenges)

    res = compute(challenges)
    return res


assert part1('./sample.txt') == 21
assert part1('./input.txt') == 8419

assert part2('./sample.txt') == 525152
assert part2('./input.txt') == 160500973317706

from typing import Any
from functools import reduce


def die(msg: str):
    raise Exception(msg)


def read_data(filename: str) -> list[str]:
    data = []
    with open(filename, "r") as data_file:
        for line in data_file:
            data.append(line.rstrip())
    return data


closing_for_opening = {"(": ")", "[": "]", "{": "}", "<": ">"}


def is_corrupted(line: str) -> tuple[bool, Any]:
    stack = []

    for s in line:
        if s in "([{<":
            stack.append(s)
            continue

        if stack and closing_for_opening[stack[-1]] == s:
            stack.pop()
            continue

        return (True, s)

    return (False, stack)


score_for_illegal = {")": 3, "]": 57, "}": 1197, ">": 25137}


def part1(filename: str) -> int:
    lines = read_data(filename)

    score = 0
    for line in lines:
        corrupted, illegal = is_corrupted(line)
        if corrupted:
            score += score_for_illegal[illegal]
    return score


assert part1("sample.txt") == 26397
assert part1("input.txt") == 193275


score_for_completion = {")": 1, "]": 2, "}": 3, ">": 4}


def get_score_for_completion(completion: list[str]) -> int:
    return reduce(lambda acc, s: acc * 5 + score_for_completion[s], completion, 0)


def part2(filename: str) -> int:
    lines = read_data(filename)

    line_scores = []
    for line in lines:
        corrupted, to_be_completed = is_corrupted(line)
        if corrupted:
            continue

        to_be_completed = list(
            map(lambda s: closing_for_opening[s], reversed(to_be_completed))
        )
        line_scores.append(get_score_for_completion(to_be_completed))

    line_scores.sort()

    return line_scores[len(line_scores) // 2]


assert part2("sample.txt") == 288957
assert part2("input.txt") == 2429644557

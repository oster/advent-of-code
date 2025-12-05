from icecream import ic


type interval = tuple[int, int]


def read_data(filename: str) -> tuple[list[interval], list[int]]:
    with open(filename, "r") as input_file:
        section_a, section_b = input_file.read().split("\n\n")

        intervals = []
        for line in section_a.split("\n"):
            (start, end) = tuple(map(int, line.split("-")))
            intervals.append((start, end))

        ingredients = [int(line.strip()) for line in section_b.split("\n")]

    return intervals, ingredients


def part1(filename: str) -> int:
    intervals, ingredients = read_data(filename)

    # count = sum(1 for ingredient in ingredients if any(start <= ingredient <= end for start, end in intervals))

    # faster, without comprehension
    count = 0
    for ingredient in ingredients:
        for start, end in intervals:
            if start <= ingredient <= end:
                count += 1
                break

    return count


def union_intervals_disjoints(intervals: list[interval]) -> list[interval]:
    if not intervals:
        return []

    intervals = sorted(intervals, key=lambda x: x[0])

    merged = []
    start, end = intervals[0]

    for n_start, n_end in intervals[1:]:
        if n_start <= end:
            end = max(end, n_end)
        else:
            merged.append((start, end))
            start, end = n_start, n_end

    merged.append((start, end))
    return merged


def part2(filename: str) -> int:
    intervals, _ = read_data(filename)

    intervals = union_intervals_disjoints(intervals)
    count = sum((end - start + 1) for (start, end) in intervals)

    return count


# ic.disable()

assert ic(part1("./sample.txt")) == 3
assert ic(part1("./input.txt")) == 735

assert ic(part2("./sample.txt")) == 14
assert ic(part2("./input.txt")) == 344306344403172

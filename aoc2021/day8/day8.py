from functools import reduce


def die(msg: str):
    raise Exception(msg)


def read_data(filename: str) -> list[tuple[list[str], list[str]]]:
    data = []
    with open(filename, "r") as data_file:
        for line in data_file:
            puzzle, digits = line.rstrip().split(" | ")
            puzzle = puzzle.split(" ")
            digits = digits.split(" ")
            data.append((puzzle, digits))
    return data


def part1(filename: str) -> int:
    data = read_data(filename)
    unique_digit_lengths = [2, 3, 4, 7]
    count = 0
    for _, digits in data:
        count += reduce(
            lambda acc, digit: acc + 1 if len(digit) in unique_digit_lengths else acc,
            digits,
            0,
        )
    return count


assert part1("sample.txt") == 0
assert part1("sample2.txt") == 26
assert part1("input.txt") == 274


def discover_segments_for_digits(hidden_digits: list[str]) -> dict[set[str], int]:
    discovered_digits = [None] * 10
    remaining_digits = []
    to_discover = [set(segments) for segments in hidden_digits]

    some_unique_digit_by_segments_count = {
        2: 1,
        4: 4,
        3: 7,
        7: 8,
    }  # {segments_count: digit}

    for segments in to_discover:
        segment_count = len(segments)
        if segment_count in some_unique_digit_by_segments_count:
            discovered_digits[
                some_unique_digit_by_segments_count[segment_count]
            ] = segments
        else:
            remaining_digits.append(segments)

    # so now, we know segments for digits 1, 4, 7, 8

    to_discover = remaining_digits
    remaining_digits = []
    for segments in to_discover:
        match len(segments):
            case 5:
                if discovered_digits[1].issubset(segments):
                    discovered_digits[3] = segments
                else:
                    remaining_digits.append(segments)
            case 6:
                if not discovered_digits[1].issubset(segments):
                    discovered_digits[6] = segments
                else:
                    remaining_digits.append(segments)
            case _:
                die("unexpected numbers of segments in hidden digit")
    # so now, we know segments for digits 1, 4, 7, 8 then 3, 6

    to_discover = remaining_digits
    for segments in to_discover:
        match len(segments):
            case 5:
                if segments.issubset(discovered_digits[6]):
                    discovered_digits[5] = segments
                else:
                    discovered_digits[2] = segments
            case 6:
                if discovered_digits[3].issubset(segments):
                    discovered_digits[9] = segments
                else:
                    discovered_digits[0] = segments
            case _:
                die("unexpected numbers of segments in hidden digit")

    assert len(discovered_digits) == 10

    # we create a map from segments (string build from ordered segments that constitute the segment) to digits (int)
    discovered_digits = {
        "".join(sorted(segments)): int(digit)
        for digit, segments in enumerate(discovered_digits)
    }
    return discovered_digits


def part2(filename: str) -> int:
    data = read_data(filename)

    sum = 0
    for hidden_digits, puzzle_digits in data:
        discovered_digits = discover_segments_for_digits(hidden_digits)
        num = 0
        for hidden_digit in puzzle_digits:
            digit = discovered_digits["".join(sorted(set(hidden_digit)))]
            num = num * 10 + int(digit)

        sum += num
    return sum


assert part2("sample.txt") == 5353
assert part2("sample2.txt") == 61229
assert part2("input.txt") == 1012089

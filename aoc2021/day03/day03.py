def die(msg: str):
    raise Exception(msg)


def read_data(filename: str) -> list[str]:
    data = []
    with open(filename, "r") as data_file:
        for line in data_file:
            data.append(line.rstrip())

    return data


def part1(filename: str) -> int:
    data = read_data(filename)

    word_len = len(data[0])
    numbers_count = len(data)

    gamma_rate = 0

    for i in range(word_len):
        one_count = sum([int(number[i]) for number in data])
        gamma_rate <<= 1
        if 2 * one_count > numbers_count:
            gamma_rate += 1

    epsilon_rate = ((1 << word_len) - 1) ^ gamma_rate
    return gamma_rate * epsilon_rate


assert part1("sample.txt") == 198
assert part1("input.txt") == 1307354


def filter_for_bit_criteria(
    numbers: list[str],
    word_len: int,
    most_common_criteria: str,
    least_common_criteria: str,
) -> int:
    # co2_scrubber_rate = data
    for i in range(word_len):
        one_count = sum([int(number[i]) for number in numbers])
        if 2 * one_count >= len(numbers):
            # '1' is the most common, therefore '0' is the least common
            criteria = most_common_criteria  #'0'
        else:
            # '0' is the most common, therefore '1' is the least common
            criteria = least_common_criteria  #'1'

        numbers = list(filter(lambda n: n[i] == criteria, numbers))
        if len(numbers) == 1:
            break

    return int(numbers[0], 2)


def part2(filename: str) -> int:
    data = read_data(filename)
    word_len = len(data[0])

    o2_generator_rate = filter_for_bit_criteria(data[:], word_len, "1", "0")
    co2_generator_rate = filter_for_bit_criteria(data, word_len, "0", "1")

    return o2_generator_rate * co2_generator_rate


assert part2("sample.txt") == 230
assert part2("input.txt") == 482500

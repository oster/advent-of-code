from icecream import ic
import math


def read_data(filename: str) -> list[list[str]]:
    data = []
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            values = line.strip().split()
            data.append(values)

    return data


def part1(filename: str) -> int:
    data = read_data(filename)

    problems_count = len(data[0])
    problem_size = len(data) - 1
    operators = data[-1]

    count = 0
    for problem_idx in range(problems_count):
        res = 0
        match operators[problem_idx]:
            case "+":
                res = sum(
                    (
                        int(data[value_idx][problem_idx])
                        for value_idx in range(problem_size)
                    )
                )
            case "*":
                res = math.prod(
                    (
                        int(data[value_idx][problem_idx])
                        for value_idx in range(problem_size)
                    )
                )

        count += res
    return count


def read_data_part2(filename: str) -> tuple[list[str], list[list[int]]]:
    with open(filename, "r") as input_file:
        data = input_file.readlines()
        operators = data[-1].strip().split()
        values_matrix = [line.strip("\n") for line in data[:-1]]

    values = []
    nums = []
    for idx in range(len(values_matrix[0])):
        s = "".join((line[idx] for line in values_matrix)).strip()
        if s:
            n = int(s)
            nums.append(n)
        else:
            values.append(nums)
            nums = []
    values.append(nums)

    return operators, values


def apply(op, nums: list[int]) -> int:
    match op:
        case "+":
            return sum(nums)
        case "*":
            return math.prod(nums)
    return -1


def part2(filename: str) -> int:
    operators, values = read_data_part2(filename)
    return sum((apply(op, numbers) for op, numbers in zip(operators, values)))


# ic.disable()

assert ic(part1("./sample.txt")) == 4277556
assert ic(part1("./input.txt")) == 5381996914800

assert ic(part2("./sample.txt")) == 3263827
assert ic(part2("./input.txt")) == 9627174150897

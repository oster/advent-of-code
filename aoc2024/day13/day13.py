from icecream import ic

def read_data(filename: str) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    values = []
    with open(filename, "r") as data_file:

        machine_specifications = data_file.read().split('\n\n')

        for machine_spec in machine_specifications:
            button_a, button_b, prize = machine_spec.strip().split('\n')

            _, _, button_a_x, button_a_y = button_a.split(' ')
            button_a_x, button_a_y = int(button_a_x[1:-1]), int(button_a_y[1:])

            _, _, button_b_x, button_b_y = button_b.split(' ')
            button_b_x, button_b_y = int(button_b_x[1:-1]), int(button_b_y[1:])

            _, x, y = prize.split(' ')
            x, y = int(x[2:-1]), int(y[2:])

            values.append(((button_a_x, button_a_y), (button_b_x, button_b_y), (x, y)))

    return values


def solve_cramer(a: int, b: int, c: int, d: int, e: int, f: int) -> tuple[bool, int, int]:
    # a b | e
    # c d | f

    det = (a * d) - (b * c)
    assert det != 0

    x = ((e * d) - (b * f)) / det
    y = ((a * f) - (e * c)) / det

    if x.is_integer() and y.is_integer():
        return True, int(x), int(y)
    else:
        # either no solution, or infinite solutions
        return False, 0, 0


def part1(filename: str) -> int:
    values = read_data(filename)

    cost = 0
    for machine in values:
        ((a, c), (b, d), (e, f)) = machine
        ok, x, y = solve_cramer(a, b, c, d, e, f)
        if ok:
            cost += x * 3 + y
    
    return cost


def part2(filename: str) -> int:
    values = read_data(filename)

    cost = 0
    for machine in values:
        ((a, c), (b, d), (e, f)) = machine
        ok, x, y = solve_cramer(a, b, c, d, e + 10000000000000, f + 10000000000000)
        if ok:
            cost += x * 3 + y
    
    return cost


# ic.disable()

assert ic(part1('./sample.txt')) == 480
assert ic(part1('./input.txt')) == 34787

assert ic(part2('./sample.txt')) == 875318608908
assert ic(part2('./input.txt')) == 85644161121698

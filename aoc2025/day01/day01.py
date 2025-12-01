from icecream import ic


def read_data(filename: str) -> list[tuple[str, int]]:
    values = []
    with open(filename, "r") as data_file:
        for l in map(str.strip, data_file.readlines()):
            rotation, clicks = l[0], int(l[1:])
            values.append((rotation, clicks))
    return values

def part1(filename: str) -> int:
    values = read_data(filename)

    dial = 50
    count = 0
    for (rotation, clicks) in values:
        if rotation == 'L':
            clicks = -clicks

        dial = (dial + clicks + 100) % 100
        assert dial >= 0 and dial < 100

        if dial == 0:
            count += 1

    return count


def part2(filename: str) -> int:
    values = read_data(filename)

    dial = 50
    count = 0
    start = dial
    for (rotation, clicks) in values:
        start = dial
        cross_zero = False
        full_loop_count = clicks // 100

        if rotation == 'L':
            clicks = -clicks
            remaining_clicks = clicks % 100 - 100
            assert remaining_clicks < 0
        else:
            remaining_clicks = clicks % 100

        if start + remaining_clicks > 100:
            cross_zero += True
        elif start != 0 and start + remaining_clicks < 0:
            cross_zero += True

        dial = (dial + remaining_clicks + 100) % 100
        assert dial >= 0 and dial < 100

        if dial == 0 and start != 0:
            cross_zero += True

        num_zeros = full_loop_count + (1 if cross_zero else 0)
        count += num_zeros
    return count

# ic.disable()

assert ic(part1("./sample.txt")) == 3
assert ic(part1('./input.txt')) == 1011

assert ic(part2('./sample.txt')) == 6
assert ic(part2('./sample2.txt')) == 10
assert ic(part2('./input.txt')) == 5937

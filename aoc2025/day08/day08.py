from typing import Any
from icecream import ic

type Pos3D = tuple[int, int, int]


def read_data(filename: str) -> Any:
    data = []
    with open(filename, "r") as input_file:
        for line in map(str.strip, input_file.readlines()):
            x, y, z = line.split(",")
            data.append((int(x), int(y), int(z)))

    return data


def dist(p1: Pos3D, p2: Pos3D) -> int:
    (x1, y1, z1) = p1
    (x2, y2, z2) = p2

    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2)
    # return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) + (z1-z2)*(z1-z2))


def merge(a, b, circuits_by_pos, unique_circuits):
    if a not in circuits_by_pos:
        if b not in circuits_by_pos:
            c = {a, b}
            circuits_by_pos[a] = c
            circuits_by_pos[b] = c
            unique_circuits.append(c)
        else:
            c = circuits_by_pos[b]
            c.add(a)
            circuits_by_pos[a] = c
    else:
        if b not in circuits_by_pos:
            c = circuits_by_pos[a]
            c.add(b)
            circuits_by_pos[b] = c
        else:
            circuits_of_a = circuits_by_pos[a]
            circuits_of_b = circuits_by_pos[b]

            if circuits_of_a != circuits_of_b:
                c = circuits_of_a.union(circuits_of_b)

                for v in circuits_of_a:
                    if v != a:
                        circuits_by_pos[v] = c
                for v in circuits_of_b:
                    if v != b:
                        circuits_by_pos[v] = c

                unique_circuits.remove(circuits_of_a)
                unique_circuits.remove(circuits_of_b)

                circuits_by_pos[a] = c
                circuits_by_pos[b] = c

                unique_circuits.append(c)
            else:
                pass


def part1(filename: str, round: int) -> int:
    data = read_data(filename)

    all_pairs = [(dist(p1, p2), p1, p2) for p1 in data for p2 in data if p1 < p2]
    all_pairs = sorted(all_pairs, key=lambda x: x[0])

    circuits_by_pos = {}
    unique_circuits = []

    for _ in range(round):
        if not all_pairs:
            break

        _, a, b = all_pairs.pop(0)
        merge(a, b, circuits_by_pos, unique_circuits)

    k = sorted(unique_circuits, key=lambda c: len(c), reverse=True)
    return len(k[0]) * len(k[1]) * len(k[2])


def part2(filename: str) -> int:
    data = read_data(filename)

    junction_box_count = len(data)

    all_pairs = [(dist(p1, p2), p1, p2) for p1 in data for p2 in data if p1 < p2]
    all_pairs = sorted(all_pairs, key=lambda x: x[0])

    circuits_by_pos = {}
    unique_circuits = []

    while True:
        if not all_pairs:
            break

        _, a, b = all_pairs.pop(0)
        merge(a, b, circuits_by_pos, unique_circuits)
        if len(circuits_by_pos) == junction_box_count:  # and len(unique_circuits) == 1:
            return a[0] * b[0]

    return -1


# ic.disable()

assert ic(part1("./sample.txt", 10)) == 40
assert ic(part1("./input.txt", 1000)) == 171503

assert ic(part2("./sample.txt")) == 25272
assert ic(part2("./input.txt")) == 9069509600

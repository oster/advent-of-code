from typing import Any, Sequence
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


classes: list[tuple[list[int], int, int]] = []
representatives = []

def init(values: Sequence[int]) -> None:
    global classes
    global representatives
    classes = [ None ] * len(values)
    representatives = [ -1 ] * len(values)
    for idx, v in enumerate(values):
        classes[idx] = ([v], idx, 1,)
        representatives[idx] = idx


def find(v: int) -> int:
    return representatives[v]


def union(i: int, j: int) -> int:
    global classes

    if representatives[i] == representatives[j]:
        return representatives[i]

    members_classe_i, idx_representative_i, sizeof_members_classe_i = classes[representatives[i]]


    assert representatives[i] == idx_representative_i
    members_classe_j, idx_representative_j, sizeof_members_classe_j = classes[representatives[j]]
    assert representatives[j] == idx_representative_j

    if sizeof_members_classe_i <= sizeof_members_classe_j:
        # append i to j
        for c_idx in members_classe_i:
            representatives[c_idx] = idx_representative_j

        members_classe_j.extend(members_classe_i)
        classes[representatives[j]] = members_classe_j, idx_representative_j, sizeof_members_classe_j + sizeof_members_classe_i
        representatives[i] = idx_representative_j
        return idx_representative_j
    else:
        # append j to i
        members_classe_i.extend(members_classe_j)

        for c_idx in members_classe_j:
            representatives[c_idx] = idx_representative_i

        classes[representatives[i]] = members_classe_i, idx_representative_i, sizeof_members_classe_i + sizeof_members_classe_j
        representatives[j] = idx_representative_i
        return idx_representative_i


def classes_sizes() -> list[int]:
    # Consider only representative classes to avoid stale sizes from merged nodes.
    sizes = [classes[rep][2] for rep in sorted(set(representatives))]
    sizes.sort(reverse=True)
    return sizes


def part1(filename: str, round: int) -> int:
    data = read_data(filename)

    all_pairs = ((dist(p1, p2), idx_p1, idx_p2) for idx_p1, p1 in enumerate(data) for idx_p2, p2 in enumerate(data) if p1 < p2)
    all_pairs = sorted(all_pairs, key=lambda x: x[0])


    init([idx for idx,_  in enumerate(data)])

    for _, a, b in all_pairs:
        round -= 1
        union(a, b)
        if round == 0:
            break

    rep_sizes = classes_sizes()
    return rep_sizes[0] * rep_sizes[1] * rep_sizes[2]


def part2(filename: str) -> int:
    data = read_data(filename)

    junction_box_count = len(data)

    all_pairs = ( (dist(p1, p2), idx_p1, idx_p2) for idx_p1, p1 in enumerate(data) for idx_p2, p2 in enumerate(data) if p1 < p2 )
    all_pairs = sorted(all_pairs, key=lambda x: x[0])
    points = [ p for _, p  in enumerate(data) ]

    init([idx for idx,_  in enumerate(data)])

    for _, a, b in all_pairs:
        u = union(a, b)
        _, _, sizeof_c = classes[u]
        if  sizeof_c == junction_box_count:
            return points[a][0] * points[b][0]

    return -1


# ic.disable()

assert ic(part1("./sample.txt", 10)) == 40
assert ic(part1("./input.txt", 1000)) == 171503

assert ic(part2("./sample.txt")) == 25272
assert ic(part2("./input.txt")) == 9069509600

assert ic(r := part1("./input2.txt", 1000)) == 117000, f'got {r}'
assert ic(r := part2("./input2.txt")) == 8368033065, f'got {r}'

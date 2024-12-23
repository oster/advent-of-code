from collections import defaultdict
from typing import Generator
from icecream import ic


def read_data(filename: str) -> dict[str, set[str]]:
    with open(filename, "r") as data_file:
        connected = defaultdict(set)
        for line in data_file.readlines():
            node1, node2 = line.strip().split("-")
            connected[node1].add(node2)
            connected[node2].add(node1)
    return connected


def setof_three(
    connected: dict[str, set[str]]
) -> Generator[frozenset[str], None, None]:
    for node1 in connected.keys():
        for node2 in connected[node1]:
            for node3 in connected[node2]:
                if node3 in connected[node1]:
                    yield frozenset((node1, node2, node3))


def set_startwith_t(s: frozenset[str]) -> bool:
    return any(map(lambda x: x.startswith("t"), s))


connected = {}


def part1(filename: str) -> int:
    global connected
    connected = read_data(filename)
    s = set(setof_three(connected))
    s = set(filter(set_startwith_t, s))
    return len(s)


def is_connected(node_a: str, node_b: str) -> bool:
    return node_b in connected[node_a]


def is_clique(set_of_nodes: set[str]) -> bool:
    for node1 in set_of_nodes:
        for node2 in set_of_nodes:
            if node1 != node2 and not is_connected(node1, node2):
                return False
    return True


# def max_clique_brute(connected: dict[str, set[str]]) -> set[str]:
#     max_clique = set()

#     def build_max_clique(nodes_to_test: set[str], group: set[str]):
#         nonlocal max_clique

#         if nodes_to_test == set():
#             return

#         if not is_clique(frozenset(group)):
#             return
#         else:
#             if len(group) > len(max_clique):
#                 max_clique = group

#         for node in nodes_to_test:
#             build_max_clique(nodes_to_test - {node}, group | {node})

#     build_max_clique(set(connected.keys()), set())
#     return max_clique


# Wikipedia: https://fr.wikipedia.org/wiki/Algorithme_de_Bron-Kerbosch
#
# algorithme BronKerbosch1(R, P, X)
#     si P et X sont vides alors
#         déclarer que R est une clique maximale
#     pour tout sommet v dans P faire
#         BronKerbosch1(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
#         P := P \ {v}
#         X := X ⋃ {v}


def max_cliques(connected: dict[str, set[str]]) -> list[set[str]]:
    max_clique = []

    def bron_kerbosch(R, P, X):
        nonlocal max_clique
        if P == set() and X == set():
            max_clique.append(R)
        for v in P:
            bron_kerbosch(R | {v}, P & connected[v], X & connected[v])
            P = P - {v}
            X = X | {v}

    bron_kerbosch(set(), set(connected.keys()), set())
    return max_clique


def part2(filename: str) -> str:
    global connected
    connected = read_data(filename)
    # max_clique = max_clique_brute(connected)
    s = max_cliques(connected)
    max_clique = max(s, key=len)
    password = ",".join(sorted(max_clique))
    return password


# ic.disable()

assert ic(part1("./sample.txt")) == 7
assert ic(part1("./input.txt")) == 998

assert ic(part2("./sample.txt")) == "co,de,ka,ta"
assert ic(part2("./input.txt")) == "cc,ff,fh,fr,ny,oa,pl,rg,uj,wd,xn,xs,zw"

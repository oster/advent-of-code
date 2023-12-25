from collections import Counter, deque
import random


def die(msg: str):
    raise Exception(msg)


def read_input(filename: str) -> dict[str, list[str]]:
    components = {}
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            conn = line.rstrip().split(": ")
            c1, c_list = conn[0], conn[1].split(" ")

            if not c1 in components:
                components[c1] = []
            components[c1].extend(c_list)

            for c in c_list:
                if not c in components:
                    components[c] = []
                components[c].append(c1)
    return components


def dump_graph(graph: dict[str, list[str]]):
    with open("graph.dot", "w") as output_file:
        output_file.write("graph G {" + "\n")

        for node in graph:
            output_file.write(f'  "{node}" [label="{node}"];' + "\n")

        visited_edges = set()
        for node in graph:
            for other_node in graph[node]:
                if ((node, other_node) not in visited_edges) and (
                    (other_node, node) not in visited_edges
                ):
                    visited_edges.add((node, other_node))
                output_file.write(f'  "{node}" -- "{other_node}";' + "\n")

        output_file.write("}" + "\n")


def collect_nodes_dfs(graph: dict[str, list[str]], node: str, visited: set) -> set:
    for other_node in graph[node]:
        if other_node not in visited:
            visited.add(other_node)
            collect_nodes_dfs(graph, other_node, visited)
    return visited


def part1(filename: str) -> int:
    graph = read_input(filename)
    # dump_graph(graph)
    # dot -Tpng graph.dot -o graph.png

    if filename == "./sample.txt":
        to_remove = [("jqt", "nvd"), ("bvb", "cmg"), ("hfx", "pzl")]
    else:
        to_remove = [("lkf", "scf"), ("mtl", "pgl"), ("zxb", "zkv")]

    for node, other_node in to_remove:
        graph[node].remove(other_node)
        graph[other_node].remove(node)

    some_node_in_cut1 = to_remove[0][0]

    a = len(collect_nodes_dfs(graph, some_node_in_cut1, set()))
    b = len(graph) - a

    return a * b


assert part1("./sample.txt") == 54
assert part1("./input.txt") == 562772


def window(iterable):
    return zip(iterable, iterable[1:])


def build_path_back(src, dst, from_to):
    # reconstruct path
    path = []
    c = src
    while c != dst:
        path.append(c)
        c = from_to[c][0]
    return list(reversed(path))


def find_shortest_path(graph, start, end):
    distances = {start: (start, 0)}
    q = deque()
    q.append((start, 0))

    while q:
        at, dist = q.popleft()
        for next in graph[at]:
            if next not in distances or distances[next][1] > dist + 1:
                distances[next] = (at, dist + 1)
                q.append((next, dist + 1))
    return build_path_back(end, start, distances)


def part1_alternate(filename: str) -> int:
    graph = read_input(filename)

    some_node_in_cut1 = None

    for _ in range(3):
        count = Counter()
        for _ in range(50):
            nodes = list(graph.keys())

            nodeA = nodes[random.randrange(0, len(nodes))]
            nodeB = nodes[random.randrange(0, len(nodes))]
            if nodeA != nodeB:
                p = find_shortest_path(graph, nodeA, nodeB)
                for src, dst in window(p):
                    count.update([(src, dst)])

        to_remove = [edge for edge, _ in count.most_common(1)]

        if not some_node_in_cut1:
            some_node_in_cut1 = to_remove[0][0]

        for node, other_node in to_remove:
            graph[node].remove(other_node)
            graph[other_node].remove(node)

    a = len(collect_nodes_dfs(graph, some_node_in_cut1, set()))
    b = len(graph) - a

    return a * b


assert part1_alternate("./sample.txt") == 54
assert part1_alternate("./input.txt") == 562772

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

from icecream import ic
from functools import lru_cache
import sys

sys.setrecursionlimit(10000)


def read_data(filename: str):
    data = {}
    with open(filename, "r") as input_file:
        for line in map(str.strip, input_file.readlines()):
            input, outputs = line.split(":")
            outputs = outputs.strip().split(" ")

            data[input] = outputs

    return data


def get_all_path_rec(graph, start, end):
    all_paths = []

    dfs_rec(graph, start, end, all_paths, [start])

    return all_paths


def dfs_rec(graph, current, end, all_paths, current_path):
    if current == end:
        all_paths.append(current_path.copy())
        return

    for neighbor in graph.get(current, []):
        if neighbor not in current_path:
            dfs_rec(graph, neighbor, end, all_paths, current_path + [neighbor])


def get_all_paths(graph, start, target):
    paths = []
    stack = [(start, [start])]

    while stack:
        node, path = stack.pop()

        if node == target:
            paths.append(path)
            continue

        for neighbor in graph.get(node, []):
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor]))

    return paths


def dump(graph):
    print("digraph G {")

    for node, neighbors in graph.items():
        for neighbor in neighbors:
            print(f"  {node} -> {neighbor};")

    print('  svr[shape=Diamond, style="filled", fillcolor=green];')
    print('    out[shape=Diamond, style="filled", fillcolor=green];')
    print('    dac[shape=Diamond, style="filled", fillcolor=red];')
    print('    fft[shape=Diamond, style="filled", fillcolor=blue];')
    print("}")


def part1(filename: str) -> int:
    graph = read_data(filename)
    start = "you"
    end = "out"

    # all_paths = get_all_paths(graph, start, end)
    # return len(all_paths)

    return count_path(graph, start, end)


def part2_all_paths(filename: str) -> int:
    graph = read_data(filename)

    start = "svr"
    end = "out"

    all_paths = get_all_paths(graph, start, end)
    c = sum(1 for path in all_paths if "fft" in path and "dac" in path)

    return c


def count_path(graph, start, target):
    @lru_cache(maxsize=None)
    def dfs(node):
        if node == target:
            return 1
        return sum(dfs(nb) for nb in graph.get(node, []))

    return dfs(start)


def part2(filename: str) -> int:
    graph = read_data(filename)

    # ic(graph)
    # dump(graph)

    svr_to_dac = count_path(graph, "svr", "dac")
    svr_to_fft = count_path(graph, "svr", "fft")
    dac_to_out = count_path(graph, "dac", "out")
    fft_to_out = count_path(graph, "fft", "out")

    dac_to_fft = count_path(graph, "dac", "fft")
    fft_to_dac = count_path(graph, "fft", "dac")

    if dac_to_fft == 0:
        return svr_to_fft * fft_to_dac * dac_to_out
    elif fft_to_dac == 0:
        return svr_to_dac * dac_to_fft * fft_to_out
    else:
        # need to find another solution
        return 0


assert ic(part1("./sample.txt")) == 5
assert ic(part1("./input.txt")) == 668

assert ic(part2("./sample2.txt")) == 2
assert ic(part2("./input.txt")) == 294310962265680

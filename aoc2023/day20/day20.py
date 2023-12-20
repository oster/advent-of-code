from collections import deque
import math
from typing import Any


def die(msg: str):
    """Prints an error message and exits the program"""
    raise Exception(msg)


type Component = dict[str, Any]


# broadcaster
def create_broadcaster(name: str, output: list[str]) -> Component:
    return {
        "type": "broadcaster",
        "name": name,
        "output": output,
    }


# %
def create_flipflop(name: str, output: list[str]) -> Component:
    return {
        "type": "flipflop",
        "name": name,
        "output": output,
        "state": False,
    }


#
def create_conjunction(name: str, output: list[str]) -> Component:
    return {
        "type": "conjunction",
        "name": name,
        "output": output,
        "mem": {},
    }


def create_dummy(name: str) -> Component:
    return {
        "type": "dummy",
        "name": name,
        "output": [],
    }


def read_input_part1(filename: str) -> dict[str, Component]:
    components = {}
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            typed_name, output = line.rstrip().split(" -> ")

            c = None
            if typed_name == "broadcaster":
                c = create_broadcaster(typed_name, output.split(", "))
            elif typed_name.startswith("%"):
                c = create_flipflop(typed_name[1:], output.split(", "))
            elif typed_name.startswith("&"):
                c = create_conjunction(typed_name[1:], output.split(", "))

            components[c["name"]] = c
    return components


def dump(components: dict[str, Component]):
    for component in components.values():
        if component["type"] == "conjunction":
            print(
                f'{component["name"]}:{"".join([ "1" if v else "0" for v in component["mem"].values()])}',
                end=", ",
            )
        if component["type"] == "flipflop":
            print(f'{component["name"]}:{1 if component["state"] else 0}', end=", ")
    print()


def part1(filename: str) -> int:
    components = read_input_part1(filename)

    # for component in components.values():
    #     print(component)

    # init memory of each conjunction components
    for component in list(components.values()):
        for connection in component["output"]:
            if connection not in components:
                components[connection] = create_dummy(connection)

            connected_to = components[connection]
            if connected_to["type"] == "conjunction":
                connected_to["mem"][component["name"]] = False

    low_pulses = 0
    high_pulses = 0
    pulses = deque()

    for _ in range(1000):
        pulses.append(("broadcaster", False, "button"))

        while pulses:
            dest, pulse_level, src = pulses.popleft()
            # print(f"{src} {'-high' if pulse_level else '-low'}-> {dest}")

            if pulse_level:
                high_pulses += 1
            else:
                low_pulses += 1

            component = components[dest]

            match component["type"]:
                case "broadcaster":
                    for target in component["output"]:
                        pulses.append((target, pulse_level, "broadcaster"))
                case "flipflop":
                    if pulse_level:
                        pass
                    else:
                        component["state"] = not component["state"]
                        for target in component["output"]:
                            pulses.append(
                                (target, component["state"], component["name"])
                            )
                case "conjunction":
                    component["mem"][src] = pulse_level
                    pulse_level_to_send = not all(component["mem"].values())
                    for target in component["output"]:
                        pulses.append((target, pulse_level_to_send, component["name"]))
                case "dummy":
                    pass
                case _:
                    die(f"Unknown component type {component['type']}")

    return high_pulses * low_pulses


assert part1("./sample.txt") == 32000000
assert part1("./sample2.txt") == 11687500


def lcm(a: int, b: int) -> int:
    # Lowest Common Multiple
    return a * b // math.gcd(a, b)


def lcms(values: list[int]):
    llcm = 1
    for v in values:
        llcm = lcm(llcm, v)
    return llcm


def part2(filename: str) -> int:
    components = read_input_part1(filename)

    # for component in components.values():
    #     print(component)

    # init memory of each conjunction components
    for component in list(components.values()):
        for connection in component["output"]:
            if connection not in components:
                components[connection] = create_dummy(connection)

            connected_to = components[connection]
            if connected_to["type"] == "conjunction":
                connected_to["mem"][component["name"]] = False

    pulses = deque()

    last_vf = 0
    last_mk = 0
    last_dh = 0
    last_rn = 0

    count = 0
    while True:
        count += 1

        pulses.append(("broadcaster", False, "button"))

        while pulses:
            dest, pulse_level, src = pulses.popleft()

            # according to the graph, the only way to get a rx low pulse is
            # when jz has received high pulses from all its inputs (vf, mk, dh, rn)
            # this is visible in the graph, using to_dot.py on input.txt
            if dest == "jz":
                if src == "vf" and pulse_level:  # print(f'count vf: {count-last_vf}')
                    last_vf = count
                if src == "mk" and pulse_level:
                    last_mk = count
                if src == "dh" and pulse_level:
                    last_dh = count
                if src == "rn" and pulse_level:
                    last_rn = count

                if last_vf > 0 and last_mk > 0 and last_dh > 0 and last_rn > 0:
                    # print(f'last_vf: {last_vf}, last_mk: {last_mk}, last_dh: {last_dh}, last_rn: {last_rn}')
                    # return lcms([last_vf, last_mk, last_dh, last_rn])
                    # since they are prime numbers
                    return last_vf * last_mk * last_dh * last_rn

            component = components[dest]

            match component["type"]:
                case "broadcaster":
                    for target in component["output"]:
                        pulses.append((target, pulse_level, "broadcaster"))
                case "flipflop":
                    if pulse_level:
                        pass
                    else:
                        component["state"] = not component["state"]
                        for target in component["output"]:
                            pulses.append(
                                (target, component["state"], component["name"])
                            )
                case "conjunction":
                    component["mem"][src] = pulse_level
                    pulse_level_to_send = not all(component["mem"].values())
                    for target in component["output"]:
                        pulses.append((target, pulse_level_to_send, component["name"]))
                case "dummy":
                    pass
                case _:
                    die(f"Unknown component type {component['type']}")


assert part2("./input.txt") == 247023644760071

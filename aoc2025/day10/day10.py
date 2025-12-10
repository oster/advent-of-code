from collections import deque
from icecream import ic
from z3 import *

def read_data(filename: str):
    data = []
    with open(filename, "r") as input_file:
        for line in map(str.strip, input_file.readlines()):

            spec = line.split(' ')

            lights = [c == '#' for c in spec[0][1:-1]]

            buttons = []
            for button_spec in spec[1:-1]:
                buttons.append([ int(b_s) for b_s in button_spec[1:-1].split(',')])

            jolts = list(map(int, spec[-1][1:-1].split(',')))
            data.append((lights, buttons, jolts))
    return data


def solve_machine(expected_lights, buttons) -> int:
    states = deque()

    visited = set()

    lights = tuple([ False ] * len(expected_lights))
    states.append((0, lights))
    step = 0

    while True:
        step, state = states.popleft()

        if state == expected_lights:
            break
        
        for b in buttons:
            updated_lights = list(state)
            for s in b:
                updated_lights[s] = not updated_lights[s] 

            new_state = tuple(updated_lights)
            if new_state in visited:
                continue
            visited.add(new_state)
            states.append((step + 1, new_state))
    return step


def part1(filename: str) -> int:
    machines = read_data(filename)

    count = 0
    for (expected_light, buttons, _) in machines:
        step = solve_machine(tuple(expected_light), buttons)

        count += step
    return count



def solve_machine2_bfs(expected_counters, buttons) -> int:
    states = deque()

    counters = tuple([ 0 ] * len(expected_counters))

    states.append((0, counters))
    step = 0
    while True:
        step, state = states.popleft()

        # ic(state)

        if state == expected_counters:
            break
        
        for b in buttons:
            updated_counters = list(state)
            for s in b:
                updated_counters[s] = updated_counters[s] + 1
            new_state = tuple(updated_counters)
            states.append((step + 1, new_state))
    return step


def solve_machine2(excepted_counters, buttons) -> int:
    m = []
    for l in excepted_counters:
        l = [ None ] * len(buttons)
        m.append(l)
        
    button_names = set()
    for idx_b, b in enumerate(buttons):
        name = f'B{idx_b}'

        for _, v in enumerate(b):
            m[v][idx_b] = name
        button_names.add(name)

    # ic(m)
    # ic(excepted_counters)
    # input()


    buttons_vars = {name: Int(name) for name in button_names}

    # s = Solver()
    s = Optimize()
    
    for v in buttons_vars.values():
        s.add(v >= 0)

    # for name in var_names:
    #     s.minimize(z3_vars[name])

    for i, row in enumerate(m):
        expr = 0
        for c in row:
            if c != None:
                expr += buttons_vars[c]
        s.add(expr == excepted_counters[i])

    total = Sum([buttons_vars[name] for name in button_names])
    s.minimize(total)


    if s.check() == "sat":
        die("Cannot solve the problem.")
    m = s.model()

    s = 0
    for name in button_names:
        s += m[buttons_vars[name]].py_value()
    
    return s


def part2(filename: str) -> int:
    machines = read_data(filename)

    count = 0
    for (_, buttons, excepted_counters) in machines:
        step = solve_machine2(tuple(excepted_counters), buttons)

        # ic(step)
        count += step
    return count

# ic.disable()


assert ic(part1("./sample.txt")) == 7
assert ic(part1("./input.txt")) == 477

assert ic(part2("./sample.txt")) == 33
assert ic(part2("./input.txt")) == 17970

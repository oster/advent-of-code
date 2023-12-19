import sys
from typing import Any
from functools import partial

# sys.setrecursionlimit(100000)


def die(msg: str):
    """Prints an error message and exits the program"""
    raise Exception(msg)


def apply(workflows : dict[str, Any], workflow_name: str, value : Any) -> Any:
    return workflows[workflow_name](value=value)

def inf(workflows : dict[str, Any], var: str, cond: int, f: Any, g: Any, value : Any) -> Any:
    if value[var] < cond:
        f(value=value)
    else:
        g(value=value)

def sup(workflows : dict[str, Any], var: str, cond: int, f: Any, g: Any, value : Any) -> Any:
    if value[var] > cond:
        f(value=value)
    else:
        g(value=value)
    


sum_part_1 = 0
def accept_part1(workflows : dict[str, Any], value : Any) -> Any:
    global sum_part_1
    sum_part_1 += value['x'] + value['m'] + value['a'] + value['s']


def reject(workflows : dict[str, Any], value : Any) -> Any:
    return 


def parse_line(line: str, workflows : dict[str, Any], accept_function) -> tuple[str, Any]:
    name, rest = line.rstrip().rstrip("}").split("{")

    function = None

    reject_function = partial(reject, workflows=workflows)

    last_op = None

    for op in reversed(rest.rstrip("}").split(",")):
        match op:
            case 'A':
                function = partial(accept_function, workflows=workflows)
            case 'R':
                function = partial(reject, workflows=workflows)
            case _:
                if '>' in op:
                    var, rest = op.split('>')
                    cond, workflow_name = rest.split(':')
                    if workflow_name == 'A':
                        f=accept_function
                    elif workflow_name == 'R':
                        f=reject_function
                    else:
                        f=partial(apply, workflows=workflows, workflow_name=workflow_name)
                    function = partial(sup, workflows=workflows, var=var, cond=int(cond), f=f, g=last_op)
                elif '<' in op:
                    var, rest = op.split('<')
                    cond, workflow_name = rest.split(':')
                    if workflow_name == 'A':
                        f=accept_function
                    elif workflow_name == 'R':
                        f=reject_function
                    else:
                        f=partial(apply, workflows=workflows, workflow_name=workflow_name)
                    function = partial(inf, workflows=workflows, var=var, cond=int(cond), f=f, g=last_op)
                else:
                    workflow_name = op
                    function = partial(apply, workflows=workflows, workflow_name=workflow_name)
        last_op = function

    return name, last_op


def read_input_part1(filename: str) -> tuple[dict[str,Any], list[int]]:
    workflows = {}
    values = []

    accept_function = partial(accept_part1, workflows=workflows)


    with open(filename, "r") as input_file:
        lines = input_file.readlines().__iter__()

        line = next(lines).rstrip()
        while line != '\n':
            workflow_name, workflow_function = parse_line(line, workflows, accept_function)
            workflows[workflow_name] = workflow_function
            line = next(lines)

        for line in lines:
            line = line.rstrip()

            x, m, a, s = line.rstrip()[1:-1].split(",")
            value = { 'x': int(x[2:]), 'm': int(m[2:]), 'a': int(a[2:]), 's': int(s[2:]) }
            values.append(value)

    return workflows, values


def part1(filename: str) -> int:
    global sum_part_1
    sum_part_1 = 0

    workflows, values = read_input_part1(filename)

    for value in values:
        workflows['in'](value=value)

    return sum_part_1


assert part1("./sample.txt") == 19114
assert part1("./input.txt") == 342650


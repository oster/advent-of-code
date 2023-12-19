from typing import Any, Callable, Iterator
from functools import partial


def die(msg: str):
    """Prints an error message and exits the program"""
    raise Exception(msg)


def parse_task(
    line: str, tasks: dict[str, Callable], accept: Callable, reject: Callable, inf: Callable, sup: Callable
) -> tuple[str, Any]:
    name, rest = line.rstrip().rstrip("}").split("{")
    last_function = None
    for op in reversed(rest.rstrip("}").split(",")):
        function = None
        if op == "A":
            function = accept
        elif op == "R":
            function = reject
        elif ">" in op:
            var, rest = op.split(">")
            cond, task_name = rest.split(":")
            if task_name == "A":
                f = accept
            elif task_name == "R":
                f = reject
            else:
                f = partial(apply, tasks=tasks, task_name=task_name)
            function = partial(sup, var=var, cond=int(cond), f=f, g=last_function)
        elif "<" in op:
            var, rest = op.split("<")
            cond, task_name = rest.split(":")
            if task_name == "A":
                f = accept
            elif task_name == "R":
                f = reject
            else:
                f = partial(apply, tasks=tasks, task_name=task_name)
            function = partial(inf, var=var, cond=int(cond), f=f, g=last_function)
        else:
            task_name = op
            function = partial(apply, tasks=tasks, task_name=task_name)
        last_function = function

    return name, last_function


def parse_tasks(lines: Iterator[str], tasks: dict[str, Callable], accept: Callable, reject: Callable, inf: Callable, sup: Callable):
    line = next(lines).rstrip()
    while line != "\n":
        task_name, task_function = parse_task(line, tasks, accept, reject, inf, sup)
        tasks[task_name] = task_function
        line = next(lines)


def parse_values(lines: Iterator[str]) -> list[Any]:
    values = []
    for line in lines:
        line = line.rstrip()

        x, m, a, s = line.rstrip()[1:-1].split(",")
        value = {"x": int(x[2:]), "m": int(m[2:]), "a": int(a[2:]), "s": int(s[2:])}
        values.append(value)
    return values


def reject(value: Any) -> int:
    return 0


def apply(tasks: dict[str, Callable], task_name: str, value: Any) -> int:
    return tasks[task_name](value=value)


def part1(filename: str) -> int:
    tasks = {}
    values = []

    def inf_part1(var: str, cond: int, f: Callable, g: Callable, value: Any) -> int:
        if value[var] < cond:
            return f(value=value)
        else:
            return g(value=value)

    def sup_part1(var: str, cond: int, f: Callable, g: Callable, value: Any) -> int:
        if value[var] > cond:
            return f(value=value)
        else:
            return g(value=value)

    def accept_part1(value: Any) -> int:
        return value["x"] + value["m"] + value["a"] + value["s"]

    with open(filename, "r") as input_file:
        parse_tasks(input_file, tasks, accept_part1, reject, inf_part1, sup_part1)
        values = parse_values(input_file)

    return sum(tasks["in"](value=value) for value in values)


assert part1("./sample.txt") == 19114
assert part1("./input.txt") == 342650


def part2(filename: str) -> int:
    def accept_part2(value: Any) -> int:
        return (
            (value["x"][1] - value["x"][0] + 1)
            * (value["m"][1] - value["m"][0] + 1)
            * (value["a"][1] - value["a"][0] + 1)
            * (value["s"][1] - value["s"][0] + 1)
        )

    def inf_part2(var: str, cond: int, f: Callable, g: Callable, value: Any) -> int:
        min, max = value[var]
        v = value.copy()
        v[var] = (min, cond - 1)
        left = f(value=v)
        v[var] = (cond, max)
        right = g(value=v)
        return left + right

    def sup_part2(var: str, cond: int, f: Callable, g: Callable, value: Any) -> int:
        min, max = value[var]
        v = value.copy()
        v[var] = (cond + 1, max)
        left = f(value=v)
        v[var] = (min, cond)
        right = g(value=v)
        return left + right

    tasks = {}
    with open(filename, "r") as input_file:
        parse_tasks(input_file, tasks, accept_part2, reject, inf_part2, sup_part2)

    interval = (1, 4000)
    initial_value = {"x": interval, "m": interval, "a": interval, "s": interval}

    return tasks["in"](value=initial_value)


assert part2("./sample.txt") == 167409079868000
assert part2("./input.txt") == 130303473508222

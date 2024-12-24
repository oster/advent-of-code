from functools import reduce
from icecream import ic

from sys import setrecursionlimit

setrecursionlimit(1000)

def read_data(filename: str) -> list[int]:
    circuit = {}
    with open(filename, "r") as data_file:
        data = data_file.read()
        initial_state, rules = data.split("\n\n")

        for wire_state in initial_state.split("\n"):
            wire, state = wire_state.strip().split(": ")
            circuit[wire] = bool(int(state))

        for connection in rules.split("\n"):
            if not connection:
                continue
            inputs, output = connection.split(" -> ")
            inputs = inputs.split(" ")
            circuit[output] = (inputs[1], inputs[0], inputs[2])

    return circuit




def evaluate(circuit: dict[str, tuple[str, str, str]], wire: str) -> bool:
    if type(circuit[wire]) == bool:
        assert circuit[wire] == True or circuit[wire] == False
        return circuit[wire]
    
    match circuit[wire]:
        case ("AND", i1, i2):
            return evaluate(circuit, i1) & evaluate(circuit, i2)
        case ("OR", i1, i2):
            return evaluate(circuit, i1) | evaluate(circuit, i2)
        case ("XOR", i1, i2):
            return evaluate(circuit, i1) ^ evaluate(circuit, i2)
        case _:
            raise ValueError(f"Unknown operation: {circuit[wire]}")


def run(circuit: dict[str, tuple[str, str, str]], name: str) -> dict[str, bool]:
    outputs = [ k for k, _ in circuit.items() if k.startswith(name) ]

    res = {}
    for o in outputs:
        res[o] = evaluate(circuit, o)
    return res


def dump_register(registers: dict[str, bool], letter: str) -> None:
    print(f'{letter}: ', end="")
    for k, v in sorted(registers.items(), key=lambda x: x[0], reverse=True):
        # print(f"{k}: {v}")
        s = "1" if v else "0"
        print(f"{s}", end="")
    print(' = ', evaluate_register(registers))


def evaluate_register(registers: dict[str, bool]) -> int:
    bits = sorted(registers.items(), key=lambda x: x[0], reverse=True)
    val = reduce(lambda acc, x: acc << 1 | x, [int(v) for k, v in bits], 0)
    return val


def part1(filename: str) -> int:
    circuit = read_data(filename)
    # ic(circuit)

    registers = run(circuit, 'z')
    # dump_register(registers, 'z')
    val = evaluate_register(registers)

    return val



def swap(a: str, b: str, circuit: dict[str, tuple[str, str, str]]) -> None:
    circuit[a], circuit[b] = circuit[b], circuit[a]


def part2_sample(filename: str) -> int:
    circuit = read_data(filename)
    # ic(circuit)

    gates = { k: v for k, v in circuit.items() if type(v) != bool }

    for g1 in gates:
        for g2 in gates:
            if g1 == g2:
                continue
            swap(g1, g2, circuit)
            for g3 in gates:
                if g1 == g3 or g2 == g3:
                    continue
                for g4 in gates:
                    if g1 == g4 or g2 == g4 or g3 == g4:
                        continue
                    swap(g3, g4, circuit)

                    x_registers = run(circuit, 'x')
                    y_registers = run(circuit, 'y')
                    z_registers = run(circuit, 'z')

                    x = evaluate_register(x_registers)
                    y = evaluate_register(y_registers)
                    z = evaluate_register(z_registers)

                    got = x & y
                    expected = z
                    if got == expected:
                        swapped = [g1, g2, g3, g4]
                        res = ','.join(sorted(swapped))
                        return res

                    swap(g3, g4, circuit)
            swap(g1, g2, circuit)

    # swap('z05', 'z00', circuit)
    # swap('z02', 'z01', circuit)


    # x_registers = run(circuit, 'x')
    # y_registers = run(circuit, 'y')
    # z_registers = run(circuit, 'z')

    # dump_register(x_registers, 'x')
    # dump_register(y_registers, 'y')
    # dump_register(z_registers, 'z')

    # x = evaluate_register(x_registers)
    # y = evaluate_register(y_registers)
    # z = evaluate_register(z_registers)


    # got = x & y
    # expected = z

    # ic(got, expected)

    return 0



def part2(filename: str) -> int:
    circuit = read_data(filename)
    # ic(circuit)

    # jss <-> rds
    # mvb <-> z08
    # wss <-> z18
    # z23 <-> bmn

    swap('jss', 'rds', circuit)
    swap('mvb', 'z08', circuit)
    swap('wss', 'z18', circuit)
    swap('z23', 'bmn', circuit)


    swapped = ['jss', 'rds', 'mvb', 'z08', 'wss', 'z18', 'z23', 'bmn']


    x_registers = run(circuit, 'x')
    y_registers = run(circuit, 'y')
    z_registers = run(circuit, 'z')

    x = evaluate_register(x_registers)
    y = evaluate_register(y_registers)
    z = evaluate_register(z_registers)

    got = x + y
    expected = z
    if got == expected:
        res = ','.join(sorted(swapped))
        return res


# ic.disable()

assert ic(part1('./sample.txt')) == 4
assert ic(part1('./sample2.txt')) == 2024
assert ic(part1('./input.txt')) == 41324968993486

assert ic(part2_sample('./sample3.txt')) == 'z00,z01,z02,z05'
assert ic(part2('./input.txt')) == 'bmn,jss,mvb,rds,wss,z08,z18,z23'


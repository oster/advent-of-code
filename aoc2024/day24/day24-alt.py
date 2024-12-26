from collections import defaultdict
from functools import reduce
from icecream import ic

class Adder:
    def __init__(self, x: str, y: str, z: str, c_in: str, c_out, circuit: 'Circuit'):
        self.x = x
        self.y = y
        self.z = z
        self.c_in = c_in
        self.c_out = c_out
        self.circuit = circuit

    def __repr__(self):
        return f"ADD({self.x} + {self.y}, {self.c_in}) -> ({self.z} {self.c_out})"

    def evaluate(self) -> bool:
        raise NotImplementedError


class Gate:
    def __init__(self, kind: str, in1: str, in2: str, out: str, circuit: 'Circuit'):
        self.in1 = in1
        self.in2 = in2
        self.out = out
        self.kind = kind
        self.circuit = circuit

    def __repr__(self):
        return f"{self.in1} {self.kind} {self.in2} -> {self.out}"
    
    def evaluate(self) -> bool:
        in1_state = self.circuit.evaluate(self.in1)
        in2_state = self.circuit.evaluate(self.in2)

        if self.kind == "AND":
            return in1_state & in2_state
        elif self.kind == "OR":
            return in1_state | in2_state
        elif self.kind == "XOR":
            return in1_state ^ in2_state
        else:
            raise ValueError(f"Unknown operation: {self.kind}")

class Circuit:
    def __init__(self):
        self.gates = {}
        self.registers = {}


    def is_register(self, wire: str) -> bool:
        return wire in self.registers
    
    def is_gate(self, wire: str) -> bool:
        return wire in self.gates

    @staticmethod
    def read_data(filename: str) -> 'Circuit':
        circuit = Circuit()
        with open(filename, "r") as data_file:
            data = data_file.read()
            initial_state, rules = data.split("\n\n")

            for register_state in initial_state.split("\n"):
                register, state = register_state.strip().split(": ")
                circuit.registers[register] = bool(int(state))

            for gates_spec in rules.split("\n"):
                if not gates_spec:
                    continue
                inputs, output = gates_spec.split(" -> ")
                inputs = inputs.split(" ")
                circuit.gates[output] = Gate(inputs[1], inputs[0], inputs[2], output, circuit)
        return circuit


    def evaluate(self, register: str) -> bool:
        if self.is_register(register):
            return self.registers[register]
        return self.gates[register].evaluate()


    def evaluate_all(self, prefix: str) -> dict[str, bool]:
        registers_states = {}

        registers = [r for r in self.registers if r.startswith(prefix)]
        for r in registers:
            registers_states[r] = self.evaluate(r)

        gates = [g for g in self.gates if g.startswith(prefix)]
        for g in gates:
            registers_states[g] = self.gates[g].evaluate()

        return registers_states


    def dump_register(self, prefix: str) -> str:
        states = self.evaluate_all(prefix)
        bits = sorted(states.items(), key=lambda x: x[0], reverse=True)
        return ''.join([str(int(v)) for _, v in bits])


    def value(self, prefix: str) -> int:
        states = self.evaluate_all(prefix)
        bits = sorted(states.items(), key=lambda x: x[0], reverse=True)
        val = reduce(lambda acc, x: acc << 1 | x, [int(v) for k, v in bits], 0)
        return val
    

    def swap(self, a: str, b: str) -> None:
        gate_a = self.gates[a]
        gate_b = self.gates[b]
        gate_a.out = b
        gate_b.out = a
        self.gates[b] = gate_a
        self.gates[a] = gate_b


    def find_faulty_adders(self, prefix: str, start: int, end: int) -> set[int]:
        # check all adder individually to find faulty ones
        faulty = set()
        for idx in range(start, end): 
            self.registers[f'x{idx:02}'] = True
            self.registers[f'y{idx:02}'] = False
            if not self.evaluate(f'z{idx:02}') == True:
                faulty.add(idx)       

            self.registers[f'x{idx:02}'] = False
            self.registers[f'y{idx:02}'] = True
            if not self.evaluate(f'z{idx:02}') == True:
                faulty.add(idx )      

            self.registers[f'x{idx:02}'] = True
            self.registers[f'y{idx:02}'] = True
            if not self.evaluate(f'z{idx:02}') == False:
                faulty.add(idx)       

            self.registers[f'x{idx:02}'] = False
            self.registers[f'y{idx:02}'] = False
            if not self.evaluate(f'z{idx:02}') == False:
                faulty.add(idx)       

        return faulty


    def _find_gate(self, in1: str, in2: str, kind = None) -> set[Gate]:
        match = set()
        for g in self.gates:
            gate = self.gates[g]
            if (gate.in1 == in1 and gate.in2 == in2) or (gate.in1 == in2 and gate.in2 == in1):
                match.add(gate)

        if filter:
            match = set(filter(lambda x: x.kind == kind, match))
        
        return match


    def _find_gate_one_input(self, in1: str, kind = None) -> set[Gate]:
        match = set()
        for g in self.gates:
            gate = self.gates[g]

            if type(gate) == Gate:
                if (gate.in1 == in1) or (gate.in2 == in1):
                    # ic(gate)
                    match.add(gate)
            elif type(gate) == Adder:
                if (gate.x == in1) or (gate.y == in1) or (gate.c_in == in1):
                    # ic(gate)
                    match.add(gate)

        # if filter:
        #     match = set(filter(lambda x: x.kind == kind, match))
        
        return match



    def match_add(self, idx: int) -> tuple[str, str, str, str, str, str, str, str]:
        x_name = f'x{idx:02}'
        x = self.registers[x_name]

        y_name = f'y{idx:02}'
        y = self.registers[y_name]

        z_name = f'z{idx:02}'
        z = self.gates[z_name]

        cin_name = None
        cin = None

        xor_xy_name = None
        xor_xy = None

        and_xy_name = None
        and_xy = None

        and_xy_cin_name = None
        and_xy_cin = None

        cout_name = None
        cout = None

        assert z.kind == 'XOR'




        if idx == 0:

            cout_name = self._find_gate('x00', 'y00', 'AND').pop() 
            return ('x00', 'y00', 'z00', None, 'mgk', None, None, None)


        z_in1 = self.gates[z.in1]
        z_in2 = self.gates[z.in2]



        assert z_in1.kind in ['XOR', 'OR'] or (idx == 1 and z_in1.kind == 'AND')
        assert z_in2.kind in ['XOR', 'OR'] or (idx == 1 and z_in2.kind == 'AND')

        xor_xy, xor_xy_name = (z_in1, z.in1) if z_in1.kind == 'XOR' else (z_in2, z.in2)
        cin, cin_name = (z_in1, z.in1) if z_in1.kind == 'OR' else (z_in2, z.in2)


        m = self._find_gate(x_name, y_name, 'AND')
        assert len(m) == 1
        and_xy = m.pop()
        and_xy_name = and_xy.out


        m = self._find_gate(xor_xy_name, cin_name, 'AND')
        assert len(m) == 1
        and_xy_cin = m.pop()
        and_xy_cin_name = and_xy_cin.out


        m = self._find_gate(and_xy_name, and_xy_cin_name, 'OR')
        assert len(m) == 1
        cout = m.pop()
        cout_name = cout.out

        # ic(x_name, y_name, z_name, cin_name, cout_name, xor_xy_name, and_xy_name, and_xy_cin_name)
        return (x_name, y_name, z_name, cin_name, cout_name, xor_xy_name, and_xy_name, and_xy_cin_name)
        # add them to remove after the matching...


    def replace(self, idx: int, values: tuple[str, str, str, str, str, str, str, str]) -> None:
        
        (x_name, y_name, z_name, cin_name, cout_name, xor_xy_name, and_xy_name, and_xy_cin_name) = values

        add = Adder(x_name, y_name, z_name, cin_name, cout_name, self)
        add_name = f'add{idx:02}'

        if z_name:
            del self.gates[z_name]
        if xor_xy_name:
            del self.gates[xor_xy_name]
        if and_xy_name:
            del self.gates[and_xy_name]
        if and_xy_cin_name:
            del self.gates[and_xy_cin_name]
        if cout_name:
            del self.gates[cout_name]

        m = self._find_gate_one_input(cout_name)
        # ic(cout_name, m)
        assert len(m) == 2 or idx >= 44
        for g in m:
            if g.in1 == cout_name:
                g.in1 = add_name + ':cout'
            else:
                g.in2 = add_name + ':cout'

        self.gates[add_name] = add

    def as_dot(self) -> str:

        uid = 0

        res = 'graph G {\n'
        res += 'node [shape="point"]'

        res += 'subgraph {\n'

        res += 'rank=same\n'
        for r in self.registers:
            color = 'lightsteelblue' if r.startswith('x') else 'lightblue'
            res += f'  {r} [shape=circle, label="{r}", color="{color}", style="filled"]\n'

        res += '}\n\n'
        res += 'subgraph {\n'
        res += 'rank=same\n'

        for idx in range(0, 45 + 1):
            res += f'  z{idx:02} [shape=doublecircle, label="z{idx:02}", color="lightgreen", style="filled"]\n'
        res += '}\n\n'

        res += 'subgraph {\n'
        for g in sorted(self.gates, key=lambda x: x[1]):
            uid += 1
            gate = self.gates[g]
            if type(gate) == Gate:
                guid = gate.kind + str(uid)

                shape = "invhouse"
                match gate.kind:
                    case "AND":
                        color = "darkolivegreen3"
                    case "OR":
                        color = "goldenrod1"
                    case "XOR":
                        color = "coral"


                in1_label = gate.in1
                in2_label = gate.in2 

                res += f'  {guid} [shape={shape}, label="{gate.kind}" color="{color}" style="filled"]\n'
                res += f'  {gate.in1} -- {guid} [label="{in1_label}"]\n'
                res += f'  {gate.in2} -- {guid} [label="{in2_label}"]\n'
                # res += f'  {guid} [shape=triangle, label="{gate.kind}"]\n'
                # res += f'  {gate.in1} -- {guid}\n'
                # res += f'  {gate.in2} -- {guid}\n'
                res += f'  {guid} -- {gate.out} [label="{gate.out}"]\n'
            elif type(gate) == Adder:
                guid = 'add' + str(uid)
                res += f'  {guid}' + '[shape="record", label="ADD|{{<cin>Cin|<a>A|<b>B}|{<s>S|<cout>Cout}}" style="filled,rounded", fillcolor="cornsilk" ]\n'
                res += f'  {gate.x} -- {guid}:a [label={gate.x}]\n'
                res += f'  {gate.y} -- {guid}:b [label={gate.y}]\n'
                if gate.c_in:
                    res += f'  {gate.c_in} -- {guid}:cin [label={gate.c_in}]\n'
                res += f'  {guid}:s -- {gate.z} [label={gate.z}]\n'
                res += f'  {guid}:cout -- {gate.c_out} [label={gate.c_out}]\n'

        res += '}\n\n'
        res += '}\n'

        return res


def part1(filename: str) -> int:
    circuit = Circuit.read_data(filename)
    # print('z:', circuit.dump_register('z'))
    return circuit.value('z')


def part2_sample(filename: str) -> str:
    circuit = Circuit.read_data(filename)

    # swap by hand to check if it works
    #
    # circuit.swap('z05', 'z00')
    # circuit.swap('z02', 'z01')
    # x = circuit.value('x')
    # y = circuit.value('y')
    # z = circuit.value('z')
    # print('x: ', circuit.dump_register('x'))
    # print('y: ', circuit.dump_register('y'))
    # print('z: ', circuit.dump_register('z'))
    # got = z
    # expected = x & y
    # ic(got, expected)

    gates = circuit.gates
    for g1 in gates:
        for g2 in gates:
            if g1 == g2:
                continue
            circuit.swap(g1, g2)
            for g3 in gates:
                if g1 == g3 or g2 == g3:
                    continue
                for g4 in gates:
                    if g1 == g4 or g2 == g4 or g3 == g4:
                        continue
                    circuit.swap(g3, g4)

                    x = circuit.value('x')
                    y = circuit.value('y')
                    z = circuit.value('z')

                    expected = x & y
                    got = z
                    if got == expected:
                        swapped = [g1, g2, g3, g4]
                        res = ','.join(sorted(swapped))
                        return res

                    circuit.swap(g3, g4)
            circuit.swap(g1, g2)

    return ''





def find_bad_wiring(circuit: dict[str, tuple[str, str, str]|bool], idx: int) -> list[str]:
    res = []

    x_name = f'x{idx:02}'
    y_name = f'y{idx:02}'
    z_name = f'z{idx:02}'

    x = circuit[x_name]
    y = circuit[y_name]
    z = circuit[z_name]

    # ic(x, y, z)

    gates = { k: v for k, v in circuit.items() if type(v) != bool }

    two_gates = [(g_out, (g_kind, g_in1, g_in2)) for g_out, (g_kind, g_in1, g_in2)  in gates.items() if (g_in1 == x_name and g_in2 == y_name) or (g_in1 == y_name and g_in2 == x_name)]
    ic(two_gates)



    return res


def part2_reduce_dot(filename: str) -> str:
    circuit = Circuit.read_data(filename)
    # ic(circuit)

    with open('tmp1.dot', 'w') as f:
        f.write(circuit.as_dot())


    res = ''
    faulties = circuit.find_faulty_adders('z', 0, 45)
    for faulty in faulties:
        res += f'z{faulty:02}, '
    ic(res)

    faulties.add(24)

    matching_adds = [ (idx, circuit.match_add(idx)) for idx in range(0, 45) if idx not in faulties ]
    for idx, values in matching_adds:
        circuit.replace(idx, values)

    with open('tmp2.dot', 'w') as f:
        f.write(circuit.as_dot())



def part2(filename: str) -> str:
    circuit = Circuit.read_data(filename)


    # jss <-> rds
    # mvb <-> z08
    # wss <-> z18
    # z23 <-> bmn

    circuit.swap('jss', 'rds')
    circuit.swap('mvb', 'z08')
    circuit.swap('wss', 'z18')
    circuit.swap('z23', 'bmn')

    swapped = ['jss', 'rds', 'mvb', 'z08', 'wss', 'z18', 'z23', 'bmn']

    x = circuit.value('x')
    y = circuit.value('y')
    z = circuit.value('z')

    if x + y == z:
        res = ','.join(sorted(swapped))
        return res

    return ''

# ic.disable()

assert ic(part1('./sample.txt')) == 4
assert ic(part1('./sample2.txt')) == 2024
assert ic(part1('./input.txt')) == 41324968993486

assert ic(part2_sample('./sample3.txt')) == 'z00,z01,z02,z05'
assert ic(part2('./input.txt')) == 'bmn,jss,mvb,rds,wss,z08,z18,z23'


ic(part2_reduce_dot('./input.txt'))

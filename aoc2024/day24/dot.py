filename = 'input.txt'

with open(filename, "r") as data_file:
    data = data_file.read()
    initial_state, rules = data.split("\n\n")

    # for wire_state in initial_state.split("\n"):
    #     wire, state = wire_state.strip().split(": ")
    #     circuit[wire] = bool(int(state))


    print('graph {')


    for i in range(45):
        print(f'x{i:02d} [style=filled, color=blue]')

    for i in range(45):
        print(f'y{i:02d} [style=filled, color=orange]')

    for i in range(46):
        print(f'z{i:02d} [style=filled, color=green]')




    counter = 0
    for connection in rules.split("\n"):
        if not connection:
            continue

        counter += 1

        inputs, out = connection.split(" -> ")
        inputs = inputs.split(" ")
        type, in1, in2 = (inputs[1], inputs[0], inputs[2])

        # print(f"{type} {in1} {in2} -> {out}")
        idg = f'{in1}{counter}'
        print(f'{idg} [shape=triangle, label="{type.upper()}"]')
        print(f'{in1} -- {idg}')
        print(f'{in2} -- {idg}')
        print(f'{idg} -- {out}')


    print('}')
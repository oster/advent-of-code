
print('graph {')

with open("input.txt", "r") as input:

    for l in input:
        l = l.strip()
        src, dst = l.split(' -> ')
        dsts = dst.split(', ')

        if src.startswith('%') or src.startswith('&'):
            name = src[1:]
        else:
            name = src

        if src.startswith('%'):
            print(f'   {name} [shape=Msquare,color=blue];')
        if src.startswith('&'):
            print(f'   {name} [shape=Mdiamond,color=green];')

        for d in dsts:
            print(f'  {name} -- {d};')
    print('rx [shape=Msquare,color=red];')

print('}')


import copy
import re

crates_stacks = []
moves = []

data = []
# with open('sample.txt','r') as data_file:
with open('input.txt','r') as data_file:
    data = data_file.readlines()

    pivot = data.index('\n')

    crates_spec = data[pivot-1:pivot]
    crates_count = int(crates_spec[-1].strip().split(' ')[-1])
    moves_log = data[pivot:]


    crates_def = [ elt.rstrip().replace('    ',' ').replace(' ', '|').replace('[','').replace(']','') for elt in data[:pivot-1] ]   
    crates_stacks = [ [] for _ in range(crates_count) ]

    for crate_def in crates_def[::-1]:
        for idx, cr in enumerate(crate_def.split('|')):
            if cr != '':
                crates_stacks[idx].append(cr)

    pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for move_str in moves_log:
        g = re.search(pattern, move_str)
        if g:
            moves.append(list(map(int, list(g.groups()))))
    
# print(crates_stacks)
# print(instructions)

# Part 1
crates_stacks_dup = copy.deepcopy(crates_stacks)
for move in moves:
    repetition, src, dst = move
    for i in range(repetition):
        crates_stacks[dst-1].append(crates_stacks[src-1].pop())

res_part1 = ''.join([ stack[-1] for stack in crates_stacks ])

# Part 2
for move in moves:
    repetition, src, dst = move
    tmp = []
    for i in range(repetition):
        tmp.append(crates_stacks_dup[src-1].pop())
    for i in range(repetition):
        crates_stacks_dup[dst-1].append(tmp.pop())

res_part2 = ''.join([ stack[-1] for stack in crates_stacks_dup ])


print(f'Part 1: {res_part1}') # VRWBSFZWM
print(f'Part 2: {res_part2}') # RBTWJWMCF

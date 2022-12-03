def get_priority(item):
    item = ord(item[0])
    if item >= ord('a') and item <= ord('z'):
        priority =  item - ord('a') + 1
        return priority
    elif item >= ord('A') and item <= ord('Z'):
        return  item - ord('A') + 1 + 26

    raise Exception('invalid item (not in [a-zA-Z]')
    return -1

bags = []
# with open('sample.txt','r') as data_file:
with open('input.txt','r') as data_file:
    bags = [ line.strip() for line in data_file.readlines() ]

total_priorities = 0

# Part 1
for bag in bags:
    pivot = len(bag)//2
    first_compartment, second_compartment = bag[:pivot], bag[pivot:]
    duplicated_item = [ item for item in first_compartment if item in second_compartment ]
    total_priorities += get_priority(duplicated_item)

# Part 2
total_badge_priorities = 0

for i in range(0, len(bags), 3):
    bp1 = bags[i]
    bp2 = bags[i+1]
    bp3 = bags[i+2]
    badge = [item2 for item2 in [ item for item in bp1 if item in bp2 ] if item2 in bp3][0]
    total_badge_priorities += get_priority(badge)


print(f'Part 1: {total_priorities}') # 7903

print(f'Part 2: {total_badge_priorities}') # 2548



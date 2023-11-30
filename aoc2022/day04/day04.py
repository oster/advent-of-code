def is_fully_contained(r1, r2):
    return (r1[0] <= r2[0] and r1[1] >= r2[1]) or (r2[0]<= r1[0] and r2[1]>= r1[1])

def are_overlapping(r1, r2):
    return (r1[1] >= r2[0] and r1[0] <= r2[1] ) or (r2[1] >= r1[0] and r2[0] <= r1[1])

data = []
# with open('sample.txt','r') as data_file:
with open('input.txt','r') as data_file:
    for line in data_file.readlines():
        data.append(list([int(x) for x in couple.split('-')] for couple in line.strip().split(',')))

fully_contained_count = 0
partial_overlap_count = 0

for pairs in data:
    if is_fully_contained(pairs[0], pairs[1]):
        fully_contained_count += 1

    if are_overlapping(pairs[0], pairs[1]):
        partial_overlap_count += 1

    # print(pairs, is_fully_contained(pairs[0], pairs[1]), are_overlapping(pairs[0], pairs[1]))

print(f'Part 1: {fully_contained_count}') # 573

print(f'Part 2: {partial_overlap_count}') # 867

# Problem 1: How many total Calories is that Elf carrying?

data = []
# with open('sample.txt','r') as data_file:
with open('input.txt','r') as data_file:
    elf = []
    for line in data_file.readlines():
        line = line.strip()
        if line:
            elf.append(int(line))
        else:
            data.append(sum(elf))
            elf = []
    data.append(sum(elf))

max_calories = max(data)
elf_index = data.index(max_calories)
print(f'Part 1: {max_calories}') # 69281

# Problem 2: How many Calories are those Elves carrying in total?

sorted_data = sorted(data, reverse=True)
print(f'Part 2: {sorted_data[0] + sorted_data[1] + sorted_data[2]}') # 201524


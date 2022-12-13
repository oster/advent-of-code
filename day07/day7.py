def read_input(filename):
    with open(filename, 'r') as datafile:
        return [line.rstrip('\n') for line in datafile.readlines()]

def populate(instructions):
    directories = {}

    stack = []
    size = 0
    path = ['/']

    for instruction in instructions:
        if instruction == '$ cd /':
            path = ['/']
            stack.clear()
        elif instruction == '$ cd ..':
            directories['/'.join(path)] = size
            subdirectory_size = size
            size = stack.pop()
            size += subdirectory_size
            path.pop()
        elif instruction.startswith('$ cd '):
            _, _, destination_dir = instruction.split(' ')
            path.append(destination_dir)
            stack.append(size)
            size = 0
        elif instruction == '$ ls':
            pass
        elif instruction.startswith('dir'):
            # _, dirname = instruction.split(' ') 
            pass
        else:
            filesize, filename = instruction.split(' ')
            filesize = int(filesize)
            size += filesize

    while len(stack) > 0:
        # we go up until / 
        directories['/'.join(path)] = size
        subdirectory_size = size
        
        size = stack.pop()
        size += subdirectory_size
        path.pop()
        current_dir = path[-1]
        directories[current_dir] = size

    return directories
        

def compute_part1(directories):
    sum = 0
    for _, size in directories.items():
        if size < 100000:
            sum += size
    return sum

def compute_part2(directories):
    disk_space = 70000000
    required_space_for_update = 30000000
    unused_space = disk_space - directories['/']
    space_to_free = required_space_for_update - unused_space

    for directory_size in sorted(directories.values()):
        if directory_size >= space_to_free:
            return directory_size
    
    return -1


input = read_input('input.txt')
directories = populate(input)

part1 = compute_part1(directories)
print('Part 1:', part1)

part2 = compute_part2(directories)
print('Part 2:', part2)

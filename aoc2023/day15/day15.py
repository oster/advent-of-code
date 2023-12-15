def read_input(filename: str) -> list[str]:
    data = []
    with open(filename, "r") as input_file:
        data = input_file.readline().rstrip().split(',')

    return data

def die(msg: str):
    raise Exception(msg)


def hash(str) -> int:
    current = 0
    for c in str:
        current += ord(c)
        current *= 17
        current %= 256
    return current


def part1(filename: str) -> int:
    data = read_input(filename)
    return sum(( hash(ins) for ins in data ))


def part2(filename: str) -> int:
    data = read_input(filename)
    boxes = [ list() for _ in range(256) ]

    for instruction in data:
        if instruction[-1] == '-' in instruction:
            op = '-'
            label = instruction[:-1]

            k = hash(label)
            for idx, lens in enumerate(boxes[k]):
                if lens[0] == label:
                    boxes[k].pop(idx)
                    break
        else:
            op = '='
            label, focal_length = instruction.split('=')
            focal_length = int(focal_length)

            k = hash(label)
            if not boxes[k]:
                # if empty
                boxes[k].append((label, focal_length))
            else:
                done = False
                for idx, lens in enumerate(boxes[k]):
                    if lens[0] == label:
                        boxes[k][idx] = (label, focal_length)
                        done = True
                        break
                if not done:
                    boxes[k].append((label, focal_length))

    # print boxes
    #
    # for i in range(0,4):
    #     print(f'Box {i:3}: ', list(boxes[i]))

    focusing_power = 0
    for idx_box, box in enumerate(boxes):
        for idx_lens, lens in enumerate(box):
            focusing_power += (idx_box + 1) * (idx_lens + 1)  * lens[1]

    return focusing_power


assert hash('HASH') == 52

assert part1("./sample.txt") == 1320
assert part1("./input.txt") == 513172

assert part2("./sample.txt") == 145
assert part2("./input.txt") == 237806


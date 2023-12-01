def read_input(filename : str) -> list[str]:
    with open(filename, 'r') as input_file:
        return [line.rstrip() for line in input_file.readlines() ]

def extract_value(line : str) -> int:
    calibration = 0
    for c in line:
        if c.isdigit():
            calibration = int(c)
            break

    calibration = calibration * 10

    for c in reversed(line):
        if c.isdigit():
            calibration += int(c)
            break

    return calibration

# def extract_value_alt(line):
#     first = 0
#     second = 0
# 
#     for c in line:
#         if c.isdigit():
#             if first == 0: 
#                 first = c 
#             second = c
# 
#     return int(first) * 10 + int(second)

words = [ 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine' ]

def preprocess_part2(line : str) -> str:
    for idx, word in enumerate(words):
        line = line.replace(word, word+str(idx+1)+word)
    return line

# def preprocess_alt(line : str) -> str:
#     min_index = sys.maxsize
#     min_word = None
#     for word in words:
#         idx = line.find(word)
#         if idx != -1 and idx < min_index:
#             min_index = idx
#             min_word = word
#     if min_word:
#         line = line[:min_index] + min_word + values[words.index(min_word)] + min_word + line[min_index+len(min_word):]
#
#     max_index = -1
#     max_word = None
#     for word in words:
#         idx = line.rfind(word)
#         if idx != -1 and idx > max_index:
#             max_index = idx
#             max_word = word
#     if max_word:
#         line = line[:max_index] + max_word + values[words.index(max_word)] + max_word + line[max_index+len(max_word):]
#
#     return line


def part1(filename : str) -> int:
    return sum([ extract_value(line) for line in read_input(filename) ])


def part2(filename : str) -> int:
    return sum([ extract_value(preprocess_part2(line)) for line in read_input(filename) ])

assert part1('./sample.txt') == 142
assert part1('./input.txt') == 55712

assert part2('./sample2.txt') == 281
assert part2('./input.txt') == 55413


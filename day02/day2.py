
# A: Rock, B: Paper, C: Scissors
# X: Rock, Y: Paper, Z: Scissors
# ->
# score
yours_vs_mine = {
    "A, X": 3 + 1,
    "B, X": 0 + 1,
    "C, X": 6 + 1,
    "B, Y": 3 + 2,
    "A, Y": 6 + 2,
    "C, Y": 0 + 2,
    "A, Z": 0 + 3,
    "B, Z": 6 + 3,
    "C, Z": 3 + 3
}

# A: Rock, B: Paper, C: Scissors
# X: lose, Y: draw, Z:win
# ->
# X: Rock, Y: Paper, Z: Scissors, score
yours_expected = {
    "A, X": ('Z', 3 + 0),
    "A, Y": ('X', 1 + 3),
    "A, Z": ('Y', 2 + 6),
    "B, X": ('X', 1 + 0),
    "B, Y": ('Y', 2 + 3),
    "B, Z": ('Z', 3 + 6),
    "C, X": ('Y', 2 + 0),
    "C, Y": ('Z', 3 + 3),
    "C, Z": ('X', 1 + 6)
}


data = []
# with open('sample.txt','r') as data_file:
with open('input.txt','r') as data_file:

    total_score = 0
    total_score_part2 = 0

    for line in data_file.readlines():
        line = line.strip()
        yours, mine = line.split(' ')

        key = f'{yours}, {mine}'
        round_outcome = yours_vs_mine.get(key, 0)
        # print(f'{key} = {round_outcome}')

        total_score += round_outcome

        # Part 2 
        r = yours_expected.get(key)
        # print(f'{key} = {r}')
        total_score_part2 += r[1]


print(f'Part 1: {total_score}') # 14163

print(f'Part 2: {total_score_part2}') # 12091



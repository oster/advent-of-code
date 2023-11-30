sample1 = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb' # 7 / 19
sample2 = 'bvwbjplbgvbhsrlpgdmjqwftvncz' # 5 / 23
sample3 = 'nppdvjthqldpwncqszvftbrmjlhg' # 6 / 23
sample4 = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg' # 10 / 29
sample5 = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw' # 11 / 26


with open('input.txt','r') as data_file:
    data = data_file.readlines()
data = data[0].strip()

def start_of_packet_index(b, l):
    l = l - 1
    for i in range(l, len(b)):
        flag = True
        for j in range(0, l):
            flag = flag and (not b[i-j] in b[i-l:i-j])

        if flag:
            return i + 1

# start_of_packet_index(data)

print(f'Part 1: {start_of_packet_index(data, 4)}') # 1566
print(f'Part 2: {start_of_packet_index(data, 14)}') # 2265

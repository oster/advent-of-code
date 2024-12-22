from typing import Generator
from dataclasses import dataclass
from icecream import ic

def read_data(filename: str) -> list[int]:
    with open(filename, "r") as data_file:
        values = list(map(int, [line.strip() for line in data_file.readlines()]))
    return values


# secret = 123
# r = []
# for i in range(10):
#     secret = (secret << 6) ^ secret
#     secret = secret & (2**24 - 1)
#     secret = secret ^ (secret >> 5)
#     secret = secret & (2**24 - 1)
#     secret = secret ^ (secret << 11)
#     secret = secret & (2**24 - 1)
#     r.append(secret)

# assert r == [ 15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254, ]


def next_secret(secret: int, n: int) -> int:
    for _ in range(n):
        secret = (secret << 6) ^ secret
        secret = secret & (2**24 - 1)
        secret = secret ^ (secret >> 5)
        secret = secret & (2**24 - 1)
        secret = secret ^ (secret << 11)
        secret = secret & (2**24 - 1)
    return secret        


# values = read_data('sample.txt')
# secrets = { v: next_secret(v, 2000) for v in values } 

# secrets == {
#     1: 8685429,
#     10: 4700978,
#     100: 15273692,
#     2024: 8667524,
# }

# assert sum(secrets.values()) == 37327623


def part1(filename: str) -> int:
    values = read_data(filename)

    secrets = { v: next_secret(v, 2000) for v in values } 
    return sum(secrets.values())


secret = 123

next_ten_secrets = [ next_secret(123, i) for i in range(10) ]
assert next_ten_secrets == [ 123, 15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, ]


def last_digits(secrets: list[int]) -> list[int]:
    return [ s % 10 for s in secrets ]

# ic(last_digits(next_ten_secrets))
assert last_digits(next_ten_secrets) == [ 3, 0, 6, 5, 4, 4, 6, 4, 4, 2 ]



from itertools import tee

def window2(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def changes(secrets: list[int]) -> list[int]:
    return [None] + [ b - a for a, b in window2(secrets) ]

assert changes(last_digits(next_ten_secrets)) == [None, -3, 6, -1, -1, 0, 2, -2, 0, -2 ]




def window4(iterable):
    a, b, c, d = tee(iterable, 4)
    next(b, None)
    next(c, None)
    next(c, None)
    next(d, None)
    next(d, None)
    next(d, None)
    return zip(a, b, c, d)


# l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# for a, b, c, d in window4(l):
#     print(a, b, c, d)




def part2(filename: str) -> int:
    buyers = read_data(filename)

    secrets_by_buyer = {}
    last_digit_by_buyers = {}
    changes_by_buyers = {}

    for buyer in buyers:
        s = buyer
        secrets = []
        for _ in range(2000):
            secrets.append(s)
            s = next_secret(s, 1)
        secrets_by_buyer[buyer] = secrets    
        last_digit_by_buyers[buyer] = last_digits(secrets)
        changes_by_buyers[buyer] = changes(last_digit_by_buyers[buyer])

    # ic(len(secrets_by_buyer[1]))
    # ic(len(last_digit_by_buyers[1]))
    # ic(len(changes_by_buyers[1]))

    # buyer = 1
    # for i in range(0,2000):
    #     print(f'{secrets_by_buyer[buyer][i]}:\t {last_digit_by_buyers[buyer][i]}\t ({changes_by_buyers[buyer][i]})')

    # buyer = 1 
    # buyer = 2
    # buyer = 3
    # buyer = 2024
    # for idx, seq in enumerate(window4(changes_by_buyers[buyer])):
    #     if seq == (-2, 1, -1, 3):
    #         print(idx)
    #         print(last_digit_by_buyers[buyer][idx+3])



    best_prices = {}
    # buyers = [1, 2, 3, 2024]
    for buyer in buyers:
        for idx, seq in enumerate(window4(changes_by_buyers[buyer])):
            seq = tuple(seq)

            if seq not in best_prices:
                best_prices[seq] = {}
            if buyer not in best_prices[seq]:
                best_prices[seq][buyer] = (0, 0)

            price = last_digit_by_buyers[buyer][idx+3]
            if seq in best_prices:
                _, best_price = best_prices[seq][buyer]
                if best_price == 0:
                    best_prices[seq][buyer] = (idx, price)
                # best_idx, best_price = best_prices[seq][buyer]
                # if price > best_price:
                #     best_prices[seq][buyer] = (idx, price)
            else:
                best_prices[seq][buyer] = (idx, price)

    # ic(best_prices)


    best_gain = 0
    best_seq = None
    for seq, prices_by_buyers in best_prices.items():
        gain = sum([ price for _, price in prices_by_buyers.values() ])
        if gain > best_gain:
            best_gain = gain
            best_seq = seq
    # ic(best_seq)
    # ic(best_gain)

    return best_gain
    


# secrets = { v: next_secret(v, 2000) for v in values } 

# secrets == {
#     1: 8685429,
#     10: 4700978,
#     100: 15273692,
#     2024: 8667524,
# }



assert ic(part1('./sample.txt')) == 37327623
assert ic(part1('./input.txt')) == 17577894908

assert ic(part2('./sample2.txt')) == 23
assert ic(part2('./input.txt')) == 1931



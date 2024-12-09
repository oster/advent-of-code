from icecream import ic
from itertools import zip_longest, starmap


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def read_data(filename: str) -> list[tuple[int, int]]:
    with open(filename, "r") as data_file:
        return [ (int(block), int(free)) for block, free in grouper(data_file.readline().strip(), 2, 0) ]


def compact_part1(disk: list[str]) -> list[str]:
    free_idx = 0
    to_compact_idx = len(disk) - 1

    while free_idx < to_compact_idx:
        while disk[free_idx] != '.':
            free_idx += 1
        while disk[to_compact_idx] == '.':
            to_compact_idx -= 1

        if free_idx > to_compact_idx:
            break

        disk[free_idx], disk[to_compact_idx] = disk[to_compact_idx], disk[free_idx]

    return disk


def checksum_part1(disk: list[str]) -> int:
    sum = 0
    for idx, file_id in enumerate(disk):
        if file_id != '.':
            sum += idx * int(file_id)
    return sum


def generate_disk_part1(spec: list[tuple[int, int]], disk_size: int) -> list[str]:
    disk = [ '.' for _ in range(0, disk_size) ]
    idx = 0
    for file_id, (block, free) in enumerate(spec):
        for _ in range(0, block):
            disk[idx] = str(file_id)
            idx += 1
        for _ in range(0, free):
            disk[idx] = '.'
            idx += 1
    return disk


# def dump_disk(disk: list[str]) -> None:
#     print(''.join(disk))


def part1(filename: str) -> int:
    spec = read_data(filename)

    disk_size = sum(starmap(int.__add__, spec))
    disk = generate_disk_part1(spec, disk_size)
    # dump_disk(disk)

    compacted = compact_part1(disk)    
    return checksum_part1(compacted)


type Block = tuple[int, int]

# from typing import NewType
# Block = NewType('Block', tuple[int, int])

# def generate_disk_part2(file_blocks : dict[int, Block], free_blocks: list[Block], disk_size: int) -> list[str]:
#     disk = [ '_' for _ in range(0, disk_size) ]
#     for file_id, (start, block_size) in file_blocks.items():
#         for idx in range(start, start + block_size):
#             disk[idx] = str(file_id)
#     for start, free_size in free_blocks:
#         for idx in range(start, start + free_size):
#             disk[idx] = '.'
#     return disk


# def dump_disk(file_blocks: dict[int, Block], free_blocks: list[Block], disk_size: int) -> None:
#     disk = generate_disk_part2(file_blocks, free_blocks, disk_size)
#     print(''.join(disk))


def checksum_part2(block: dict[int, Block]) -> int:
    return sum(idx * file_id for file_id, (start, block_size) in block.items() for idx in range(start, start + block_size))


def process_fileblocks_freeblocks_part2(disk_spec : list[tuple[int, int]]) -> tuple[dict[int, Block], list[Block], int]:
    file_blocks = {}
    free_spaces = []
    disk_index = 0

    for file_id, (block_size, free_size) in enumerate(disk_spec):
        file_blocks[file_id] = (disk_index, block_size)
        disk_index += block_size

        if free_size > 0:
            free_spaces.append((disk_index, free_size))
            disk_index += free_size

    return file_blocks, free_spaces, disk_index                                                                                                                        


def compact_part2(file_blocks: dict[int, Block], free_blocks: list[Block]) -> tuple[dict[int, Block], list[Block]]:
    for file_id in sorted(file_blocks.keys(), reverse=True):
        block_start, block_size = file_blocks[file_id]

        for freeblock_idx, (freeblock_start, freeblock_size) in enumerate(free_blocks):
            if freeblock_size >= block_size and freeblock_start < block_start:
                file_blocks[file_id] = (freeblock_start, block_size)

                new_size = freeblock_size - block_size
                if new_size > 0:
                    free_blocks[freeblock_idx] = (freeblock_start + block_size, new_size)
                else:
                    del free_blocks[freeblock_idx]

                break

    return file_blocks, free_blocks


def part2(filename: str) -> int:
    spec = read_data(filename)
    file_blocks, free_blocks, disk_space = process_fileblocks_freeblocks_part2(spec)
    file_blocks, free_blocks = compact_part2(file_blocks, free_blocks)

    return checksum_part2(file_blocks)


# ic.disable()

assert ic(part1('./sample.txt')) == 1928
assert ic(part1('./input.txt')) == 6435922584968

assert ic(part2('./sample.txt')) == 2858
assert ic(part2('./input.txt')) == 6469636832766

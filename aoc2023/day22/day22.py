import sys


def die(msg: str):
    raise Exception(msg)


type Cube = tuple[int, int, int]
type Brick = tuple[Cube, Cube]


def read_input(filename: str) -> list[Brick]:
    bricks = []
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            points = line.rstrip().split("~")
            p1 = tuple(map(int, points[0].split(",")))
            p2 = tuple(map(int, points[1].split(",")))
            bricks.append((p1, p2))

    return bricks


X = 0
Y = 1
Z = 2


def can_go_down(brick: Brick, other_bricks: list[Brick]) -> bool:
    posA, posB = brick

    if posA[Z] == 1:
        return False

    for belowA, belowB in other_bricks:
        if posA[Z] - belowB[Z] - 1 <= 0:
            if (min(belowB[X], posB[X]) - max(posA[X], belowA[X])) >= 0 and min(
                posB[Y], belowB[Y]
            ) - max(posA[Y], belowA[Y]) >= 0:
                return False

    return True


def how_far_go_down(brick: Brick, other_bricks: list[Brick]) -> int:
    posA, posB = brick

    if posA[Z] == 1:
        return 0

    h = posA[Z] - 1

    if len(other_bricks) == 0:
        return h

    for belowA, belowB in other_bricks:
        if (min(belowB[X], posB[X]) - max(posA[X], belowA[X])) >= 0 and min(
            posB[Y], belowB[Y]
        ) - max(posA[Y], belowA[Y]) >= 0:
            h = min(h, posA[Z] - belowB[Z] - 1)

    return h


def move_down(brick: Brick, h=1) -> Brick:
    posA, posB = brick
    return ((posA[X], posA[Y], posA[Z] - h), (posB[X], posB[Y], posB[Z] - h))


def part1(filename: str) -> int:
    bricks = read_input(filename)
    bricks = sorted(bricks, key=lambda brick: brick[1][Z])

    # packing bricks
    for idx, brick in enumerate(bricks):
        remaining = bricks[:idx]
        brick = move_down(brick, how_far_go_down(brick, remaining))
        bricks[idx] = brick

    # print(bricks)

    count = 0
    for idx, disintegrated_brick in enumerate(bricks):
        must_keep = False
        remaining_bricks = (
            b
            for b in bricks
            if b != disintegrated_brick and b[0][Z] >= disintegrated_brick[0][Z]
        )

        for brick in remaining_bricks:
            to_be_considered = (
                b
                for b in bricks
                if b != disintegrated_brick and b != brick and b[0][Z] < brick[0][Z] 
            )
            if can_go_down(brick, to_be_considered):
                must_keep = True
                break

        if not must_keep:
            count += 1
    return count


# from time import time
# start = time()
# print(part1("./input.txt"))
# print(f"Time: {time()-start}")


# assert part1("./sample.txt") == 5
# assert part1("./input.txt") == 482


def part2(filename: str) -> int:
    bricks = read_input(filename)
    bricks = sorted(bricks, key=lambda brick: brick[1][Z])

    # packing bricks
    for idx, brick in enumerate(bricks):
        remaining = bricks[:idx]
        brick = move_down(brick, how_far_go_down(brick, remaining))
        bricks[idx] = brick

    count = 0
    for idx, disintegrated_brick in enumerate(bricks):
        copy_bricks = bricks.copy()

        remaining_bricks = (
            b
            for b in copy_bricks
            if b != disintegrated_brick and b[0][Z] >= disintegrated_brick[0][Z]
        )

        for brick in remaining_bricks:
            to_be_considered = [
                b
                for b in copy_bricks
                if b != brick and b[0][Z] < brick[0][Z] and b != disintegrated_brick
            ]

            idxxx = copy_bricks.index(brick)
            if can_go_down(brick, to_be_considered):
                count += 1
                brick = move_down(brick, how_far_go_down(brick, to_be_considered))
                # while can_go_down(brick, to_be_considered):
                #     brick = move_down(brick)
                copy_bricks[idxxx] = brick

    return count


from time import time
start = time()
print(part1("./input.txt"))
print(f"Time: {time()-start}")


start = time()
print(part2("./input.txt"))
print(f"Time: {time()-start}")

# assert part2("./sample.txt") == 7
# assert part2("./sample.txt") == 103010

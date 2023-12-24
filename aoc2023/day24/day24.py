from typing import Any, Optional
import sys


type Pos2D = tuple[float, float]
type Velocity2D = tuple[float, float]
type Eq = tuple[float, float]

def read_input(filename: str) -> list[tuple[Pos2D, Velocity2D]]:
    data = []
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            line = line.rstrip().split(" @ ")
            pos = tuple(map(float, line[0].split(", ")))
            pos2D = (pos[0], pos[1])
            vel = tuple(map(float, line[1].split(", ")))
            vel2D = (vel[0], vel[1])
            data.append((pos2D, vel2D))
    return data

def get_line_equation(p1: Pos2D, v1: Velocity2D) -> Eq:
    p1_x, p1_y = p1
    v1_x, v1_y = v1

    p2_x = p1_x + v1_x
    p2_y = p1_y + v1_y

    if p2_x == p1_x:
        assert False, "no vertical line expected"
        return sys.float_info.max, p1_x

    a = (p2_y - p1_y) / (p2_x - p1_x)
    # y - p1_y = a * (x - p1_x)
    # y = a * (x - p1_x) + p1_y
    # y = a * x - a * p1_x + p1_y
    b = -a * p1_x + p1_y

    return a, b


def die(msg: str):
    raise Exception(msg)


def get_two_big_points(eq: Eq, min: int, max: int) -> tuple[Pos2D, Pos2D]:
    a, b = eq
    if a == sys.float_info.max:
        assert False, "no vertical line expected"
        # return (min, min), (max, max)

    ymin = a * min + b
    ymax = a * max + b
    return (min, ymin), (max, ymax)


def get_intersection_point(
    pA: Pos2D, pB: Pos2D, pC: Pos2D, pD: Pos2D
) -> Optional[Pos2D]:
    pA_x, pA_y = pA
    pB_x, pB_y = pB
    pC_x, pC_y = pC
    pD_x, pD_y = pD

    # Line AB represented as a1x + b1y = c1
    a1 = pB_y - pA_y
    b1 = pA_x - pB_x
    c1 = a1 * (pA_x) + b1 * (pA_y)

    # Line CD represented as a2x + b2y = c2
    a2 = pD_y - pC_y
    b2 = pC_x - pD_x
    c2 = a2 * (pC_x) + b2 * (pC_y)

    det = a1 * b2 - a2 * b1

    if det == 0:
        # The lines are parallel.
        return None
    else:
        x = (b2 * c1 - b1 * c2) / det
        y = (a1 * c2 - a2 * c1) / det
        return (x, y)


def is_past_point(some: Pos2D, ref: tuple[Pos2D, Velocity2D], line_eq: Eq) -> bool:
    # a, b = line_eq
    some_x, some_y = some
    (ref_x, ref_y), (vel_x, vel_y) = ref

    # if a == sys.float_info.max:
    #     assert False, 'no vertical line expected'

    # print(f'Line equation: y = {a:.3f} * x + {b:.3f}')

    if vel_x > 0:
        if vel_y > 0:
            increasing = True
            going_right = True
        else:
            increasing = False
            going_right = True
    else:
        if vel_y > 0:
            increasing = False
            going_right = False
        else:
            increasing = True
            going_right = False

    # print(f'Increasing: {increasing}, going right: {going_right}')

    if increasing:
        if going_right:
            return some_x < ref_x
        else:
            return some_x > ref_x
    else:
        if going_right:
            return some_x < ref_x
        else:
            return some_x > ref_x


def inside(some: Pos2D, min: int, max: int) -> bool:
    some_x, some_y = some
    return some_x >= min and some_x <= max and some_y >= min and some_y <= max


def part1(filename: str, min_value: int, max_value: int) -> int:
    data = read_input(filename)
    # print(data)

    lines = [get_line_equation(p, v) for p, v in data]
    # print(lines)

    two_points = [get_two_big_points(eq, min_value, max_value) for eq in lines]

    intersect_count = 0

    for idx1, (pA, pB) in enumerate(two_points):
        for idx2, (pC, pD) in enumerate(two_points[idx1 + 1 :]):
            id2 = idx1 + idx2 + 1

            print(f"Hailstone A: {data[idx1]}")
            print(f"Hailstone B: {data[id2]}")
            if idx1 == id2:
                continue
            intersection = get_intersection_point(pA, pB, pC, pD)
            if intersection is None:
                print(
                    f"Hailstones' paths are parallel; they never intersect."
                )
            else:
                is_past_A = is_past_point(intersection, data[idx1], lines[idx1])
                is_past_B = is_past_point(intersection, data[id2], lines[id2])

                if is_past_A:
                    if is_past_B:
                        print(
                            "Hailstones' paths crossed in the past for both hailstones."
                        )
                    else:
                        print(f"Hailstones' paths crossed in the past for hailstone A.")
                elif is_past_B:
                    print(f"Hailstones' paths crossed in the past for hailstone B.")
                else:
                    if inside(intersection, min_value, max_value):
                        print(
                            f"Hailstones' paths will cross inside the test area (at x={intersection[0]:.3f}, y={intersection[1]:.3f})."
                        )
                        intersect_count += 1
                    else:
                        print(
                            f"Hailstones' paths will cross outside the test area (at x={intersection[0]:.3f}, y={intersection[1]:.3f})."
                        )

            print()

    print(f"Total number of intersections: {intersect_count}")
    return intersect_count


assert part1("./sample.txt", 7, 27) == 2
assert (
    part1("./input.txt", 200000000000000, 400000000000000) == 31208
)

print(part1("./sample.txt", 7, 27))


type Pos3D = tuple[float, float, float]
type Velocity3D = tuple[float, float, float]

def read_input_part2(filename: str) -> list[tuple[Pos3D, Velocity3D]]:
    data = []
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            line = line.rstrip().split(" @ ")
            pos = tuple(map(float, line[0].split(", ")))
            vel = tuple(map(float, line[1].split(", ")))
            data.append((pos, vel))
    return data


# def colineaires(v1: Velocity3D, v2: Velocity3D) -> bool:
#     v1_x, v1_y, v1_z = v1
#     v2_x, v2_y, v2_z = v2

#     i = v1_x / v2_x
#     j = v1_y / v2_y 
#     k = v1_z / v2_z 

#     return i == j == k 

from z3 import Real, Solver

def part2(filename: str) -> int:
    lines3D = read_input_part2(filename)

    s = Solver()

    target_x = Real('target_x')
    target_y = Real('target_y')
    target_z = Real('target_z')
    target_vx = Real('target_vx')
    target_vy = Real('target_vy')
    target_vz = Real('target_vz')

    for idx, ((point_x, point_y, point_z), (point_vx, point_vy, point_vz)) in enumerate(lines3D):
        t = Real(f't{idx}')
        s.add(target_x + target_vx * t == point_x + point_vx * t)
        s.add(target_y + target_vy * t == point_y + point_vy * t)
        s.add(target_z + target_vz * t == point_z + point_vz * t)

    s.check()
    m = s.model()

    res = m[target_x].as_long() + m[target_y].as_long() + m[target_z].as_long()
    return res


assert part2("./sample.txt") == 47
assert part2("./input.txt") == 580043851566574

from icecream import ic
from enum import IntEnum

def read_data(filename: str) -> tuple[int, int, int, list[int]]:
    with open(filename, "r") as data_file:
        ra = int(data_file.readline().split(':')[1].strip())
        rb = int(data_file.readline().split(':')[1].strip())
        rc = int(data_file.readline().split(':')[1].strip())

        _ = data_file.readline()
        pr = list(map(int, data_file.readline().split(':')[1].strip().split(',')))
        return ra, rb, rc, pr

class OpCode(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

    def __str__(self):
        return ['ADV', 'BXL', 'BST', 'JNZ', 'BXC', 'OUT', 'BDV', 'CDV'][self.value]

class Computer:
    ra:int = 0
    rb:int = 0
    rc:int = 0
    mem: list[int] = []

    ip: int = 0
    jp: bool = False

    def __init__(self, ra:int, rb:int, rc:int, mem: list[int]):
        self.ra = ra
        self.rb = rb
        self.rc = rc
        self.mem = mem
        self.stdout: list[int] = []

    def get_stdout(self) -> str:
        return ','.join(map(str, self.stdout))

    def reset(self, ra:int=0, rb:int=0, rc:int=0):
        self.ra = ra
        self.rb = rb
        self.rc = rc
        # self.mem = []
        self.ip = 0
        self.jp = False
        self.stdout = []


    def run(self):
        while 0 <= self.ip < len(self.mem):
            self.jp = False
            operand = self.mem[self.ip + 1]
            match self.mem[self.ip]:
                case OpCode.ADV:
                    self.adv(operand)
                case OpCode.BXL:
                    self.bxl(operand)
                case OpCode.BST:
                    self.bst(operand)
                case OpCode.JNZ:
                    self.jnz(operand)
                case OpCode.BXC:
                    self.bxc(operand)
                case OpCode.OUT:
                    self.out(operand)
                case OpCode.BDV:
                    self.bdv(operand)
                case OpCode.CDV:
                    self.cdv(operand)
            if not self.jp:
                self.ip += 2


    def combo(self, operand: int) -> int:
        match operand:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return self.ra
            case 5:
                return self.rb
            case 6:
                return self.rc
            # case 7:
            #     raise ValueError("Invalid operand")
        raise ValueError("Invalid operand")      

    def combo_str(self, operand: int) -> str:
        match operand:
            case 0:
                return '0'
            case 1:
                return '1'
            case 2:
                return '2'
            case 3:
                return '3'
            case 4:
                return 'RA'
            case 5:
                return 'RB'
            case 6:
                return 'RC'
            # case 7:   
            #     raise ValueError("Invalid operand")        
        raise ValueError("Invalid operand")      

    def adv(self, operand: int):
        numerator = self.ra
        denominator = 2**self.combo(operand)
        self.ra = numerator // denominator
    
    def adv_str(self, operand: int):
        return f"ADV: RA = RA // 2^{self.combo_str(operand)}"

    def bxl(self, operand: int):
        self.rb = self.rb ^ operand

    def bxl_str(self, operand: int):
        return f"BXL: RB = RB XOR {operand}"


    def bst(self, operand: int):
        self.rb = self.combo(operand) % 8

    def bst_str(self, operand: int):
        return f"BST: RB = {self.combo_str(operand)} % 8"


    def jnz(self, operand: int):
        if self.ra == 0:
            pass
        else:
            self.ip = operand
            self.jp = True

    def jnz_str(self, operand: int):
        return f"NJZ: IF RA != 0: GOTO #{str(operand)}"

    def bxc(self, operand: int):
        self.rb = self.rb ^ self.rc

    def bxc_str(self, operand: int):
        return f"BXC: RB = RB XOR RC"

    def out(self, operand: int):
        v = self.combo(operand) % 8
        self.stdout.append(v)

    def out_str(self, operand: int):
        return f"OUT: {self.combo_str(operand)} % 8"

    def bdv(self, operand: int):
        numerator = self.ra
        denominator = 2**self.combo(operand)
        self.rb = numerator // denominator

    def bdv_str(self, operand: int):
        return f"BDV: RB = RA // 2^{self.combo_str(operand)}"

    def cdv(self, operand: int):
        numerator = self.ra
        denominator = 2**self.combo(operand)
        self.rc = numerator // denominator

    def cdv_str(self, operand: int):
        return f"CDV: RC = RA // 2^{self.combo_str(operand)}"

    def disassemble(self):
        adr = 0
        for idx in range(0, len(self.mem), 2):
            opcode = self.mem[idx]
            operand = self.mem[idx + 1]
            op = OpCode(opcode)
            print(f'{adr:03d}\t', end='')
            match op:
                case OpCode.ADV:
                    print(self.adv_str(operand))
                case OpCode.BXL:
                    print(self.bxl_str(operand))
                case OpCode.BST:
                    print(self.bst_str(operand))
                case OpCode.JNZ:
                    print(self.jnz_str(operand))
                case OpCode.BXC:
                    print(self.bxc_str(operand))
                case OpCode.OUT:
                    print(self.out_str(operand))
                case OpCode.BDV:
                    print(self.bdv_str(operand))
                case OpCode.CDV:
                    print(self.cdv_str(operand))
            adr += 2


def part1(filename: str) -> str:
    ra, rb, rc, pr = read_data(filename)

    c = Computer(ra, rb, rc, pr)
    c.run()

    return c.get_stdout()


def test_sample2_part2():
    ra, rb, rc, pr = read_data('sample2.txt')
    c = Computer(ra, rb, rc, pr)

    c.reset(ra=117440)
    c.run()
    assert(c.get_stdout() == '0,3,5,4,3,0')
    assert(c.stdout == c.mem)


def disassemble(filename: str):
    ra, rb, rc, pr = read_data(filename)
    c = Computer(ra, rb, rc, pr)

    c.disassemble()


# ic.disable()

assert ic(part1('./sample.txt')) == '4,6,3,5,6,3,5,2,1,0'
assert ic(part1('./input.txt')) == '7,1,3,4,1,2,6,7,1'


# test_sample2_part2()

# ic(part1('./sample2.txt'))


# disassemble('./sample2.txt')

# 000     ADV: RA = RA // 2^3
# 002     OUT: RA % 8
# 004     NJZ: IF RA != 0: GOTO #0


# def sample2():
#     res = ''
#     ra = 117440
#     rb = 0
#     rc = 0
#     while ra != 0:
#         ra = ra // 2**3
#         res += str(ra % 8)
#     assert res == '035430'

# sample2()

# disassemble('./input.txt')

# 000     BST: RB = RA % 8
# 002     BXL: RB = RB XOR 5
# 004     CDV: RC = RA // 2^RB
# 006     ADV: RA = RA // 2^3
# 008     BXC: RB = RB XOR RC
# 010     BXL: RB = RB XOR 6
# 012     OUT: RB % 8
# 014     NJZ: IF RA != 0: GOTO #0


# def challenge():
#     res = ''
#     ra = 46187030
#     rb = 0
#     rc = 0
#     while ra != 0:
#         rb = ra % 8
#         rb = rb ^ 5
#         rc = ra // 2**rb
#         ra = ra // 2**3
#         rb = rb ^ rc
#         rb = rb ^ 6
#         res += str(rb % 8)
#     assert res == '713412671'

# challenge()


def compute_challenge(ra: int) -> int:
    res = 0
    ra = 46187030
    rb = 0
    rc = 0

    while ra != 0:
        rb = ra % 8
        rb = rb ^ 5
        rc = ra // 2**rb
        ra = ra // 2**3
        rb = rb ^ rc
        rb = rb ^ 6
        res = res * 10 + (rb % 8)

    return res

assert compute_challenge(46187030) == 713412671


def compute_challenge_2(ra: int) -> int:
    res = 0
    rc = 0
    while ra != 0:
        # rc = ra >> (ra & 7 ^ 5) 
        # rb = (ra & 7) ^ 3 ^ 7 & rc

        # rc = ra >> ((ra & 7) ^ 5)
        # rb = (ra ^ rc ^ 3 ) & 7

        # rc = ra >> ((ra & 7) ^ 5)
        # rb = (ra ^ rc ^ 3 ) & 7
        rb = (ra ^ (ra >> ((ra & 7) ^ 5)) ^ 3 ) & 7

        res = res * 10 + rb
        ra = ra >> 3

    return res

assert compute_challenge_2(46187030) == 713412671


def compute_challenge_3(ra: int) -> int:

    res = 0
    # rc = 0
    while ra != 0:
        # rc = ra >> (ra & 7 ^ 5) 
        # rb = (ra & 7) ^ 3 ^ 7 & rc

        # rc = ra >> ((ra & 7) ^ 5)
        # rb = (ra ^ rc ^ 3 ) & 7

        # rc = ra >> ((ra & 7) ^ 5)
        # rb = (ra ^ rc ^ 3 ) & 7


        # rb = (ra >> ((ra & 7) ^ 5)) ^ 3 ^ ra
        # rb = (ra >> (ra & 7 ^ 5 & 7)) ^ 3 ^ ra
        # rb = (ra >> (( (ra & 2) | ((~ra | ~7) & 5 )) )) ^ 3 ^ ra
        shift = ((ra & 7) ^ 5)
        rb = ((ra >> shift) ^ ((ra & 7) ^ 3)) & 7
        res = res * 10 + rb
        ra = ra >> 3

    return res


assert compute_challenge_2(372212742271220) == 56312351775523512
assert compute_challenge_2(136902135580827) == 2415750340165530
assert compute_challenge_3(136902135580827) == 2415750340165530


def part2() -> int:
    expected_rb = list(reversed([2, 4, 1, 5, 7, 5, 0, 3, 4, 0, 1, 6, 5, 5, 3, 0]))
    ra = 0
    def solve_rec(ra, idx_rb):
        if idx_rb == len(expected_rb):
            return ra >> 3
        
        for oct_value in range(0, 8):
            potential_ra = ra + oct_value
            computed_rb = ((((potential_ra % 8) ^ 5) ^ (potential_ra // (1 << ((potential_ra % 8) ^ 5)))) ^ 6) & 7

            if computed_rb == expected_rb[idx_rb]:
                next_ra = solve_rec(potential_ra << 3, idx_rb + 1)
                if next_ra:
                    return next_ra

        return None

    ra = solve_rec(ra, 0)

    assert compute_challenge_3(ra) == 2415750340165530

    return ra


assert ic(part2()) == 109019476330651

# assert ic(compute_challenge_3(136902135580827)) == 2415750340165530
# assert ic(compute_challenge_3(109019485802241)) == 2415750340165530

# 109019476330651 (good one!)
# 109019485802241
# 136902135580827
# 136902148099849

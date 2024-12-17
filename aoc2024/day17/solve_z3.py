from z3 import Optimize, BitVec

# 000     BST: RB = RA % 8
# 002     BXL: RB = RB XOR 5
# 004     CDV: RC = RA // 2^RB
# 006     ADV: RA = RA // 2^3
# 008     BXC: RB = RB XOR RC
# 010     BXL: RB = RB XOR 6
# 012     OUT: RB % 8
# 014     NJZ: IF RA != 0: GOTO #0

opt = Optimize()
s = BitVec('s', 64)

ra = s
rb = 0
# rc = 0

for x in [2, 4, 1, 5, 7, 5, 0, 3, 4, 0, 1, 6, 5, 5, 3, 0]:
    # rb = ra % 8
    # rb = rb ^ 5
    # rc = ra / (1 << rb)
    # ra = ra / (1 << 3)
    # rb = rb ^ rc
    # rb = rb ^ 6

    rb = (((ra & 7) ^ 5) ^ (ra / (1 << ((ra & 7) ^ 5)))) ^ 6
    ra = ra / (1 << 3)

    opt.add((rb % 8) == x)
opt.add(ra == 0)

opt.minimize(s)

if str(opt.check()) == 'sat':
    print(opt.model().eval(s))


# found: 136902135580827
# found: 109019485802241
# found: 109019476330651 (good one!)

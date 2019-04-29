from decimal import Decimal as D, getcontext

getcontext().prec = 100


def contfrac_to_frac(seq):
    num, den = 1, 0
    for u in reversed(seq):
        num, den = den + num * u, num
    return num, den


def CF(num1, n=10):
    a = [int(num1)]
    num = num1 % 1  # Mantissa
    while num != 1:
        num = 1 / num
        whole_num = int(num)
        a.append(whole_num)
        num -= whole_num
        if len(a) == n + 1:
            break
    return a


pi = D(31415926535897932384626433832795028841971693993751) / D(10 ** 49)
a = CF(pi, n=27)  # n represents length of CF
print(a)
# Expected output
# [3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, 2, 1, 1, 2, 2, 2, 2, 1, 84, 2, 1,
# 1, 15, 3, 13]

num, den = contfrac_to_frac(a[0] + a[1:])
print(num, den)

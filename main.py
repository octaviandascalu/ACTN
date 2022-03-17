# Implement Reed-Solomon encoding/decoding using the algorithms dis-
# cussed in class. For simplicity, consider s = 1 (a single error may be
# corrected). Use as few modular inversions operations as possible. (10p)

import sympy
import random


def gen_p(n):
    return sympy.randprime(2 ** (n - 1) + 1, 2 ** n - 1)


#####################Encoding#####################

def base_10_to_p(m, p):
    r = []
    while m:
        r.append(m % p)
        m = m // p
    # r.reverse()
    # print(r)
    return r


def P(a, k, p, x):
    val = 0
    for i in range(k - 1, 0, -1):  # indexarea e de la 0
        val = (val + a[i - 1]) * x
    return val % p


def encode(a, k, s, p):
    y = []
    n = k + 2 * s
    for i in range(1, n + 1):
        y.append(P(a, k, p, i))
    return y


def encoding(k, s, p, m):
    a = base_10_to_p(int(m), p)
    return encode(a, k, s, p)


#####################Decoding#####################

def inv_mod(x, p):
    return pow(x, -1, p)


def f_c_worst():
    f_c = 0
    for i in A:
        prod = 1
        for j in A:
            if j != i:
                prod *= (j * inv_mod((j - i) % p, p))
        f_c += (z[i - 1] * prod) % p
    print(f_c % p)


def f_c_k():
    f_c = 0
    for i in A:
        prod1 = 1
        prod2 = 1
        for j in A:
            if j != i:
                prod1 *= j
                prod2 *= ((j - i) % p)
        f_c += (z[i - 1] * prod1 * inv_mod(prod2, p)) % p
    print(f_c % p)


###!!!!De regandit!!!! ~ probabil de adus la num comun tot
# def f_c_1():
#     f_c = 0
#     for i in A:
#         prod1 = 1
#         prod2 = 1
#         for j in A:
#             if j != i:
#                 prod1 *= j
#                 prod2 *= ((j - i) % p)
#         f_c += (z[i - 1] * prod1 * inv_mod(prod2, p)) % p
#     print(f_c % p)


def multiply(P1, P2):
    n = len(P1)
    m = len(P2)
    prod = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            prod[i + j] += P1[i] * P2[j]
    return prod


def add(P1, P2):
    n = len(P1)
    m = len(P2)
    sum = [0] * max(n, m)
    for i in range(n):
        sum[i] = P1[i]
    for i in range(m):
        sum[i] += P2[i]
    return sum


def printP(P):
    n = len(P)
    for i in range(n):
        print(P[i], end="");
        if (i != 0):
            print(" * x ^", i, end="");
        if (i != n - 1):
            print(" + ", end="");
    print("\n")


printP(multiply([1, -1], [1, 1]))
printP(multiply([5, 0, 10, 6], [1, 2, 4]))
printP(add([5, 0, 10, 6], [1, 2, 4]))


def get_P():
    P = []
    print(A)
    for i in A:
        prod1 = [1]
        prod2 = 1
        for j in A:
            if j != i:
                prod1 = multiply(prod1, [-j, 1])
                prod2 *= ((j - i) % p)

        # adunam polin
        # aux = [(z[i - 1] * i * inv_mod(prod2, p)) % p for i in prod1]
        # prod1 = aux
        # P = list(map(lambda x, y: (x + y) % p, P, prod1))
    # print(P)


# get_P()
#####################Main#####################

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    encoding(3, 1, 11, 29)
    p = gen_p(162)
    print("Un numar prim mare (peste 161 biti):", p)
    print("Codificarea lui k = 3, s = 1, p = 11 si m = 29:", encoding(3, 1, 11, "29"))

    k = 3
    p = 11
    # y = [9, 0, 6, 5, 8]
    z = [9, 2, 6, 5, 8]

    A = random.sample(range(1, len(z) + 1), k + 1)
    print(A)

    f_c_worst()
    f_c_k()

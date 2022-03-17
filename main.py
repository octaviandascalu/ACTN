# Implement Reed-Solomon encoding/decoding using the algorithms dis-
# cussed in class. For simplicity, consider s = 1 (a single error may be
# corrected). Use as few modular inversions operations as possible. (10p)

import sympy
import random


def gen_p(n):
    return sympy.randprime(2 ** (n - 1) + 1, 2 ** n - 1)


#####################Encoding#####################

def base_10_to_p(m, p):
    print("Reprezentarea lui ", m, "in baza", p, end=" ")
    r = []
    while m:
        r.append(m % p)
        m = m // p
    # r.reverse()
    print(":", r)
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


def multiply(P1, P2):  # de ad %p
    n = len(P1)
    m = len(P2)
    prod = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            prod[i + j] = (prod[i + j] + P1[i] * P2[j]) % p
    return prod


def add(P1, P2):
    n = len(P1)
    m = len(P2)
    sum = [0] * max(n, m)
    for i in range(n):
        sum[i] = P1[i]
    for i in range(m):
        sum[i] = (sum[i] + P2[i]) % p
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


# printP(multiply([1, -1], [1, 1]))
# printP(multiply([5, 0, 10, 6], [1, 2, 4]))
# printP(add([5, 0, 10, 6], [1, 2, 4]))


def f_c_worst(A):
    f_c = 0
    for i in A:
        prod = 1
        for j in A:
            if j != i:
                prod *= (j * inv_mod((j - i) % p, p))
        f_c += (z[i - 1] * prod) % p
    return f_c % p


def f_c_k(A):
    f_c = 0
    for i in A:
        prod1 = 1
        prod2 = 1
        for j in A:
            if j != i:
                prod1 *= j
                prod2 *= ((j - i) % p)
        f_c += (z[i - 1] * prod1 * inv_mod(prod2, p)) % p
    return f_c % p


def P_dec(A):
    pol = [0]
    for i in A:
        prod1 = [1]
        prod2 = 1
        for j in A:
            if j != i:
                prod1 = multiply(prod1, [-j, 1])
                prod2 = ((prod2 * (i - j)) % p)
        pol = add(pol, [(x * z[i - 1] * inv_mod(prod2, p)) % p for x in prod1])
    # pol.reverse()
    return pol


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

def decodificare():
    f_c = -1
    A = None
    while f_c != 0:
        A = random.sample(range(1, len(z) + 1), k + 1)
        # print(A)
        # f_c = f_c_worst(A)
        # print(f_c)

        f_c = f_c_k(A)
        # print(f_c)
    print("A:", A)
    print("f_c:", f_c)
    print("Decodificare:", P_dec(A))


#####################Main#####################

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    p = gen_p(162)
    print("Un numar prim mare (peste 161 biti):", p)

    k = 3
    p = 11
    s = 1
    print("Codificarea lui k = 3, s = 1, p = 11 si m = 29:", encoding(k, s, p, "29"))
    # y = [9, 0, 6, 5, 8]
    z = [9, 2, 6, 5, 8]
    decodificare()

    k = 4
    p = 13
    s = 1
    print("Codificarea lui k = 4, s = 1, p = 13 si m = 205:", encoding(k, s, p, "205"))
    # y = [0, 12, 5, 0, 5, 2]
    z = [0, 9, 5, 0, 5, 2]
    decodificare()

    k = 5
    p = 31
    s = 1
    print("Codificarea lui k = 5, s = 1, p = 31 si m = 65785:", encoding(k, s, p, "65785"))
    # y = [25, 2, 30, 1, 3, 10, 6]
    z = [25, 11, 30, 1, 3, 10, 6]
    decodificare()

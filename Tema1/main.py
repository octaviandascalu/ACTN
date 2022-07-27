import sympy
import random
import time


def gen_p(n):
    return sympy.randprime(2 ** (n - 1) + 1, 2 ** n - 1)


# ####################Encoding#####################

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
    k = len(a) + 1
    return encode(a, k, s, p), k


# ####################Decoding#####################

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
        print(P[i], end="")
        if (i != 0):
            print(" * x ^", i, end="")
        if (i != n - 1):
            print(" + ", end="")
    print("\n")


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


def f_c_1(A):
    numarator = 0
    numitor = 1
    for i in A:
        termen = z[i - 1]
        for j in A:
            if j != i:
                termen = termen * j
                for l in A:
                    if l != j:
                        termen = termen * (l - j)
        termen = termen % p
        numarator = (numarator + termen) % p

    for i in A:
        for j in A:
            if j != i:
                numitor = (numitor * (i - j)) % p
    f_c = numarator * inv_mod(numitor, p)
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
    pol = pol[1:-1]
    return pol


def decodificare():
    f_c = None
    A = None
    k_time = None
    kk_1_time = None
    one_time = None
    while f_c != 0:
        A = random.sample(range(1, len(z) + 1), k + 1)
        # print(A)
        start_time = time.time()
        f_c = f_c_worst(A)
        kk_1_time = time.time() - start_time
        # print(f_c)

        start_time = time.time()
        f_c = f_c_k(A)
        k_time = time.time() - start_time
        # print(f_c)

        start_time = time.time()
        f_c = f_c_1(A)
        one_time = time.time() - start_time
        # print(f_c)
    print("k time %s vs kk-1 time %s vs 1 time %s" % (k_time, kk_1_time, one_time))
    print("A:", A)
    print("f_c:", f_c)
    print("Decodificare:", P_dec(A), "\n")


# ####################Main#####################

if __name__ == '__main__':
    p = gen_p(162)
    print("Un numar prim mare (peste 161 biti):", p)
    k = 0
    s = 1
    y, k = encoding(k, s, p,
                    "2678789503665347665881359631006576495673545615576715765365461585463545644645353434334229")
    print("Codificare instanta mare:", y)
    z = y
    z[2] = 1
    decodificare()

    k = 0
    p = 11
    s = 1
    y, k = encoding(k, s, p, "29")
    print("Codificarea lui k = 3, s = 1, p = 11 si m = 29:", y)
    # y = [9, 0, 6, 5, 8]
    z = [9, 2, 6, 5, 8]
    decodificare()

    k = 0
    p = 13
    s = 1
    y, k = encoding(k, s, p, "45620")
    print("Codificarea lui k = 6, s = 1, p = 13 si m = 45620:", y)
    # y = [6, 10, 0, 8, 9, 2, 0, 7]
    z = [6, 10, 0, 8, 1, 2, 0, 7]
    decodificare()

    k = 0
    p = 13
    s = 1
    y, k = encoding(k, s, p, "456206")
    print("Codificarea lui k = 7, s = 1, p = 13 si m = 456206:", y)
    # y = [12, 8, 8, 7, 0, 12, 3, 12, 7]
    z = [12, 8, 8, 7, 0, 12, 7, 12, 7]
    decodificare()
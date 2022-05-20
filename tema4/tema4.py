import numpy as np
import sympy as sp
import random as rd


def gen_prime(n):
    return sp.randprime(2 ** (n - 1) + 1, 2 ** n - 1)


def gen_factorization(n):
    f = []

    d = 2
    while n % d == 0:
        f.append(d)
        n /= d

    for i in range(3, int(np.sqrt(n)) + 1, 2):
        # while i divides n , print i and divide n
        while n % i == 0:
            f.append(i)
            n = n / i

    if n > 1:
        f.append(int(n))
    # print(f)
    f = list(set(f))
    f.sort()
    return f


def gen_shanks_input():
    print("gen_shanks_input")
    p = gen_prime(16)
    alpha = PrimitiveRoot2(p)
    while alpha == -1:
        print("what")
        p = gen_prime(32)
        alpha = PrimitiveRoot2(p)
    return (p, alpha)


def GenerateQuadraticNonResidue(p):
    print("GenerateQuadraticNonResidue")
    if p % 4 == 3:
        print("alpha1:", -1)
        return -1
    if p % 8 == 5:
        print("alpha1:", 2)
        return 2

    a = rd.randint(2, p - 1)
    while LegendreJacobi(a, p) != -1:
        a = rd.randint(2, p - 1)

    print("alpha1:", a)
    return a


def PrimitiveRoot2(p):
    print("PrimitiveRoot2")
    alpha = GenerateQuadraticNonResidue(p)

    print("alpha2:", alpha)
    ok = 1
    f = gen_factorization(p - 1)
    print("f:", f)
    for r in f:
        if r != 2 and pow(alpha, (p - 1) // r, p) == 1:
            ok = 0
    if ok == 1:
        return alpha


def LegendreJacobi(a, n):
    t = 1
    while a != 0:
        while a % 2 == 0:
            a = a / 2
            if n % 8 in {-3, 3}:
                t = -t
        (a, n) = (n, a)
        if a % 4 == 3 and n % 4 == 3:
            t = -t
        a = a % n
    return t


def shanks(p, alpha, beta):
    m = int(np.ceil(np.sqrt(p - 1)))
    print("alpha3:", alpha)
    # babysteps
    l = []
    for j in range(m):
        l.append((j, pow(alpha, j, p)))
    l.sort(key=lambda x: x[1])
    print("l:", l)

    # giant steps
    for i in range(m):
        val = (beta * pow(alpha, -i * m, p)) % p
        # print("val:", val)
        for k in range(m):
            if l[k][1] == val:
                j = l[k][0]
                return (i * m + j) % p
    return "No discret log found"


def gen_sph_input():
    p = gen_prime(32)
    alpha = GenerateQuadraticNonResidue(p)
    return p, alpha


def sph():
    return 0


if __name__ == '__main__':
    # print("shanks:", shanks(13, 2, 11))
    # print(gen_factorization(48048))

    (p, alpha) = gen_shanks_input()
    beta = rd.randint(1, p - 1)
    print("shanks(", p, ",", alpha, ",", beta, "):", shanks(p, alpha, beta))

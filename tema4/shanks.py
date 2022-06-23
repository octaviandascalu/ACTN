import random as rd
import sympy as sp
import numpy as np


def gen_prime(n):
    return sp.randprime(2 ** (n - 1) + 1, 2 ** n - 1)


def randomZp(p):
    a = rd.randint(1, p - 1)
    while sp.gcd(a, p) != 1:
        a = rd.randint(1, p - 1)
    return a


def gen_input_shanks():
    p = gen_prime(32)
    # alpha = PrimitiveRoot1(p)
    alpha = PrimitiveRoot2(p)
    beta = rd.randint(1, p - 1)
    return p, alpha, beta


def factorization(n):
    f = []
    while n % 2 == 0:
        f.append(2)
        n /= 2

    d = 3
    while d * d <= n:
        while n % d == 0:
            f.append(d)
            n /= d
        d += 2

    if n > 1:
        f.append(d)

    f = list(set(f))
    f.sort()
    print("f:", f)
    return f


def LegendreJacobi(a, n):
    t = 1
    while a != 0:
        while a % 2 == 0:
            a = a / 2
            if n % 8 == 3 or n % 8 == -1:
                t = -t
        (a, n) = (n, a)
        if a % 4 == 3 and n % 4 == 3:
            t = -t
        a = a % n
    return t


def GenerateQuadraticNonResidue(p):
    if p % 4 == 3:
        return p - 1
    if p % 8 == 5:
        return 2

    a = randomZp(p)
    while LegendreJacobi(a, p) != -1:
        a = randomZp(p)

    return a


def PrimitiveRoot1(p):
    alpha = randomZp(p)
    ok = 1
    f = factorization(p - 1)
    for r in f:
        if pow(alpha, (p - 1) // r, p) == 1:
            ok = 0
    if ok == 1:
        return alpha


def PrimitiveRoot2(p):
    alpha = GenerateQuadraticNonResidue(p)
    ok = 1
    f = factorization(p - 1)
    if f[0] == 2:
        f.pop(0)
    for r in f:
        if pow(alpha, (p - 1) // r, p) == 1:
            ok = 0
    if ok == 1:
        return alpha


def Shanks(p, alpha, beta):
    m = int(np.ceil(np.sqrt(p - 1)))
    l = []
    # baby steps
    for j in range(0, m):
        l.append((j, pow(alpha, j, p)))
    l.sort(key=lambda x: x[1])
    print("l:", l)

    # giant steps
    for i in range(0, m):
        val = (beta * pow(alpha, -i * m, p)) % p
        print("val:", val)
        for k in range(0, m):
            if l[k][1] == val:
                j = l[k][0]
                return i * m + j
    return "No discrete algorithm "


if __name__ == '__main__':
    epsilon = Shanks(13, 2, 11)
    print("Shanks(13, 2, 11):", epsilon, end="\n\n")
    print(pow(2, epsilon, 13) == 11)
    print()

    # p, alpha, beta = gen_input_shanks()
    # while alpha is None:
    #     p, alpha, beta = gen_input_shanks()
    # print("p, alpha, beta:", p, alpha, beta)
    # epsilon = Shanks(p, alpha, p - 1)
    # print("Shanks(", p, ",", alpha, ",", p - 1, "):", epsilon, end="\n\n")
    # print(pow(alpha, epsilon, p) == beta)

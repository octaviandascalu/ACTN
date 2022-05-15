import random as rd
import sympy as sp
import numpy as np


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


def gen_prime(n):
    return sp.randprime(2 ** (n - 1) + 1, 2 ** n - 1)


def gen_input_SPH():
    p = gen_prime(32)
    alpha = PrimitiveRoot1(p)
    beta = rd.randint(1, p - 1)
    return p, alpha, beta


def randomZp(p):
    a = rd.randint(1, p - 1)
    while sp.gcd(a, p) != 1:
        a = rd.randint(1, p - 1)
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


def Silver_Pohlig_Hellman(alpha, n, beta):
    return None

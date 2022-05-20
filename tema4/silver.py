import random as rd
import sympy as sp
import numpy as np

import math


def factorization(n):
    f = []
    if n % 2 == 0:
        power = 0
        while n % 2 == 0:
            power += 1
            n /= 2
        f.append([2, power])

    d = 3
    while d * d <= n:
        power = 0
        while n % d == 0:
            power += 1
            n /= d
        if power > 0:
            f.append([d, power])
        d += 2

    if n > 1:
        f.append([int(n), 1])

    print("f:", f)
    return f


def gen_prime(n):
    return sp.randprime(2 ** (n - 1) + 1, 2 ** n - 1)


def gen_input_SPH():
    p = gen_prime(32)
    f = factorization(p - 1)
    alpha = PrimitiveRoot1(p)
    beta = rd.randint(1, p - 1)
    return p, f, alpha, beta


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


def discrete_log_3_56(n, alpha, beta):
    return None


def compute_x_i(n, alpha, beta, p_i, e_i):
    x_i = 0
    q = p_i
    e = e_i
    gama = 1
    l__1 = 0
    alpha_inv = pow(alpha, n / q)

    for j in range(e):
        gama = gama * pow(alpha, l__1 * pow(q, j - 1))
        beta_inv = pow(beta * pow(gama, -1), n / pow(q, j + 1))
        l_j = math.log(beta_inv, alpha_inv)
        x_i += l_j * pow(q, j)
        print("l_j,q^j:", l_j, pow(q, j))

    return x_i % pow(p_i, e_i)


def CRT(f, x_i, p):
    x = 0

    for i in range(0, len(f)):
        M_i = (p - 1) // pow(f[i][0], f[i][1])
        y_i = pow(M_i, -pow(f[i][0], f[i][1]))
        x = (x + (x_i[i] * M_i * y_i) % (p - 1)) % (p - 1)

    return x


def Silver_Pohlig_Hellman(p, f, alpha, beta):
    x_i = []
    for p_i, e_i in f:
        x_i.append(compute_x_i(n=p,
                               alpha=alpha,
                               beta=beta,
                               p_i=p_i,
                               e_i=e_i))
    print("x", x_i)
    return CRT(f, x_i, p)


if __name__ == '__main__':
    # factorization(40)
    print("Silver_Pohlig_Hellman(41, [[2, 3], [5, 1]], 6, 5):",
          Silver_Pohlig_Hellman(p=41,
                                f=factorization(40),
                                alpha=6,
                                beta=5),
          end="\n\n")
    print()

    # p, alpha, beta = gen_input_shanks()
    # while alpha is None:
    #     p, alpha, beta = gen_input_shanks()
    # print("p, alpha, beta:", p, alpha, beta)
    # print("Shanks(", p, ",", alpha, ",", p - 1, "):", Shanks(p, alpha, p - 1), end="\n\n")

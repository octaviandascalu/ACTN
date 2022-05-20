import random as rd
import sympy as sp
import numpy as np
from sympy.ntheory import discrete_log
from shanks import PrimitiveRoot2


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


def gen_input_SPH(biti=32):
    p = gen_prime(biti)
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
    for r, q in f:
        print(r, "--", p)
        if pow(alpha, (p - 1) // r, p) == 1:
            ok = 0
    if ok == 1:
        return alpha


def TCR(x, m):
    while len(x) > 1:
        new_x = pow(m[1], -1, m[0]) * x[0] * m[1] + pow(m[0], -1, m[1]) * x[1] * m[0]

        new_m = m[0] * m[1]

        x.pop(0)
        x.pop(0)
        x.insert(0, new_x % new_m)

        m.pop(0)
        m.pop(0)
        m.insert(0, new_m)

    return x[0]


def SPH(n, beta, alpha, factors):
    x = []

    for q, e in factors:
        y = 1
        l = [0]

        alpha_ = pow(alpha, n // q, n)
        # print("alpha, alpha_, n, q:", alpha, alpha_, n, q)

        for j in range(e):
            y = y * pow(alpha, l[j] * pow(q, j - 1, n), n)
            beta_ = pow(beta * pow(y, -1, n), n // pow(q, j + 1), n)
            l.append(int(discrete_log(n, beta_, alpha_)))

        print(l)
        l.pop(0)  # stergem l-1

        x_i = 0
        power = 1

        for j in range(len(l)):
            x_i += l[j] * power
            power *= q

        x.append(x_i % n)

    return TCR(x, [pow(factor[0], factor[1]) for factor in factors])


# def log(p, alpha, beta):
#     m = int(np.ceil(np.sqrt(p - 1)))
#     l = []
#     # baby steps
#     for j in range(0, m):
#         l.append((j, pow(alpha, j, p)))
#     l.sort(key=lambda x: x[1])
#     # print("l:", l)
#
#     alpha_m = pow(alpha, -m, p)
#     # print("alpha_m:", alpha_m)
#     # print("m:", m)
#     # print("alpha:", alpha)
#     y = beta
#
#     # giant steps
#     for i in range(0, m):
#         # print("y:", y)
#         for k in range(0, m):
#             if l[k][1] == y:
#                 j = l[k][0]
#                 return i * m + j
#         y = y * alpha_m
#     return "No discrete algorithm "


if __name__ == '__main__':
    p = 41
    alpha = 6
    beta = 5
    factors = [(2, 3), (5, 1)]

    epsilon = SPH(p, beta, alpha, factors)
    print("SPH(p={}, beta={}, alpha={}, factors={}):".format(p, beta, alpha, factors), epsilon)
    print(pow(alpha, epsilon, p) == beta)
    print()

    p, f, alpha, beta = gen_input_SPH(10)
    while alpha is None:
        p, f, alpha, beta = gen_input_SPH(10)

    epsilon = SPH(p, beta, alpha, factors)
    print("SPH(p={}, beta={}, alpha={}, factors={}):".format(p, beta, alpha, factors), epsilon)
    print(pow(alpha, epsilon, p) == beta)
    print()

    # # SPH big
    # print("SPH big")
    # p = 22708823198678103974314518195029102158525052496759285596453269189798311427475159776411276642277139650833937
    # factors = [(2, 4), (104729, 8), (224737, 8), (350377, 4)]
    # alpha = generate_primitive_root_2(p, factors)
    # while not is_primitive_root(alpha, p):
    #     alpha = generate_primitive_root_2(p, factors)
    # # alpha = primitive_root(p)
    #
    # beta = randint(0, p - 1)
    # print("ALPHA: ", alpha)
    # print("BETA: ", beta)
    # res = SPH(p, beta, alpha, factors)
    # print(res)

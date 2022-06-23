import random as rd
from sympy.ntheory import discrete_log, is_primitive_root
from shanks import gen_prime, GenerateQuadraticNonResidue

def factorizare(n):
    f = []
    if n % 2 == 0:
        power = 0
        while n % 2 == 0:
            power += 1
            n /= 2
        f.append((2, power))

    d = 3
    while d * d <= n:
        power = 0
        while n % d == 0:
            power += 1
            n /= d
        if power > 0:
            f.append((d, power))
        d += 2

    if n > 1:
        f.append((int(n), 1))

    print("f:", f)
    return f

def modular_multiplicative_inverse(a, modulo):
    return pow(int(a), -1, modulo)


def PrimitiveRoot2(p, factors):
    alpha = GenerateQuadraticNonResidue(p)
    ok = True
    for f, e in factors:
        if f != 2:
            if pow(alpha, (p - 1) // f, p) == 1:
                ok = False
    if ok:
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


def SPH(p, factors, alpha, beta):
    x = []
    for q, e in factors:
        y = 1
        l = [0]

        alpha_ = pow(alpha, p // q, p)
        # print("alpha, alpha_, n, q:", alpha, alpha_, n, q)

        for j in range(e):
            y = y * pow(alpha, int(l[j] * pow(q, j - 1)), p)
            beta_ = pow(beta * modular_multiplicative_inverse(y, p), p // pow(q, j + 1), p)
            l.append(discrete_log(p, beta_, alpha_))

        # print(l)
        l.pop(0)  # stergem l-1

        x_i = 0
        power = 1

        for j in range(len(l)):
            x_i += l[j] * power
            power *= q

        x.append(x_i % p)

    return int(TCR(x, [pow(p, e) for p, e in factors]))


if __name__ == '__main__':
    # SPH curs

    p = 41
    alpha = 6
    beta = 5
    factors = [(2, 3), (5, 1)]
    epsilon = SPH(p, factors, alpha, beta)
    print("SPH(p={}, beta={}, alpha={}, factors={}):".format(p, beta, alpha, factors), epsilon)
    print(epsilon)
    print(pow(alpha, epsilon, p) == beta)

    print()
    p = 4057616897
    factors = factorizare(p-1)
    alpha = PrimitiveRoot2(p, factors)
    while not is_primitive_root(alpha, p):
        alpha = PrimitiveRoot2(p, factors)

    beta = rd.randint(1, p - 1)
    epsilon = SPH(p, factors, alpha, beta)
    print("SPH(p={}, beta={}, alpha={}, factors={}):".format(p, beta, alpha, factors), epsilon)

    print(epsilon)
    print(pow(alpha, epsilon, p) == beta)


    # SPH 1024
    print()

    p = gen_prime(32)
    factors = factorizare(p-1)
    alpha = PrimitiveRoot2(p, factors)
    while alpha is None:
        alpha = PrimitiveRoot2(p, factors)

    beta = rd.randint(1, p - 1)
    epsilon = SPH(p, factors, alpha, beta)
    print("SPH(p={}, beta={}, alpha={}, factors={}):".format(p, beta, alpha, factors), epsilon)

    print(epsilon)
    print(pow(alpha, epsilon, p) == beta)

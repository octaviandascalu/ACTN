import sympy
import random
import time

statistics = False

garnerTime = []
decryptTime = []
henselTime = []


def gen_prime(n):
    return sympy.randprime(2 ** (n - 1) + 1, 2 ** n - 1)


def inv_mod(x, p):
    return pow(x, -1, p)


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


# ####################Multiprime RSA#####################

# - generarea corecta a parametrilor (p, q, r, n, e, d, y) folosind numere mari  (1p)
def gen_instMPrime():
    p = gen_prime(512)

    q = p
    while q == p:
        q = gen_prime(512)

    r = p
    while r == p or r == q:
        r = gen_prime(512)

    n = p * q * r
    phi_n = (p - 1) * (q - 1) * (r - 1)
    e = gen_prime(16)
    d = inv_mod(e, phi_n)

    x = 105651
    x = x % n
    y = encrypt(x, e, n)
    if not statistics:
        print("x is ", x)
        print_instMPrime(p, q, r, n, phi_n, e, d, y)
    return p, q, r, n, phi_n, e, d, y


def encrypt(x, e, n):
    return pow(x, e, n)


def decrypt(y, d, n):
    start = time.time()
    x = pow(y, d, n)
    end = time.time() - start
    if not statistics:
        print("decrypt time: ", end)
    else:
        decryptTime.append(end);
    return x


def garner(p, q, r, d, y):
    start = time.time()

    mp = pow(y % p, d % (p - 1), p)
    mq = pow(y % q, d % (q - 1), q)
    mr = pow(y % r, d % (r - 1), r)

    x = mp
    alpha = ((mq - x) % q * inv_mod(mp, q)) % q
    x += alpha * mp
    alpha = ((mr - x) % r * inv_mod(mp * mq, r)) % r
    x += alpha * mp * mq

    end = time.time() - start
    if not statistics:
        print("garner time: ", end)
    else:
        garnerTime.append(end);
    return x


def print_instMPrime(p, q, r, n, phi_n, e, d, y):
    print("p=", p)
    print("q=", q)
    print("r=", r)
    print("n=", n)
    print("phi_n=", phi_n)
    print("e=", e)
    print("d=", d)
    print("y=", y)


# - decriptarea folosind Teorema Chineza a Resturilor (2p)
#         (trebuie sa implementati algoritmul lui Garner)
# - comparatii intre cele doua metode (1p)
def multiprimeRSA():
    p, q, r, n, phi_n, e, d, y = gen_instMPrime()
    x = decrypt(y, d, n)
    if not statistics:
        print("x is ", x)
    x = garner(p, q, r, d, y)
    if not statistics:
        print("x is ", x)


# ####################Multipower RSA#####################
# - generarea corecta a parametrilor (p, q,  n, e, d, y) folosind numere mari  (1p)
def gen_instMPower():
    p = gen_prime(512)

    q = p
    while q == p:
        q = gen_prime(512)

    n = p * p * q
    phi_n = p * (p - 1) * (q - 1)
    e = gen_prime(16)
    d = inv_mod(e, phi_n)

    x = 105651
    x = x % n
    y = encrypt(x, e, n)
    if not statistics:
        print("x is ", x)
        print_instMPower(p, q, n, phi_n, e, d, y)
    return p, q, n, phi_n, e, d, y


def hensel(p, q, e, d, y):
    start = time.time()

    mq = pow(y % q, d % (q - 1), q)
    x0 = pow(y % p, d % (p - 1), p)
    alpha = (y - pow(x0, e, p * p)) // p
    x1 = (alpha * inv_mod(e * pow(x0, e - 1, p), p)) % p

    x = x1 * p + x0
    alpha = ((mq - x) % q * inv_mod(x, q)) % q
    x += alpha * x
    end = time.time() - start
    if not statistics:
        print("garner time: ", end)
    else:
        henselTime.append(end)
    return x


def print_instMPower(p, q, n, phi_n, e, d, y):
    print("p^2=", p * p)
    print("q=", q)
    print("n=", n)
    print("phi_n=", phi_n)
    print("e=", e)
    print("d=", d)
    print("y=", y)


def multipowerRSA():
    p, q, n, phi_n, e, d, y = gen_instMPower()
    x = decrypt(y, d, n)

    if not statistics:
        print("x is ", x)
    x = hensel(p, q, e, d, y)
    if not statistics:
        print("x is ", x)


# - decriptarea folosind Teorema Chineza a Resturilor si Lema lui Hensel (2p)
# - comparatii intre cele doua metode (1p)


# ####################Lanturi aditive#####################
def base_10_to_p(m, p):
    print("Reprezentarea lui ", m, "in baza", p, end=" ")
    r = []
    while m:
        r.append(m % p)
        m = m // p
    # r.reverse()
    print(":", r)
    return r


# - folosind metoda binara de la stanga la dreapta (0.5p)
def Lr_bin_exp(x, n, m):
    n = base_10_to_p(n, 2)
    y = 1
    k = len(n)
    for i in reversed(range(k)):
        y = (y * y) % m
        if n[i] == 1:
            y = (y * x) % m
    return y


def Lr_beta_exp(x, n, m):
    beta = 4
    vx = []
    vx.append(1)
    for i in range(1, beta):
        vx.append((vx[i - 1] * x) % m)
    n = base_10_to_p(n, beta)
    y = 1
    k = len(n)
    for i in reversed(range(k)):
        y = pow(y, beta, m)
        y = (y * vx[n[i]]) % m
    return y


# - folosind metoda ferestrei fixe de la stanga la dreapta (0.5p)
# - folosind metoda ferestrei glisante de la stanga la dreapta (0.5p)
# - comparatii intre cele trei metode (0.5p)

if __name__ == '__main__':
    statistics = False
    multiprimeRSA()

    statistics = True
    for i in range(30):
        multiprimeRSA()
    print("Average Decrypt Time is ", sum(decryptTime) / len(decryptTime))
    print("Average Garner Time is ", sum(garnerTime) / len(garnerTime))

    statistics = False
    multipowerRSA()

    decryptTime = []
    statistics = True
    for i in range(30):
        multipowerRSA()
    print("Average Decrypt Time is ", sum(decryptTime) / len(decryptTime))
    print("Average Hensel Time is ", sum(henselTime) / len(henselTime))

import sympy
import random
import time

statistics = False

garnerTime = []
decryptTime = []
henselTime = []
Lr_bin_expTime = []
Lr_beta_expTime = []
Lr_slid_wind_expTime = []


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
    while gcd(e, phi_n) != 1:
        e = gen_prime(16)
    d = inv_mod(e, phi_n)

    x = 105651786786786
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

    x = 105651786786786
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
        print("hensel time: ", end)
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
    # print("Reprezentarea lui ", m, "in baza", p, end=" ")
    r = []
    while m:
        r.append(m % p)
        m = m // p
    # print(":", r)
    return r


def garner1(p, q, r, d, y):
    start = time.time()

    mp = Lr_bin_exp(y % p, d % (p - 1), p)
    mq = Lr_bin_exp(y % q, d % (q - 1), q)
    mr = Lr_bin_exp(y % r, d % (r - 1), r)

    x = mp
    alpha = ((mq - x) % q * inv_mod(mp, q)) % q
    x += alpha * mp
    alpha = ((mr - x) % r * inv_mod(mp * mq, r)) % r
    x += alpha * mp * mq

    end = time.time() - start
    if not statistics:
        print("Lr_bin_exp time: ", end)
    else:
        Lr_bin_expTime.append(end);
    return x


def garner2(p, q, r, d, y):
    start = time.time()

    mp = Lr_beta_exp(y % p, d % (p - 1), p)
    mq = Lr_beta_exp(y % q, d % (q - 1), q)
    mr = Lr_beta_exp(y % r, d % (r - 1), r)

    x = mp
    alpha = ((mq - x) % q * inv_mod(mp, q)) % q
    x += alpha * mp
    alpha = ((mr - x) % r * inv_mod(mp * mq, r)) % r
    x += alpha * mp * mq

    end = time.time() - start
    if not statistics:
        print("Lr_beta_exp time: ", end)
    else:
        Lr_beta_expTime.append(end);
    return x


def garner3(p, q, r, d, y):
    start = time.time()

    vv = 2
    mp = Lr_slid_wind_exp(y % p, d % (p - 1), p, vv)
    mq = Lr_slid_wind_exp(y % q, d % (q - 1), q, vv)
    mr = Lr_slid_wind_exp(y % r, d % (r - 1), r, vv)

    x = mp
    alpha = ((mq - x) % q * inv_mod(mp, q)) % q
    x += alpha * mp
    alpha = ((mr - x) % r * inv_mod(mp * mq, r)) % r
    x += alpha * mp * mq

    end = time.time() - start
    if not statistics:
        print("Lr_beta_exp time: ", end)
    else:
        Lr_slid_wind_expTime.append(end);
    return x


def multiprimeRSA1():
    p, q, r, n, phi_n, e, d, y = gen_instMPrime()
    x = decrypt(y, d, n)
    if not statistics:
        print("x is ", x)
    x = garner(p, q, r, d, y)
    if not statistics:
        print("x is ", x)
    x = garner1(p, q, r, d, y)
    if not statistics:
        print("x is ", x)
    x = garner2(p, q, r, d, y)
    if not statistics:
        print("x is ", x)
    x = garner3(p, q, r, d, y)
    if not statistics:
        print("x is ", x)


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


# - folosind metoda ferestrei fixe de la stanga la dreapta (0.5p)

def Lr_beta_exp(x, n, m):
    beta = 16
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


# - folosind metoda ferestrei glisante de la stanga la dreapta (0.5p)
def Lr_slid_wind_exp(x, n, m, vv):
    vx = [0] * pow(2, vv)
    vx[1] = (x % m)
    vx[2] = (vx[1] * vx[1]) % m
    for w in range(3, pow(2, vv), 2):
        vx[w] = (vx[w - 2] * vx[2]) % m
    n = base_10_to_p(n, 2)
    y = 1
    k = len(n)
    i = k - 1
    while i >= 0:
        if n[i] == 0:
            y = (y * y) % m
            i -= 1
        else:
            j = i - vv + 1
            while j < i and n[j] != 1:
                j += 1
            for l in range(1, i - j + 1 + 1):
                y = (y * y) % m

            coef = 0
            for l in range(j, i + 1):
                if n[l] == 1:
                    coef += pow(2, l - j)
            y = (y * vx[coef]) % m
            i = j - 1
    return y
    # - comparatii intre cele trei metode (0.5p)


if __name__ == '__main__':
    # print(Lr_bin_exp(5, 10, 170))
    # print(Lr_bin_exp(67878478,2274722,643))
    # print(pow(67878478,2274722,643))
    statistics = False
    multiprimeRSA()

    statistics = True
    for i in range(30):
        multiprimeRSA()
    print()
    print("Average Decrypt Time is ", sum(decryptTime) / len(decryptTime))
    print("Average Garner Time is ", sum(garnerTime) / len(garnerTime))
    print()

    statistics = False
    multipowerRSA()

    decryptTime = []
    statistics = True
    for i in range(30):
        multipowerRSA()
    print()
    print("Average Decrypt Time is ", sum(decryptTime) / len(decryptTime))
    print("Average Hensel Time is ", sum(henselTime) / len(henselTime))
    print()

    statistics = False
    multiprimeRSA1()
    statistics = True
    for i in range(30):
        multiprimeRSA1()
    print()
    print("Average Lr_bin_exp Time is ", sum(Lr_bin_expTime) / len(Lr_bin_expTime))
    print("Average Lr_beta_exp Time is ", sum(Lr_beta_expTime) / len(Lr_beta_expTime))
    print("Average Lr_slid_wind_exp Time is ", sum(Lr_slid_wind_expTime) / len(Lr_slid_wind_expTime))
    print()

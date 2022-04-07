import sympy
import random
import time


def gen_prime(n):
    return sympy.randprime(2 ** (n - 1) + 1, 2 ** n - 1)


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(a, b):
    return a * b / gcd(a, b)


# ####################Multiprime RSA#####################

# - generarea corecta a parametrilor (p, q, r, n, e, d, y) folosind numere mari  (1p)
# - decriptarea folosind Teorema Chineza a Resturilor (2p)
#         (trebuie sa implementati algoritmul lui Garner)
# - comparatii intre cele doua metode (1p)


# ####################Multipower RSA#####################
# - generarea corecta a parametrilor (p, q,  n, e, d, y) folosind numere mari  (1p)
# - decriptarea folosind Teorema Chineza a Resturilor si Lema lui Hensel (2p)
# - comparatii intre cele doua metode (1p)


# ####################Lanturi aditive#####################
# - folosind metoda binara de la stanga la dreapta (0.5p)
# - folosind metoda ferestrei fixe de la stanga la dreapta (0.5p)
# - folosind metoda ferestrei glisante de la stanga la dreapta (0.5p)
# - comparatii intre cele trei metode (0.5p)

if __name__ == '__main__':
    print(gen_prime(512))
    print(gcd(12, 16))

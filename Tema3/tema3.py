import random
import math
import time


#########################################Solovay-Strassen#########################################
# 1. Implement the Solovay-Strassen primality test.
# For computing the Jacobi symbol, use the rules discussed in AFCS class (5p)

def Jacobi(a, n):
    if n < 0 or n % 2 == 0:
        raise Exception("WOW")
    a = a % n
    j = 1
    while a != 0:
        while a % 2 == 0:
            a = a / 2
            if n % 8 == 3 or n % 8 == 5:  # reg cu 2
                j = -j

        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:  # leg reciprocitatii
            j = -j

        a = a % n

    if n == 1:
        return j
    else:
        return 0


def Solovay_Strassen(n, t):
    for i in range(1, t):
        a = random.randint(2, n - 2)
        r = pow(a, (n - 1) // 2, n)
        if r != 1 and r != n - 1:
            return "composite"
        s = Jacobi(a, n)
        if r % n != s % n:
            return "composite"
    return "prime"


#########################################Lucas-Lehmer#########################################
# 2. Implement the Lucas-Lehmer primality test for Mersenne numbers.
# For performing the modular reduction modulo a Mersenne number, use the algorithm discussed in class  (5p)

timp_LL = []
timp_LLRM = []


def Lucas_Lehmer(s):
    n = pow(2, s) - 1
    # print("n=", n)
    f = 2
    while f <= math.floor(math.sqrt(s)):
        if s % f == 0:
            return "composite"
        f += 1

    u = 4

    start = time.time()
    for k in range(0, s - 2):
        u = (u * u - 2) % n
    end = time.time() - start
    timp_LL.append(end)

    # print(n, " - ", end=" ")

    if u == 0:
        return "prime"
    else:
        return "composite"


def mersenne_modular_reduction(s, a):
    a1 = a // pow(2, s)
    a0 = a % pow(2, s)
    r = a0 + a1
    if (a0 + a1 < pow(2, s) - 1):
        return a0 + a1
    else:
        return a0 + a1 - (pow(2, s) - 1)


def Lucas_Lehmer_modular_reduction(s):
    n = pow(2, s) - 1
    # print("n=", n)
    f = 2
    while f <= math.floor(math.sqrt(s)):
        if s % f == 0:
            return "composite"
        f += 1

    u = 4

    start = time.time()
    for k in range(0, s - 2):
        u = mersenne_modular_reduction(s, u * u - 2)
    end = time.time() - start
    timp_LLRM.append(end)

    # print(n, " - ", end=" ")

    if u == 0:
        return "prime"
    else:
        return "composite"


# print(Jacobi(5, 1))
# print(Jacobi(5, 9))
# print(Jacobi(5, 99))
# print(Jacobi(5, 13))
# print(Jacobi(10, 15))

print("Jacobi(20, 41) = ", Jacobi(20, 41))  # 1
print("Jacobi(25, 57) = ", Jacobi(25, 57))  # 1
print("Jacobi(19, 45) = ", Jacobi(19, 45))  # 1
print("Jacobi(8, 21) = ", Jacobi(8, 21))  # -1
print("Jacobi(5, 21) = ", Jacobi(5, 21))  # 1

print("Solovay_Strassen(121, 10): ", Solovay_Strassen(121, 10))
print("Solovay_Strassen(173, 10): ", Solovay_Strassen(173, 10))
print("Solovay_Strassen(997, 100): ", Solovay_Strassen(997, 100))
print("Solovay_Strassen(1000, 5): ", Solovay_Strassen(1000, 5))

print("Indici numere prime Mersenne:")
for i in range(3, 2500):
    if (Lucas_Lehmer(i) == "prime"):
        print(i, end=" ")
print()

print("Indici numere prime Mersenne:")
for i in range(3, 2500):
    if (Lucas_Lehmer_modular_reduction(i) == "prime"):
        print(i, end=" ")
print()

print("Timpi LL ", timp_LL)
print("Timpi LLRM ", timp_LLRM)

print("Timp mediu LL ", sum(timp_LL)/len(timp_LL))
print("Timp mediu LLRM ", sum(timp_LLRM)/len(timp_LLRM))

print("Delta timp LL ", [x - y for (x, y) in zip(timp_LL, timp_LLRM)])

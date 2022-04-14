import random
import math


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

def Lucas_Lehmer(s):
    n = pow(2, s) - 1
    # print("n=", n)
    f = 2
    while f <= math.floor(math.sqrt(s)):
        if s % f == 0:
            return "composite"
        f += 1

    u = 4

    for k in range(1, s - 2 + 1):
        u = (u * u - 2) % n

    if u == 0:
        return "prime"
    else:
        return "composite"


# print(Jacobi(5, 1))
# print(Jacobi(5, 9))
# print(Jacobi(5, 99))
# print(Jacobi(5, 13))
# print(Jacobi(10, 15))

print(Jacobi(20, 41))  # 1
print(Jacobi(25, 57))  # 1
print(Jacobi(19, 45))  # 1
print(Jacobi(8, 21))  # -1
print(Jacobi(5, 21))  # 1

print(Solovay_Strassen(121, 10))
print(Solovay_Strassen(173, 10))
print(Solovay_Strassen(997, 100))
print(Solovay_Strassen(1000, 5))

for i in range(3, 2000):
    if (Lucas_Lehmer(i) == "prime"):
        print(i)

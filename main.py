# Implement Reed-Solomon encoding/decoding using the algorithms dis-
# cussed in class. For simplicity, consider s = 1 (a single error may be
# corrected). Use as few modular inversions operations as possible. (10p)

#####################Encoding#####################

def base_10_to_p(m, p):
    r = []
    while m:
        r.append(m % p)
        m = m // p
    # r.reverse()
    # print(r)
    return r


def P(a, k, p, x):
    val = 0
    for i in range(k - 1, 0, -1):  # indexarea e de la 0
        val = (val + a[i - 1]) * x
    return val % p


def encode(a, k, s, p):
    y = []
    n = k + 2 * s
    for i in range(1, n + 1):
        y.append(P(a, k, p, i))
    return y


def encoding(k, s, p, m):
    a = base_10_to_p(m, p)
    print(encode(a, k, s, p))
    return 0


#####################Decoding#####################

def inv_mod(x, p):
    return pow(x, -1, p)


p = 11
y = [9, 0, 6, 5, 8]
z = [9, 2, 6, 5, 8]

A = {1, 3, 4, 5}


def f_c_worst():
    f_c = 0
    for i in A:
        prod = 1
        for j in A:
            if j != i:
                prod *= (j * inv_mod((j - i) % p, p))
        f_c += (z[i - 1] * prod) % p
    print(f_c % p)


def f_c_k():
    f_c = 0
    for i in A:
        prod1 = 1
        prod2 = 1
        for j in A:
            if j != i:
                prod1 *= j
                prod2 *= ((j - i) % p)
        f_c += (z[i - 1] * prod1 * inv_mod(prod2, p)) % p
    print(f_c % p)

###!!!!De regandit!!!! ~ probabil de adus la num comun tot
# def f_c_1():
#     f_c = 0
#     for i in A:
#         prod1 = 1
#         prod2 = 1
#         for j in A:
#             if j != i:
#                 prod1 *= j
#                 prod2 *= ((j - i) % p)
#         f_c += (z[i - 1] * prod1 * inv_mod(prod2, p)) % p
#     print(f_c % p)


f_c_worst()
f_c_k()

#####################Main#####################

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
# encoding(3, 1, 11, 29)

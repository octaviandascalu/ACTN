# Implement Reed-Solomon encoding/decoding using the algorithms dis-
# cussed in class. For simplicity, consider s = 1 (a single error may be
# corrected). Use as few modular inversions operations as possible. (10p)


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    encoding(3, 1, 11, 29)

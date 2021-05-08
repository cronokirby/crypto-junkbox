INF = '∞'

def exp(x, e, P):
    """
    Calculate x^e % P, assuming x is already reduced
    """
    x_squared = x
    acc = 1
    while e > 0:
        if e & 1:
            acc = (acc * x_squared) % P
        e >>= 1
        x_squared = (x_squared * x_squared) % P
    return acc


def mod_inv(x, P):
    """
    Calculate the modular inverse of x % P
    """
    return exp(x, P - 2, P)


def check_point(x, y, P):
    return (y ** 2) % P == (x ** 3 + 1) % P


def points(P):
    for x in range(P):
        for y in range(P):
            if check_point(x, y, P):
                yield (x, y)

def point_add(p1, p2, P):
    if p1 == INF:
        return p2
    if p2 == INF:
        return p1
    if p1[1] == (P - p2[1]) % P:
        return INF
    if p1 == p2:
        l = (3 * p1[0] ** 2) * mod_inv(p1[1], P) % P
    else:
        l = (p2[1] - p1[1]) * mod_inv(p2[0] - p1[0], P) % P
    x = (l * l - p1[0] - p2[0]) % P
    y = (l * (p1[0] - x) - p1[1]) % P
    return (x, y)

def generated_set(q, P):
    acc = q
    yield INF
    while acc != INF:
        yield acc
        acc = point_add(acc, q, P)
    

def cross_generated(list_a, list_b, P):
    for p1 in list_a:
        for p2 in list_b:
            yield point_add(p1, p2, P)
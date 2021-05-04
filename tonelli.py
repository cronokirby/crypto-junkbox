def exp(x, e, P):
    x_squared = x % P
    acc = 1
    while e > 0:
        if e & 1:
            acc = (acc * x_squared) % P
        e >>= 1
        x_squared = (x_squared * x_squared) % P
    return acc


def find_non_square(P):
    e = (P - 1) >> 1
    x = 2
    while exp(x, e, P) == 1:
        x += 1
    return x


class Constants:
    def __init__(self, P):
        self.c1 = 0
        self.c2 = P - 1
        while self.c2 & 1 == 0:
            self.c1 += 1
            self.c2 >>= 1
        self.c3 = (self.c2 - 1) >> 1
        self.c4 = find_non_square(P)
        self.c5 = exp(self.c4, self.c2, P)

    def __str__(self):
        return str((self.c1, self.c2, self.c3, self.c4, self.c5))

    def __repr__(self):
        return self.__str__()


def square_root(x, P, constants=None):
    if constants is None:
        constants = Constants(P)
    z = exp(x, constants.c3, P)
    t = (z * z * x) % P
    z = (z * x) % P
    b = t
    c = constants.c5
    for i in range(constants.c1, 1, -1):
        for j in range(1, i - 1):
            b = (b * b) % P
        if b != 1:
            z = (z * c) % P
        c = (c * c) % P
        if b != 1:
            t = (t * c) % P
        b = t
    return z

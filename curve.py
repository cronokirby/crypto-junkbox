class Modulus:
    """
    Represents a Modulus, enabling modular arithmetic
    """

    def __init__(self, P):
        self.P = P

    def reduce(self, x):
        """
        Reduce x modulo this modulus
        """
        return x % self.P

    def add(self, a, b):
        """
        Calculate a + b % P, assuming a and b are already reduced
        """
        added = a + b
        if added >= self.P:
            added -= self.P
        return added

    def mul(self, a, b):
        """
        Calculate a * b % P assuming a and b are already reduced
        """
        return (a * b) % self.P

    def exp(self, x, e):
        """
        Calculate x^e % P, assuming x is already reduced
        """
        x_squared = x
        acc = 1
        while e > 0:
            if e & 1:
                acc = self.mul(acc, x_squared)
            e >>= 1
            x_squared = self.mul(x_squared, x_squared)
        return acc

    def invert(self, x):
        """
        Calculate x^(-1) % P, assuming x is already reduced
        """
        return self.exp(x, self.P - 2)


class Curve:
    """
    Represent a Montgomery Curve By^2 = x^3 + Ax^2 + x, over the field Z_P
    """

    def __init__(self, B, A, P):
        self.B = B
        self.A = A
        self.P = P

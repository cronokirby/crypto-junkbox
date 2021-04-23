from dataclasses import dataclass


@dataclass
class Modulus:
    """
    Represents a Modulus, enabling modular arithmetic
    """

    P: int

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


@dataclass
class Curve:
    """
    Represent a Montgomery Curve By^2 = x^3 + Ax^2 + x
    """

    P: int
    B: int
    A: int

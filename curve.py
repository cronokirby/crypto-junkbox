from dataclasses import dataclass


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
    
    def negate(self, x):
        """
        Calculate -x % P
        """
        if x == 0:
            return x
        return self.P - x

    def sub(self, a, b):
        return self.add(a, self.negate(b))

    def __str__(self):
        return f"Modulus({self.P:_X})"

    def __repr__(self):
        return self.__str__()


@dataclass
class Point:
    """
    Represents a Point on the curve
    """

    is_infinity: bool
    x: int
    y: int

    @staticmethod
    def infinity():
        return Point(True, 0, 0)

    def to_projective(self):
        if self.infinity:
            return Projective(0, 1, 0)
        return Projective(self.x, self.y, 1)
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        if self.is_infinity:
            return "Point(∞)"
        return f"Point(x={self.x:_X} y={self.y:_X})"


@dataclass
class Projective:
    x: int
    y: int
    z: int

    def project(self, P: Modulus):
        if self.z == 0:
            return Point.infinity()
        zinv = P.invert(self.z)
        return Point(False, self.x * zinv, self.y * zinv)


class Curve:
    """
    Represent a Montgomery Curve By^2 = x^3 + Ax^2 + x, over the field Z_P
    """

    def __init__(self, B, A, P: Modulus):
        self.B = B
        self.A = A
        self.P = P

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Curve(B={self.B:_X}, A={self.A:_X}, P={self.P})"

    def poly(self, x):
        x2 = self.P.mul(x, x)
        x3 = self.P.mul(x, x2)
        out = self.P.add(x3, x)
        return self.P.add(out, self.P.mul(self.A, x2))

    def add(self, p: Point, q: Point):
        if p.is_infinity:
            return q
        if q.is_infinity:
            return p
        l = 0
        if p.x == q.x:
            if p.y != q.y:
                return Point.infinity()
            l = self.P.reduce(3 * p.x * p.x + 2 * self.A * p.x + 1)
            l = self.P.mul(l, self.P.invert(self.P.reduce(2 * self.B * p.y)))
        l = self.P.sub(q.y, p.y)
        l = self.P.mul(l, self.P.invert(self.P.sub(q.x, q.y)))
        l2 = self.P.mul(l, l)
        out_x = self.P.reduce(self.B * l2 - self.A - p.x - q.x)
        out_y = self.P.reduce(l * (p.x - out_x) - p.y)
        return Point(False, out_x, out_y)


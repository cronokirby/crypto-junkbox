P = (1 << 255) - 19


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


def from_le_bytes(le_bytes):
    acc = 0
    for b in le_bytes[::-1]:
        acc = (acc << 8) + b
    return acc


def to_le_bytes(num):
    acc = []
    while num > 0:
        acc.append(num & 0xFF)
        num >>= 8
    return acc


def x25519(k_bytes, u_bytes):
    k_bytes_cp = k_bytes[:]
    k_bytes_cp[0] &= 248
    k_bytes_cp[31] &= 127
    k_bytes_cp[31] |= 64
    print("scalar", [f'{b:02X}' for b in k_bytes_cp])
    k = from_le_bytes(k_bytes_cp)
    u = (from_le_bytes(u_bytes) & ((1 << 255) - 1)) % P
    x1 = u
    x2 = 1
    z2 = 0
    x3 = u
    z3 = 1
    swap = 0
    print(f'x1 {x1:_X}')
    print(f'x2 {x2:_X}')
    print(f'x3 {x2:_X}')
    for b in range(255, -1, -1):

        bit = (k >> b) & 1
        swap ^= bit
        print(f'b {b} bit {bit} swap {swap}')
        print(f'  x2 {x2:_X}')
        print(f'  z2 {z2:_X}')
        print(f'  x3 {x3:_X}')
        print(f'  z3 {z3:_X}')
        if swap:
            (x2, x3) = (x3, x2)
            (z2, z3) = (z3, z2)
        swap = bit

        A = x2 + z2
        AA = A * A
        B = x2 - z2
        BB = B * B
        E = AA - BB
        C = x3 + z3
        D = x3 - z3
        DA = D * A
        CB = C * B
        x3 = (DA + CB) ** 2
        x3 = x3 % P
        z3 = x1 * ((DA - CB) ** 2)
        z3 = z3 % P
        x2 = AA * BB
        x2 = x2 % P
        z2 = E * (AA + 121665 * E)
        z2 = z2 % P
    if swap:
        (x2, x3) = (x3, x2)
        (z2, z3) = (z3, z2)
    print('final')
    print(f'  x2 {x2:_X}')
    print(f'  z2 {z2:_X}')
    print(f'  z2^-1 {exp(z2, P - 2, P) % P:_X}')
    out = (x2 * exp(z2, P - 2, P)) % P
    print(f'out {out:_X}')
    return to_le_bytes(out)


def bytes_from_string(s):
    acc = []
    for i in range(0, len(s), 2):
        acc.append(int(s[i : i + 2], 16))
    return acc


def print_bytes(s):
    return '[' + ', '.join(f'0x{b:02X}' for b in bytes_from_string(s)) + ']'


if __name__ == "__main__":
    tests = [
        (
            "a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4",
            "e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c",
        ),
        (
            "4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d",
            "e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a413",
        ),
    ]
    for k_bytes, u_bytes in tests:
        print("k_bytes", k_bytes);
        print("u_bytes", u_bytes);
        print(
            "".join(
                f"{b:02x}"
                for b in x25519(bytes_from_string(k_bytes), bytes_from_string(u_bytes))
            )
        )

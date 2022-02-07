import math


class Q:
    def __init__(self, n: int, d: int):
        if d == 0:
            raise ZeroDivisionError

        if d < 0:  # let n always carry the sign.
            n *= -1
            d *= -1

        gcd = math.gcd(n, d)
        self.n = int(n / gcd)
        self.d = int(d / gcd)

    def reciprocal(self):
        return self.__class__(self.d, self.n)

    def __pow__(self, other):
        if other.n == 0:
            return self.__class__(1, 1)
        n = self.n
        d = self.d
        for _ in range(0, other.n - 1):
            n *= n
            d *= d
        # shrug
        n = math.pow(n, 1 / other.d)
        if n != int(n):
            raise ValueError("irrational")
        d = math.pow(d, 1 / other.d)
        if d != int(d):
            raise ValueError("irrational")
        return self.__class__(int(n), int(d))

    def __mul__(self, other):
        return self.__class__(self.n * other.n, self.d * other.d)

    def __sub__(self, other):
        return self + self.__class__(-1 * other.n, other.d)

    def __eq__(self, other):
        return (
            # self.n == other.n == 0 or
            self.n == other.n
            and self.d == other.d
        )

    def __add__(self, other):
        lcm = math.lcm(self.d, other.d)
        self_c = int(lcm / self.d)
        other_c = int(lcm / other.d)
        n = self_c * self.n + other_c * other.n
        assert self_c * self.d == other_c * other.d
        d = self_c * self.d
        return self.__class__(n, d)

    def __truediv__(self, other):
        return self * other.reciprocal()

    def __repr__(self):
        return "%d/%d" % (self.n, self.d)


if __name__ == "__main__":

    q1 = Q(3, 9)
    q2 = Q(4, 8)
    assert q1 == Q(1, 3)
    assert q2 == Q(1, 2)
    assert q1 * q2 == Q(1, 6)
    assert q1 + q2 == Q(5, 6)
    assert q1 / q2 == Q(2, 3)
    assert q1 - q2 == Q(-1, 6)

    assert Q(-1, 2) == Q(1, -2)
    assert Q(-1, -1) == Q(1, 1)
    assert Q(0, 1) == Q(0, 3)

    assert Q(2, 1) ** Q(2, 1) == Q(4, 1)
    assert Q(4, 1) ** Q(1, 2) == Q(2, 1)

    for exception_test, expected_exception in [
        (lambda: Q(1 / 0), ZeroDivisionError),
        (lambda: Q(2 / 0), ZeroDivisionError),
        (lambda: Q(1 / 0), ZeroDivisionError),
        (lambda: Q(1.1, 3), TypeError),
        (lambda: Q(3, 1.1), TypeError),
        (lambda: Q(2, 1) ** Q(1, 2), ValueError),
    ]:
        try:
            exception_test()
            raise AssertionError
        except expected_exception:
            pass

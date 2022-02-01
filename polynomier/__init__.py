import re
from itertools import product, chain


def super_int(num_string):
    lookup = {
        0: chr(0x2070),
        1: chr(0x00B9),
        2: chr(0x00B2),
        3: chr(0x00B3),
        4: chr(0x2074),
        5: chr(0x2075),
        6: chr(0x2076),
        7: chr(0x2077),
        8: chr(0x2078),
        9: chr(0x2079),
    }
    result = ""
    for c in num_string:
        result += lookup[int(c)]
    return result


class Polynomial:
    """The required terms dictionary takes the form

    {
        <exponent>: (set(<symbols>), <coefficient>)
    }

    Examples:
    """

    def __init__(self, *coeff, as_dict=None):
        if as_dict is None:
            self.coeff = dict(enumerate(coeff))
        else:
            self.coeff = as_dict

    def coeff_items(self):
        for index, coeff in self.coeff.items():
            if coeff != 0:
                yield index, coeff

    def __sub__(self, other):
        if not isinstance(other, Polynomial):
            other = Polynomial(other)
        return self + Polynomial(as_dict={i: -1 * c for (i, c) in other.coeff_items()})

    def __eq__(self, other):
        if self.degree != other.degree:
            return False
        for i in range(0, self.degree):
            if self.coeff.get(i, 0) != other.coeff.get(i, 0):
                return False
        return True

    def __pow__(self, n):
        if not isinstance(n, int):
            raise ValueError("Only positive integer exponenents supported.")
        if n == 0:
            return 1  # really?
        result = self
        for _ in range(0, n - 1):
            result *= result
        return result

    def div(self, other):
        remainder = self
        quotient = Polynomial()
        while remainder.degree > 1:
            term = Polynomial(
                as_dict={
                    remainder.degree
                    - other.degree: remainder.coeff[remainder.degree]
                    / other.coeff[other.degree]
                }
            )
            quotient += term
            remainder -= other * term
        return quotient, remainder

    def __floordiv__(self, other):
        quotient, _ = self.div(other)
        return quotient

    def __truediv__(self, other):
        quotient, remainder = self.div(other)
        return quotient + remainder

    def __mod__(self, other):
        _, remainder = self.div(other)
        return remainder

    def __add__(self, other):
        if not isinstance(other, Polynomial):
            other = Polynomial(other)
        indicies = set([i for (i, _) in chain(self.coeff_items(), other.coeff_items())])
        new_coeff = {}
        for index in indicies:
            new_coeff[index] = self.coeff.get(index, 0) + other.coeff.get(index, 0)
        return Polynomial(as_dict=new_coeff)

    def __mul__(self, other):
        if not isinstance(other, Polynomial):
            return Polynomial(as_dict={i: other * c for (i, c) in self.coeff_items()})
        else:
            expanded = [
                (a[0] + b[0], a[1] * b[1])
                for (a, b) in product(self.coeff_items(), other.coeff_items())
            ]
            max_index = max(i for (i, c) in expanded)
            new_coeff = {}
            for index in range(0, max_index + 1):
                new_coeff[index] = sum([c for (i, c) in expanded if i == index])
            return Polynomial(as_dict=new_coeff)

    def __call__(self, x):
        return sum([c * x ** i for i, c in self.coeff_items()])

    def is_root(self, x):
        return self(x) == 0

    @property
    def degree(self):
        indicies = [i for (i, _) in self.coeff_items()]
        if len(indicies) == 0:
            raise ValueError("Zero polynomial has undefined degree.")
        return max(indicies)

    def _get_term_repr(self, i):
        "how to implement shitty human syntax"
        c = self.coeff.get(i, 0)
        if c == 0:
            return ""
        exponent = "" if i < 2 else super_int(str(i))
        coeff = "" if i > 0 and c == 1 else str(c)
        variable = "" if i < 1 else "x"
        oper = "" if i == self.degree else " + "
        if c < 0:
            oper = "-" if i == self.degree else " - "
            if len(coeff) > 0:
                coeff = coeff.lstrip("-")
        return oper + coeff + variable + exponent

    def __repr__(self):
        result = []
        for i in sorted(self.coeff, reverse=True):
            result.append(self._get_term_repr(i))
        return "".join(result).lstrip(" +")


def parse_term(term):
    if not re.search(r"\d", term):
        if term.startswith("-"):
            term = "-1" + term.lstrip(" -")
        else:
            term = "1" + term.lstrip(" +")
    result = re.search("(?P<coeff>[-]?\d+(\.\d+)?)(?P<symbols>(?:[^\d]?).*)", term)
    coeff = float(result.group("coeff"))
    symbols = result.group("symbols").strip(" )(")
    indexes = set(re.findall("\^(\d+)", symbols))
    index = 1
    if len(indexes) > 1:
        raise ValueError
    if len(indexes) > 0:
        index = int(indexes.pop())
    symbols = set(re.sub("[\d^]", "", symbols))
    return index, symbols, coeff


def str_to_poly(string):
    results = string.replace(" ", "")
    results = results.replace("-", "@-")
    results = results.replace("+", "@+").lstrip("@")
    return [parse_term(term) for term in results.split("@")]


if __name__ == "__main__":

    assert str_to_poly("3x^2") == [(2, {"x"}, 3.0)]
    assert str_to_poly("-3x^3y^3") == [(3, {"x", "y"}, -3.0)]
    assert str_to_poly("-3x^3y^3 + 2y^2") == [(3, {"x", "y"}, -3.0), (2, {"y"}, 2.0)]
    assert str_to_poly("-3x^3y^3 + 2y^2 - y") == [
        (3, {"x", "y"}, -3.0),
        (2, {"y"}, 2.0),
        (1, {"y"}, -1.0),
    ]
    assert str_to_poly("-3x^3y^3 + 2y^2 - y + 3") == [
        (3, {"x", "y"}, -3.0),
        (2, {"y"}, 2.0),
        (1, {"y"}, -1.0),
        (1, set(), 3.0),
    ]

    p1 = Polynomial(0, 0, 1)
    print("p1 = %s" % p1)
    p2 = Polynomial(1, 0, 2)
    print("p2 = %s" % p2)
    p3 = p1 * p2
    print("p3 = p1 * p2 = %s" % p3)
    p4 = p3 + p2
    print("p4 = p3 + p2 = %s" % p4)
    p5 = p4 + 8
    print("p5 = p4 + 8 = %s" % p5)
    p6 = p3 - 8
    print("p6 = p3 - 8 = %s" % p6)
    p7 = p4 - p3
    print("p7 = p4 - p3 = %s" % p7)

    assert 36 == p3(2)
    assert 4 == p1(2)
    assert 9 == p2(2)
    assert Polynomial(1, 0, 3, 0, 2) == p4
    assert Polynomial(as_dict={4: 2, 2: 3, 0: 9}) == p5
    assert Polynomial(as_dict={4: 2, 2: 1, 0: -8}) == p6
    assert p7 == Polynomial(0, 0, 1) * 2 + 1

    p8 = Polynomial(1, 1)
    p9 = Polynomial(1, 1)
    print("(%s) * (%s) = %s" % (p8, p9, p8 * p9))

    p10 = Polynomial(1, 1)
    p11 = Polynomial(-1, 1)
    print("(%s) * (%s) = %s" % (p10, p11, p10 * p11))

    division = [
        (Polynomial(5, 2, 1, 3), Polynomial(1, 2, 1)),
        (Polynomial(-10, -3, 1), Polynomial(2, 1)),
        (Polynomial(-4, 0, -2, 1), Polynomial(-3, 1)),
    ]
    for dividend, divisor in division:
        quotient = dividend // divisor
        remainder = dividend % divisor
        assert dividend == divisor * quotient + remainder
        assert dividend / divisor == quotient + remainder

    rootable = Polynomial(-1, 0, 1)
    assert rootable.is_root(1)
    assert rootable.is_root(-1)

    has_complex_roots = Polynomial(1, 0, 1)
    assert has_complex_roots.is_root(1j)
    assert has_complex_roots.is_root(-1j)

    # see:
    # https://en.wikipedia.org/wiki/Polynomial_long_division#Finding_tangents_to_polynomial_functions
    r = 1
    divisor = Polynomial(-1, r) ** 2
    dividend = Polynomial(-42, 0, -12, 1)
    assert dividend % divisor == Polynomial(-32, -21)

import re
from itertools import product, chain
from . import super_int

class Polynomial:

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

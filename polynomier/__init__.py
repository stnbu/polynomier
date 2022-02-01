import re
from itertools import product, chain
from frozendict import frozendict as fd


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


############



def add(p0, p1):
    results = {}
    common_terms = set(p0) & set(p1)
    p0_ = p0.copy()
    p1_ = p1.copy()
    for key in common_terms:
        results[key] = p0[key] + p1[key]
        p0_.pop(key)
        p1_.pop(key)
    results.update(p0_)
    results.update(p1_)
    return {v: c for (v, c) in results.items() if c != 0}


# for now... define just field element (e.g. 3.95/aka float) multiplication
def mul(p0, r):
    results = {}
    for key, coeff in p0.items():
        results[key] = coeff * r
    return results


# which permits us to define sub as
def sub(p0, p1):
    return add(p0, mul(p1, -1))


def _get_symbol(sym, symbol_pows):
    for symbol, power in symbol_pows:
        if sym == symbol:
            return sym, power


def mul(p0, p1):
    results = {}
    for (vars0, coeff0), (vars1, coeff1) in product(p0.items(), p1.items()):
        vars0 = dict(vars0)
        vars1 = dict(vars1)
        new_vars = []
        for symbol in set(vars0) | set(vars1):
            power = vars0.get(symbol, 0) + vars1.get(symbol, 0)
            new_vars.append((symbol, power))

        results[fs(new_vars)] = coeff0 * coeff1
    return results


if __name__ == "__main__":

    for v in "abcdefghijklmnopqrstuvwxyz":
        globals()[v] = v

    p0 = {fd([(x, 2)]): 3, fd([(y, 1)]): 1}
    p1 = {fd([(x, 2)]): 2, fd([(y, 1)]): 1}
    assert add(p0, p1) == {fd({y: 1}): 2, fd({x: 2}): 5}

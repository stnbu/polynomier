from itertools import product
from frozendict import frozendict as fd


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


def _mulr(p0, r):
    results = {}
    for key, coeff in p0.items():
        results[key] = coeff * r
    return results


def sub(p0, p1):
    return add(p0, _mulr(p1, -1))


def mul(p0, p1):
    results = {}
    for (vars0, coeff0), (vars1, coeff1) in product(p0.items(), p1.items()):
        new_vars = {}
        for symbol in set(vars0) | set(vars1):
            new_vars[symbol] = vars0.get(symbol, 0) + vars1.get(symbol, 0)
        results.setdefault(fd(new_vars), 0)
        results[fd(new_vars)] += coeff0 * coeff1
    return results


class MultiPoly:
    def __init__(self, terms):
        self.terms = terms

    def __add__(self, other):
        return self.__class__(add(self.terms, other.terms))

    def __sub__(self, other):
        return self.__class__(sub(self.terms, other.terms))

    def __mul__(self, other):
        return self.__class__(mul(self.terms, other.terms))

    def __repr__(self):
        return repr(self.terms).replace("frozendict.frozendict", "fd")

    def __eq__(self, other):
        return self.terms == other.terms

    def __pow__(self, power):
        if power == 0:
            return self.__class__({fd(): 1})
        result = self
        for _ in range(0, power-1):
            result *= result
        return result

    def substitute(self, symbol, substitution):
        result = self.__class__(self.terms.copy())
        for vars, coeff in self.terms.items():
            if symbol not in vars:
                continue
            del result.terms[vars]
            new_vars = {}
            for sym, power in vars.items():
                if sym != symbol:
                    new_vars[sym] = power
                else:
                    expanded_symbol = substitution ** power
            new_poly = MultiPoly({fd(new_vars): coeff}) * expanded_symbol
            result += new_poly
        return result

if __name__ == "__main__":

    for v in "abcdefghijklmnopqrstuvwxyz":
        globals()[v] = v

    p0 = MultiPoly({fd([(x, 2)]): 3, fd([(y, 1)]): 1})
    p1 = MultiPoly({fd([(x, 2)]): 2, fd([(y, 1)]): 1})
    p2 = MultiPoly({fd({x: 1}): 1, fd(): -1})
    p3 = MultiPoly({fd({x: 2}): 1, fd(): -1})
    F_t = MultiPoly({fd({t: 1}): 1, fd(): -1})
    assert p0 + p1 == MultiPoly({fd({x: 2}): 5, fd({y: 1}): 2})
    assert p0 - p1 == MultiPoly({fd({x: 2}): 1})
    assert p0 * p1 == MultiPoly({fd({x: 4}): 6, fd({y: 1, x: 2}): 5, fd({y: 2}): 1})
    assert p2 ** 2 == MultiPoly({fd({x: 2}): 1, fd({x: 1}): -2, fd({}): 1})
    assert p3.substitute(x, F_t) == MultiPoly({fd({t: 2}): 1, fd({t: 1}): -2})

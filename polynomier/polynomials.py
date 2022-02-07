# TODO:
# * Write tests for fields other than R.
# * What if not a Field? What then!
# * See if we can include negative exponents.
# * Implement __div__ and family.
# * I guess s/MultiPoly/Polinomial/g
# * Q can be implemented elegantly including clean, readable output. Do that.
# * Maybe a latex printer.
# * Would it be reasonable to use sympy's expression tooling?

from itertools import product
from . import super_int, fd


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


def wrap(handler):
    def wrapper(self, other):
        if not isinstance(other, self.__class__):
            other = self.__class__({fd(): other})
        return self.__class__(handler(self.terms, other.terms))

    return wrapper


class Polynomial:
    __add__ = wrap(add)
    __sub__ = wrap(sub)
    __mul__ = wrap(mul)
    __add__ = wrap(add)

    def __init__(self, terms):
        self.terms = {vars: coeff for (vars, coeff) in terms.items() if coeff != 0}

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            other = self.__class__({fd(): other})
        return self.terms == other.terms

    def __pow__(self, power):
        if power == 0:
            return self.__class__({fd(): 1})
        result = self
        for _ in range(0, power - 1):
            result *= result
        return result

    def substitute(self, *args):
        result = self.__class__(self.terms.copy())
        for symbol, substitution in args:
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
                new_poly = self.__class__({fd(new_vars): coeff}) * expanded_symbol
                result += new_poly
        return result

    @classmethod
    def from_sympy_expr(cls, expr):
        raise NotImplemented

    def to_sympy_expr(self):
        from sympy import symbols
        from sympy.core.add import Add
        from sympy.core.mul import Mul
        from sympy.core.expr import ExprBuilder
        poly = ExprBuilder(Add, [0])
        for vars, coeff in self.terms.items():
            term =  ExprBuilder(Mul, [coeff])
            for symbol, power in vars.items():
                symbol = symbols(symbol)
                term.args.extend([symbol] * power)
            poly.args.append(term)
        return poly.build()

    def _get_term_repr(self, vars, coeff):
        results = "+ " if coeff > 0 else "- "
        if abs(coeff) != 1 or len(vars) == 0:
            results += str(abs(coeff))
        for symbol, power in sorted(vars.items()):
            results += "%s%s" % (symbol, "" if power == 1 else super_int(power))
        return results

    def _get_terms_repr(self):
        return repr(self.terms).replace("frozendict.frozendict", "fd")

    def __repr__(self):
        if not all([isinstance(c, (int, float)) for c in self.terms.values()]):
            return self._get_terms_repr()
        result = []
        degree = lambda term: -sum(term[0].values())
        for vars, coeff in sorted(self.terms.items(), key=degree):
            result.append(self._get_term_repr(vars, coeff))
        results = " ".join(result)
        results = results.lstrip(" +")
        if results[:2] == "- ":
            results = "-" + results[2:]
        return results  # happy, humans?

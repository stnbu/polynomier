from polynomier import Polynomial, MultiPoly, fd, str_to_poly
from polynomier.symbols import *


def test():

    # MultiPoly

    p0 = MultiPoly({fd([(x, 2)]): 3, fd([(y, 1)]): 1})
    assert repr(p0) == "3x² + y"
    p1 = MultiPoly({fd([(x, 2)]): 2, fd([(y, 1)]): 1})
    assert repr(p1) == "2x² + y"
    p2 = MultiPoly({fd({x: 1}): 1, fd(): -1})
    assert repr(p2) == "x - 1"
    p3 = MultiPoly({fd({x: 2}): 1, fd(): -1})
    assert repr(p3) == "x² - 1"
    p4 = p0 + p1
    assert repr(p4) == "5x² + 2y"
    assert p4 == MultiPoly({fd({x: 2}): 5, fd({y: 1}): 2})
    p5 = p0 - p1
    assert repr(p5) == "x²"
    assert p5 == MultiPoly({fd({x: 2}): 1})
    p6 = p0 * p1
    assert repr(p6) == "6x⁴ + 5x²y + y²"
    assert p6 == MultiPoly({fd({x: 4}): 6, fd({y: 1, x: 2}): 5, fd({y: 2}): 1})
    p7 = p2 ** 2
    assert repr(p7) == "x² - 2x + 1"
    assert p7 == MultiPoly({fd({x: 2}): 1, fd({x: 1}): -2, fd({}): 1})
    p8 = p3.substitute((x, MultiPoly({fd({t: 1}): 1, fd(): -1})))
    assert repr(p8) == "t² - 2t"
    assert p8 == MultiPoly({fd({t: 2}): 1, fd({t: 1}): -2})

    # Polynomial

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
    assert repr(p1) == "x²"
    p2 = Polynomial(1, 0, 2)
    assert repr(p2) == "2x² + 1"
    p3 = p1 * p2
    assert repr(p3) == "2x⁴ + x²"
    p4 = p3 + p2
    assert repr(p4) == "2x⁴ + 3x² + 1"
    p5 = p4 + 8
    assert repr(p5) == "2x⁴ + 3x² + 9"
    p6 = p3 - 8
    assert repr(p6) == "2x⁴ + x² - 8"
    p7 = p4 - p3
    assert repr(p7) == "2x² + 1"

    assert 36 == p3(2)
    assert 4 == p1(2)
    assert 9 == p2(2)
    assert Polynomial(1, 0, 3, 0, 2) == p4
    assert Polynomial(as_dict={4: 2, 2: 3, 0: 9}) == p5
    assert Polynomial(as_dict={4: 2, 2: 1, 0: -8}) == p6
    assert p7 == Polynomial(0, 0, 1) * 2 + 1

    p8 = Polynomial(1, 1)
    p9 = Polynomial(1, 1)
    assert repr(p8 * p9) == "x² + 2x + 1"

    p10 = Polynomial(1, 1)
    p11 = Polynomial(-1, 1)
    assert repr(p10 * p11) == "x² - 1"

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


if __name__ == "__main__":
    test()

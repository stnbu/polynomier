from polynomier import Polynomial, fd
from polynomier.symbols import *


def test():

    p0 = Polynomial({fd([(x, 2)]): 3, fd([(y, 1)]): 1})
    assert repr(p0) == "3x² + y"
    p1 = Polynomial({fd([(x, 2)]): 2, fd([(y, 1)]): 1})
    assert repr(p1) == "2x² + y"
    p2 = Polynomial({fd({x: 1}): 1, fd(): -1})
    assert repr(p2) == "x - 1"
    p3 = Polynomial({fd({x: 2}): 1, fd(): -1})
    assert repr(p3) == "x² - 1"
    p4 = p0 + p1
    assert repr(p4) == "5x² + 2y"
    assert p4 == Polynomial({fd({x: 2}): 5, fd({y: 1}): 2})
    p5 = p0 - p1
    assert repr(p5) == "x²"
    assert p5 == Polynomial({fd({x: 2}): 1})
    p6 = p0 * p1
    assert repr(p6) == "6x⁴ + 5x²y + y²"
    assert p6 == Polynomial({fd({x: 4}): 6, fd({y: 1, x: 2}): 5, fd({y: 2}): 1})
    p7 = p2 ** 2
    assert repr(p7) == "x² - 2x + 1"
    assert p7 == Polynomial({fd({x: 2}): 1, fd({x: 1}): -2, fd({}): 1})
    p8 = p3.substitute((x, Polynomial({fd({t: 1}): 1, fd(): -1})))
    assert repr(p8) == "t² - 2t"
    assert p8 == Polynomial({fd({t: 2}): 1, fd({t: 1}): -2})

    # Polynomial

    p1 = Polynomial({fd({x: 2}): 1})
    assert repr(p1) == "x²"
    p2 = Polynomial({fd({x: 2}): 2, fd(): 1})
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

    assert Polynomial({fd(): 1, fd({x: 2}): 3, fd({x: 4}): 2}) == p4
    assert Polynomial({fd({x: 4}): 2, fd({x: 2}): 3, fd(): 9}) == p5
    assert Polynomial({fd({x: 4}): 2, fd({x: 2}): 1, fd(): -8}) == p6
    assert p7 == Polynomial({fd({x: 2}): 1}) * 2 + 1

    p8 = Polynomial({fd({x: 1}): 1, fd(): 1})
    p9 = Polynomial({fd({x: 1}): 1, fd(): 1})
    assert repr(p8 * p9) == "x² + 2x + 1"

    p10 = Polynomial({fd({x: 1}): 1, fd(): 1})
    p11 = Polynomial({fd({x: 1}): 1, fd(): -1})
    assert repr(p10 * p11) == "x² - 1"

    # Other fields...

    a = 3 - 4j
    b = -1 + 1j
    c = 4 + 0j
    d = -0.5j

    p12 = Polynomial({fd({x: 1}): a, fd(): b})
    p13 = Polynomial({fd({x: 2}): c, fd({x: 1}): d})
    assert p12 * p13 == Polynomial(
        {
            fd({"x": 3}): (12 - 16j),
            fd({"x": 2}): (-6 + 2.5j),
            fd({"x": 1}): (0.5 + 0.5j),
        }
    )


if __name__ == "__main__":
    test()

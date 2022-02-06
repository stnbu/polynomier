def super_int(num):
    num = str(num)
    if not num.isdecimal():
        raise ValueError("Expected int or str(int) as input")
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
    for c in num:
        result += lookup[int(c)]
    return result


from .multivar import Polynomial, fd
from . import symbols

__all__ = ["Polynomial", "fd", "str_to_poly"]
